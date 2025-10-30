#!/usr/bin/env python3
"""Advanced FlatBuffer deserializer for unknown schemas"""

import json
import struct
from pathlib import Path
from typing import Any


class FlatBufferDeserializer:
    def __init__(self, data: bytes):
        self.data = data
        self.root_offset = struct.unpack("<I", data[:4])[0]
        self.root_table_start = self.root_offset

    def read_vtable(self) -> dict[str, int]:
        """Read and parse the vtable"""
        vtable_offset = struct.unpack(
            "<H", self.data[self.root_table_start : self.root_table_start + 2]
        )[0]
        vtable_start = self.root_table_start - vtable_offset

        vtable_size = struct.unpack("<H", self.data[vtable_start : vtable_start + 2])[0]
        object_size = struct.unpack(
            "<H", self.data[vtable_start + 2 : vtable_start + 4]
        )[0]

        entries = {}
        for i in range(2, vtable_size // 2):
            entry_offset = struct.unpack(
                "<H", self.data[vtable_start + i * 2 : vtable_start + (i + 1) * 2]
            )[0]
            entries[f"field_{i-2}"] = entry_offset

        return {
            "vtable_size": vtable_size,
            "object_size": object_size,
            "entries": entries,
        }

    def read_field(self, field_offset: int, field_type: str = "auto") -> Any:
        """Read a field at the given offset"""
        if field_offset == 0:
            return None

        field_start = self.root_table_start + field_offset

        if field_type == "auto":
            # Try to determine type automatically
            if field_start + 4 <= len(self.data):
                # Try as uint32 first
                value = struct.unpack("<I", self.data[field_start : field_start + 4])[0]
                if value < len(self.data) and value > 0:
                    # Might be a pointer/offset
                    return self.follow_pointer(value)
                return value
        elif field_type == "uint32":
            return struct.unpack("<I", self.data[field_start : field_start + 4])[0]
        elif field_type == "int32":
            return struct.unpack("<i", self.data[field_start : field_start + 4])[0]
        elif field_type == "float":
            return struct.unpack("<f", self.data[field_start : field_start + 4])[0]
        elif field_type == "string":
            return self.read_string(field_start)
        elif field_type == "vector":
            return self.read_vector(field_start)

        return None

    def follow_pointer(self, offset: int) -> Any:
        """Follow a pointer to its target"""
        if offset >= len(self.data):
            return None

        # Check if it's a string
        if self.data[offset] != 0:
            return self.read_string(offset)

        # Check if it's a table
        vtable_offset = struct.unpack("<H", self.data[offset : offset + 2])[0]
        if vtable_offset > 0 and vtable_offset < 1000:  # Reasonable vtable offset
            return self.read_table(offset)

        # Check if it's a vector
        length = struct.unpack("<I", self.data[offset : offset + 4])[0]
        if length < 10000:  # Reasonable vector length
            return self.read_vector(offset)

        return None

    def read_string(self, offset: int) -> str:
        """Read a null-terminated string"""
        start = offset
        while offset < len(self.data) and self.data[offset] != 0:
            offset += 1
        return self.data[start:offset].decode("utf-8", errors="ignore")

    def read_vector(self, offset: int) -> list[Any]:
        """Read a vector (array)"""
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

    def read_table(self, offset: int) -> dict[str, Any]:
        """Read a table structure"""
        vtable_offset = struct.unpack("<H", self.data[offset : offset + 2])[0]
        if vtable_offset == 0:
            return {}

        vtable_start = offset - vtable_offset
        vtable_size = struct.unpack("<H", self.data[vtable_start : vtable_start + 2])[0]

        table = {}
        for i in range(2, vtable_size // 2):
            field_offset = struct.unpack(
                "<H", self.data[vtable_start + i * 2 : vtable_start + (i + 1) * 2]
            )[0]
            if field_offset > 0:
                field_value = self.read_field(field_offset)
                table[f"field_{i-2}"] = field_value

        return table

    def deserialize(self) -> dict[str, Any]:
        """Main deserialization method"""
        vtable = self.read_vtable()

        result = {"root_offset": self.root_offset, "vtable": vtable, "fields": {}}

        # Read all fields from the root table
        for field_name, field_offset in vtable["entries"].items():
            if field_offset > 0:
                field_value = self.read_field(field_offset)
                result["fields"][field_name] = field_value

        return result

    def extract_strings(self) -> list[dict[str, Any]]:
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


def analyze_file(file_path: Path) -> dict[str, Any]:
    """Analyze a FlatBuffer file and return structured data"""
    print(f"Analyzing: {file_path}")

    with open(file_path, "rb") as f:
        data = f.read()

    deserializer = FlatBufferDeserializer(data)

    # Get basic structure
    structure = deserializer.deserialize()

    # Extract strings
    strings = deserializer.extract_strings()

    # Filter interesting strings (likely game data)
    interesting_strings = [
        s
        for s in strings
        if any(
            keyword in s["string"].lower()
            for keyword in ["pokemon", "trainer", "move", "item", "battle", "data"]
        )
    ]

    return {
        "file_size": len(data),
        "structure": structure,
        "all_strings": strings[:50],  # First 50 strings
        "interesting_strings": interesting_strings,
        "total_strings": len(strings),
    }


def main():
    import sys

    if len(sys.argv) != 2:
        print("Usage: python flatbuffer_deserializer.py <file_path>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"File not found: {file_path}")
        sys.exit(1)

    result = analyze_file(file_path)

    print(f"\nFile size: {result['file_size']:,} bytes")
    print(f"Total strings found: {result['total_strings']}")
    print(f"Interesting strings: {len(result['interesting_strings'])}")

    print("\nStructure:")
    print(json.dumps(result["structure"], indent=2, default=str))

    if result["interesting_strings"]:
        print("\nInteresting strings:")
        for s in result["interesting_strings"][:20]:
            print(f"  Offset 0x{s['offset']:x}: '{s['string']}'")


if __name__ == "__main__":
    main()
