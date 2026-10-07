import sys
import re
from pathlib import Path

# Pattern matches: disc_track_-_artist_-_album_-_song (extension omitted)
FILENAME_PATTERN = re.compile(
    r"^(?P<disc>\d+)_(?P<track>\d+)_-_(?P<artist>.+?)_-_(?P<album>.+?)_-_(?P<song>.+?)$"
)

def validate_filename(stem: str) -> tuple[bool, str]:
    match = FILENAME_PATTERN.match(stem)
    if not match:
        return False, "Does not match 'disc_track_-_artist_-_album_-_song'"

    disc = int(match.group("disc"))
    track = int(match.group("track"))

    if not (1 <= disc <= 50):
        return False, f"Disc number ({disc}) is out of range (1–50)"

    if not (1 <= track <= 100):
        return False, f"Track number ({track}) is out of range (1–100)"

    return True, "Valid"

def scan_directory(target_dir: str):
    root_path = Path(target_dir)

    if not root_path.exists() or not root_path.is_dir():
        print(f"Error: '{target_dir}' is not a valid directory.")
        sys.exit(1)

    total_files = 0
    skipped_files = 0
    invalid_files = 0

    print(f"Scanning directory and subdirectories: {root_path.resolve()}\n")

    for file_path in root_path.rglob("*"):
        if file_path.is_file():
            # Skip any .jpg or .JPG files
            if file_path.suffix.lower() == ".jpg":
                skipped_files += 1
                continue

            total_files += 1
            is_valid, reason = validate_filename(file_path.stem)

            if not is_valid:
                invalid_files += 1
                print(f"[INVALID] {file_path} \n          --> Reason: {reason}\n")

    print("=" * 60)
    print("Scan Complete.")
    print(f"Total files checked : {total_files}")
    print(f"Skipped (.jpg)      : {skipped_files}")
    print(f"Invalid files found : {invalid_files}")
    print("=" * 60)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    scan_directory(target)