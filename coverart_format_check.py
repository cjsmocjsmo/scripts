import sys
import re
from pathlib import Path

# Matches: artist_-_album (requires non-empty strings separated by '_-_')
COVER_PATTERN = re.compile(r"^(?P<artist>.+?)_-_(?P<album>.+)$")

def validate_cover_art(stem: str) -> bool:
    return bool(COVER_PATTERN.match(stem))

def scan_jpg_files(target_dir: str):
    root_path = Path(target_dir)

    if not root_path.exists() or not root_path.is_dir():
        print(f"Error: '{target_dir}' is not a valid directory.")
        sys.exit(1)

    total_jpgs = 0
    invalid_jpgs = 0

    print(f"Scanning for .jpg cover art in: {root_path.resolve()}\n")

    for file_path in root_path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() == ".jpg":
            total_jpgs += 1
            if not validate_cover_art(file_path.stem):
                invalid_jpgs += 1
                print(f"[INVALID] {file_path}")

    print("\n" + "=" * 60)
    print("Scan Complete.")
    print(f"Total .jpg files checked : {total_jpgs}")
    print(f"Invalid .jpg files found : {invalid_jpgs}")
    print("=" * 60)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    scan_jpg_files(target)