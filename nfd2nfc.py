#!/usr/bin/env python3
"""
nfd2nfc.py — Convert NFD filenames to NFC in a specified directory.

Usage:
    nfd2nfc.py [-d <directory>]

If -d is not provided, the current directory is used.
"""

import os
import sys
import unicodedata


def convert_directory(target_dir: str) -> int:
    """Recursively rename NFD filenames to NFC. Returns the count of renamed files."""
    count = 0

    for entry in os.scandir(target_dir):
        if entry.is_file(follow_symlinks=False):
            old_name = entry.name
            new_name = unicodedata.normalize("NFC", old_name)
            if old_name != new_name:
                old_path = entry.path
                new_path = os.path.join(target_dir, new_name)
                os.rename(old_path, new_path)
                print(f"  {old_name} → {new_name}")
                count += 1
        elif entry.is_dir(follow_symlinks=False):
            count += convert_directory(entry.path)

    return count


def main() -> None:
    # ── argument parsing ──────────────────────────────────────────
    target_dir = "."
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "-d" and i + 1 < len(sys.argv):
            target_dir = sys.argv[i + 1]
            i += 2
        elif arg in ("-h", "--help"):
            print("Usage: nfd2nfc.py [-d <directory>]")
            print("Convert NFD filenames to NFC in the specified directory.")
            print("If -d is omitted, the current directory is used.")
            sys.exit(0)
        else:
            print(f"Unknown option: {arg}", file=sys.stderr)
            sys.exit(1)

    # Resolve to absolute path
    try:
        target_dir = os.path.realpath(target_dir)
    except OSError as e:
        print(f"Error: '{target_dir}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    count = convert_directory(target_dir)

    if count == 0:
        print("No NFD filenames found. Nothing to do.")
    else:
        print(f"\nRenamed {count} file(s).")


if __name__ == "__main__":
    main()
