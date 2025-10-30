"""Binary data analyzer for unknown FlatBuffers files."""

import struct
import sys
from pathlib import Path


def analyze_flatbuffer_header(data: bytes) -> dict[str, int] | None:
    """Analyze the FlatBuffer header to understand the structure."""
    if len(data) < 4:
        return None

    # Read the root table offset (first 4 bytes, little-endian)
    root_offset = struct.unpack("<I", data[:4])[0]

    print(f"Root table offset: 0x{root_offset:x} ({root_offset})")

    if root_offset >= len(data):
        print("ERROR: Root offset beyond file size")
        return None

    # Read the root table
    root_table_start = root_offset
    if root_table_start + 4 > len(data):
        print("ERROR: Root table beyond file size")
        return None

    # Read vtable offset (relative to root table)
    vtable_offset = struct.unpack("<H", data[root_table_start : root_table_start + 2])[
        0
    ]
    print(f"VTable offset: 0x{vtable_offset:x} ({vtable_offset})")

    if vtable_offset == 0:
        print("ERROR: Null vtable offset")
        return None

    vtable_start = root_table_start - vtable_offset
    if vtable_start < 0 or vtable_start + 4 > len(data):
        print("ERROR: VTable beyond file bounds")
        return None

    # Read vtable size and object size
    vtable_size = struct.unpack("<H", data[vtable_start : vtable_start + 2])[0]
    object_size = struct.unpack("<H", data[vtable_start + 2 : vtable_start + 4])[0]

    print(f"VTable size: {vtable_size} bytes")
    print(f"Object size: {object_size} bytes")

    # Analyze vtable entries
    print("\nVTable entries:")
    for i in range(2, vtable_size // 2):
        if vtable_start + (i + 1) * 2 <= len(data):
            entry = struct.unpack(
                "<H", data[vtable_start + i * 2 : vtable_start + (i + 1) * 2]
            )[0]
            print(f"  Entry {i-2}: offset {entry}")

    return {
        "root_offset": root_offset,
        "vtable_offset": vtable_offset,
        "vtable_size": vtable_size,
        "object_size": object_size,
        "vtable_start": vtable_start,
    }


def find_strings(data: bytes, min_length: int = 4) -> list[tuple[int, str]]:
    """Find potential string data in the binary."""
    strings: list[tuple[int, str]] = []
    i = 0
    while i < len(data) - min_length:
        # Look for null-terminated strings
        if data[i] != 0:
            start = i
            while i < len(data) and data[i] != 0:
                i += 1
            if i - start >= min_length:
                try:
                    string = data[start:i].decode("utf-8", errors="ignore")
                    if string.isprintable():
                        strings.append((start, string))
                except Exception:
                    pass
        i += 1
    return strings


def analyze_data_patterns(data: bytes) -> None:
    """Look for common data patterns."""
    print("\n=== Data Pattern Analysis ===")

    # Look for repeated 4-byte patterns (common in game data)
    patterns: dict[bytes, int] = {}
    for i in range(0, len(data) - 4, 4):
        pattern = data[i : i + 4]
        if pattern in patterns:
            patterns[pattern] += 1
        else:
            patterns[pattern] = 1

    # Show most common patterns
    common_patterns: list[tuple[bytes, int]] = sorted(
        patterns.items(), key=lambda x: x[1], reverse=True
    )[:10]
    print("Most common 4-byte patterns:")
    for pattern, count in common_patterns:
        hex_str = " ".join(f"{b:02x}" for b in pattern)
        print(f"  {hex_str}: {count} occurrences")


def main() -> None:
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python analyze_binary.py <file_path>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"File not found: {file_path}")
        sys.exit(1)

    print(f"Analyzing: {file_path}")
    print(f"File size: {file_path.stat().st_size:,} bytes")

    with open(file_path, "rb") as f:
        data = f.read()

    print("\n=== FlatBuffer Header Analysis ===")
    header_info = analyze_flatbuffer_header(data)

    if header_info:
        print("\n=== String Analysis ===")
        strings = find_strings(data)
        print(f"Found {len(strings)} potential strings:")
        for offset, string in strings[:20]:  # Show first 20 strings
            print(f"  Offset 0x{offset:x}: '{string}'")

        analyze_data_patterns(data)

        # Try to extract some basic data
        print("\n=== Basic Data Extraction ===")
        try:
            # Look for common data types at the root table
            root_start = header_info["root_offset"]
            print("Root table data (first 32 bytes):")
            root_data = data[root_start : root_start + 32]
            hex_str = " ".join(f"{b:02x}" for b in root_data)
            print(f"  {hex_str}")

            # Try to interpret as different data types
            print("\nTrying to interpret root table data:")
            for i in range(0, min(32, len(root_data)), 4):
                if i + 4 <= len(root_data):
                    uint32 = struct.unpack("<I", root_data[i : i + 4])[0]
                    int32 = struct.unpack("<i", root_data[i : i + 4])[0]
                    float32 = struct.unpack("<f", root_data[i : i + 4])[0]
                    print(
                        f"  Offset {i}: uint32={uint32}, int32={int32}, float={float32:.2f}"
                    )
        except Exception as e:
            print(f"Error extracting data: {e}")


if __name__ == "__main__":
    main()
