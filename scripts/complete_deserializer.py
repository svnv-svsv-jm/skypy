#!/usr/bin/env python3
"""Complete FlatBuffer deserializer with error handling and multiple format support."""

import json
import struct
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class DeserializedData:
    file_name: str
    file_size: int
    format_type: str
    root_data: dict[str, Any]
    strings: list[dict[str, Any]]
    success: bool
    error_message: str | None = None


class CompleteFlatBufferDeserializer:
    def __init__(self, data: bytes, file_name: str):
        self.data = data
        self.file_name = file_name
        self.strings_cache = {}

    def detect_format(self) -> str:
        """Detect the format of the binary data"""
        if len(self.data) < 4:
            return "unknown"

        # Check for FlatBuffer signature
        root_offset = struct.unpack("<I", self.data[:4])[0]

        if root_offset < len(self.data) and root_offset > 0:
            # Check if it looks like a FlatBuffer
            if root_offset + 2 <= len(self.data):
                vtable_offset = struct.unpack(
                    "<H", self.data[root_offset : root_offset + 2]
                )[0]
                if 0 < vtable_offset < 1000:
                    return "flatbuffer"

        # Check for other common formats
        if self.data[:4] == b"TRPF":
            return "trpf"
        elif self.data[:4] == b"TRFS":
            return "trfs"
        elif self.data[:4] == b"TRMD":
            return "trmd"
        else:
            return "unknown"

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

    def deserialize_flatbuffer(self) -> dict[str, Any]:
        """Deserialize FlatBuffer format"""
        try:
            root_offset = struct.unpack("<I", self.data[:4])[0]

            # Read vtable
            vtable_offset = struct.unpack(
                "<H", self.data[root_offset : root_offset + 2]
            )[0]
            vtable_start = root_offset - vtable_offset

            vtable_size = struct.unpack(
                "<H", self.data[vtable_start : vtable_start + 2]
            )[0]
            object_size = struct.unpack(
                "<H", self.data[vtable_start + 2 : vtable_start + 4]
            )[0]

            # Read fields
            fields = {}
            for i in range(2, vtable_size // 2):
                field_offset = struct.unpack(
                    "<H", self.data[vtable_start + i * 2 : vtable_start + (i + 1) * 2]
                )[0]
                if field_offset > 0:
                    field_value = self.read_field_value(root_offset + field_offset)
                    fields[f"field_{i-2}"] = field_value

            return {
                "root_offset": root_offset,
                "vtable_size": vtable_size,
                "object_size": object_size,
                "fields": fields,
            }
        except Exception as e:
            return {"error": str(e)}

    def read_field_value(self, field_offset: int) -> Any:
        """Read a field value at the given offset"""
        if field_offset >= len(self.data):
            return None

        # Try to read as uint32
        if field_offset + 4 <= len(self.data):
            uint32_val = struct.unpack(
                "<I", self.data[field_offset : field_offset + 4]
            )[0]
            if uint32_val < len(self.data) and uint32_val > 0:
                # Might be a pointer to string
                try:
                    return self.read_string(uint32_val)
                except:
                    return uint32_val
            return uint32_val

        return None

    def deserialize_unknown(self) -> dict[str, Any]:
        """Deserialize unknown format by analyzing patterns"""
        # Look for common patterns
        patterns = {}
        for i in range(0, len(self.data) - 4, 4):
            pattern = self.data[i : i + 4]
            if pattern in patterns:
                patterns[pattern] += 1
            else:
                patterns[pattern] = 1

        # Find most common patterns
        common_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)[
            :10
        ]

        return {
            "format": "unknown",
            "common_patterns": [
                {"pattern": p.hex(), "count": c} for p, c in common_patterns
            ],
            "header": self.data[:32].hex() if len(self.data) >= 32 else self.data.hex(),
        }

    def deserialize(self) -> DeserializedData:
        """Main deserialization method"""
        try:
            format_type = self.detect_format()
            strings = self.extract_all_strings()

            if format_type == "flatbuffer":
                root_data = self.deserialize_flatbuffer()
            else:
                root_data = self.deserialize_unknown()

            return DeserializedData(
                file_name=self.file_name,
                file_size=len(self.data),
                format_type=format_type,
                root_data=root_data,
                strings=strings,
                success=True,
            )

        except Exception as e:
            return DeserializedData(
                file_name=self.file_name,
                file_size=len(self.data),
                format_type="error",
                root_data={},
                strings=[],
                success=False,
                error_message=str(e),
            )


def analyze_file(file_path: Path) -> DeserializedData:
    """Analyze a single file"""
    print(f"Analyzing: {file_path}")

    with open(file_path, "rb") as f:
        data = f.read()

    deserializer = CompleteFlatBufferDeserializer(data, file_path.name)
    result = deserializer.deserialize()

    print(f"  Format: {result.format_type}")
    print(f"  Size: {result.file_size:,} bytes")
    print(f"  Strings: {len(result.strings)}")
    print(f"  Success: {result.success}")

    if not result.success:
        print(f"  Error: {result.error_message}")

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python complete_deserializer.py <file_path> [output_file]")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"File not found: {file_path}")
        sys.exit(1)

    result = analyze_file(file_path)

    # Show interesting strings
    interesting_strings = [
        s
        for s in result.strings
        if any(
            keyword in s["string"].lower()
            for keyword in [
                "battle",
                "scene",
                "pokemon",
                "trainer",
                "arc",
                "world",
                "data",
            ]
        )
    ]

    if interesting_strings:
        print(f"\nFound {len(interesting_strings)} interesting strings:")
        for s in interesting_strings[:20]:  # Show first 20
            print(f"  Offset 0x{s['offset']:x}: '{s['string']}'")

    # Export to JSON if output file specified
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(asdict(result), f, indent=2, ensure_ascii=False, default=str)
        print(f"\nExported to: {output_file}")


if __name__ == "__main__":
    main()
