#!/usr/bin/env python3
"""Universal FlatBuffer deserializer that can handle unknown schemas
and create working Python objects from binary data
"""

import json
import struct
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class FlatBufferField:
    name: str
    offset: int
    value: Any
    type_hint: str = "unknown"


@dataclass
class FlatBufferTable:
    name: str
    offset: int
    fields: list[FlatBufferField]
    vtable_size: int
    object_size: int


class UniversalFlatBufferDeserializer:
    def __init__(self, data: bytes):
        self.data = data
        self.root_offset = struct.unpack("<I", data[:4])[0]
        self.tables = []
        self.strings_cache = {}

    def read_string(self, offset: int) -> str:
        """Read a null-terminated string with caching"""
        if offset in self.strings_cache:
            return self.strings_cache[offset]

        start = offset
        while offset < len(self.data) and self.data[offset] != 0:
            offset += 1

        string = self.data[start:offset].decode("utf-8", errors="ignore")
        self.strings_cache[offset] = string
        return string

    def read_vtable(self, table_offset: int) -> dict[str, int]:
        """Read vtable for a table"""
        vtable_offset = struct.unpack("<H", self.data[table_offset : table_offset + 2])[
            0
        ]
        if vtable_offset == 0:
            return {}

        vtable_start = table_offset - vtable_offset
        vtable_size = struct.unpack("<H", self.data[vtable_start : vtable_start + 2])[0]
        object_size = struct.unpack(
            "<H", self.data[vtable_start + 2 : vtable_start + 4]
        )[0]

        entries = {}
        for i in range(2, vtable_size // 2):
            field_offset = struct.unpack(
                "<H", self.data[vtable_start + i * 2 : vtable_start + (i + 1) * 2]
            )[0]
            entries[f"field_{i-2}"] = field_offset

        return {
            "vtable_size": vtable_size,
            "object_size": object_size,
            "entries": entries,
        }

    def read_vector(self, offset: int) -> list[Any]:
        """Read a vector (array)"""
        if offset >= len(self.data):
            return []

        length = struct.unpack("<I", self.data[offset : offset + 4])[0]
        if length > 10000:  # Sanity check
            return []

        vector_start = offset + 4
        items = []

        for i in range(length):
            item_offset = struct.unpack(
                "<I", self.data[vector_start + i * 4 : vector_start + (i + 1) * 4]
            )[0]
            if item_offset > 0:
                items.append(self.follow_pointer(item_offset))
            else:
                items.append(None)

        return items

    def follow_pointer(self, offset: int) -> Any:
        """Follow a pointer to its target"""
        if offset >= len(self.data):
            return None

        # Check if it's a string
        if self.data[offset] != 0:
            return self.read_string(offset)

        # Check if it's a table
        if offset + 2 <= len(self.data):
            vtable_offset = struct.unpack("<H", self.data[offset : offset + 2])[0]
            if 0 < vtable_offset < 1000:  # Reasonable vtable offset
                return self.read_table(offset)

        # Check if it's a vector
        if offset + 4 <= len(self.data):
            length = struct.unpack("<I", self.data[offset : offset + 4])[0]
            if 0 < length < 10000:  # Reasonable vector length
                return self.read_vector(offset)

        # Try as primitive value
        if offset + 4 <= len(self.data):
            return struct.unpack("<I", self.data[offset : offset + 4])[0]

        return None

    def read_table(self, offset: int) -> FlatBufferTable:
        """Read a complete table structure"""
        vtable_info = self.read_vtable(offset)
        if not vtable_info:
            return FlatBufferTable("Unknown", offset, [], 0, 0)

        fields = []
        for field_name, field_offset in vtable_info["entries"].items():
            if field_offset > 0:
                field_value = self.read_field_value(offset + field_offset)
                field_type = self.guess_field_type(field_value)
                fields.append(
                    FlatBufferField(field_name, field_offset, field_value, field_type)
                )

        return FlatBufferTable(
            "Table",
            offset,
            fields,
            vtable_info["vtable_size"],
            vtable_info["object_size"],
        )

    def read_field_value(self, field_offset: int) -> Any:
        """Read a field value at the given offset"""
        if field_offset >= len(self.data):
            return None

        # Try to read as different types
        if field_offset + 4 <= len(self.data):
            # Try as uint32
            uint32_val = struct.unpack(
                "<I", self.data[field_offset : field_offset + 4]
            )[0]
            if uint32_val < len(self.data) and uint32_val > 0:
                # Might be a pointer
                return self.follow_pointer(uint32_val)
            return uint32_val

        return None

    def guess_field_type(self, value: Any) -> str:
        """Guess the type of a field value"""
        if isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return "vector"
        elif isinstance(value, dict):
            return "table"
        elif isinstance(value, int):
            if 0 <= value <= 255:
                return "uint8"
            elif 0 <= value <= 65535:
                return "uint16"
            else:
                return "uint32"
        else:
            return "unknown"

    def deserialize_all(self) -> dict[str, Any]:
        """Deserialize the entire FlatBuffer structure"""
        root_table = self.read_table(self.root_offset)

        result = {
            "root_table": asdict(root_table),
            "all_strings": self.extract_all_strings(),
            "file_size": len(self.data),
            "root_offset": self.root_offset,
        }

        return result

    def extract_all_strings(self) -> list[dict[str, Any]]:
        """Extract all strings from the data"""
        strings = []
        i = 0
        while i < len(self.data) - 4:
            if self.data[i] != 0:
                start = i
                while i < len(self.data) and self.data[i] != 0:
                    i += 1
                if i - start > 3:  # Only strings longer than 3 chars
                    try:
                        string = self.data[start:i].decode("utf-8", errors="ignore")
                        if string.isprintable() and len(string) > 3:
                            strings.append(
                                {
                                    "offset": start,
                                    "string": string,
                                    "length": len(string),
                                }
                            )
                    except:
                        pass
            i += 1
        return strings

    def export_to_json(self, output_file: str):
        """Export the deserialized data to JSON"""
        data = self.deserialize_all()
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)


def main():
    if len(sys.argv) < 2:
        print("Usage: python universal_deserializer.py <file_path> [output_file]")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"File not found: {file_path}")
        sys.exit(1)

    print(f"Deserializing: {file_path}")

    with open(file_path, "rb") as f:
        data = f.read()

    deserializer = UniversalFlatBufferDeserializer(data)
    result = deserializer.deserialize_all()

    print(f"File size: {result['file_size']:,} bytes")
    print(f"Root offset: 0x{result['root_offset']:x}")
    print(f"Total strings: {len(result['all_strings'])}")

    # Show structure
    root_table = result["root_table"]
    print(f"\nRoot table has {len(root_table['fields'])} fields:")
    for field in root_table["fields"]:
        print(f"  {field['name']}: {field['type_hint']} = {field['value']}")

    # Show interesting strings
    interesting_strings = [
        s
        for s in result["all_strings"]
        if any(
            keyword in s["string"].lower()
            for keyword in ["battle", "scene", "pokemon", "trainer", "arc"]
        )
    ]

    print(f"\nFound {len(interesting_strings)} interesting strings:")
    for s in interesting_strings[:20]:  # Show first 20
        print(f"  Offset 0x{s['offset']:x}: '{s['string']}'")

    # Export to JSON if output file specified
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
        deserializer.export_to_json(output_file)
        print(f"\nExported to: {output_file}")


if __name__ == "__main__":
    main()
