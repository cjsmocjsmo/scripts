import os
import re
import sys
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3

# Define target file extensions
VALID_EXTENSIONS = {'.mp3', '.flac'}

# Regular expression matching any character that is NOT a letter, number, or standard space
SPECIAL_CHAR_PATTERN = re.compile(r'[^a-zA-Z0-9\s]')

def get_album(file_path):
    """Extracts the album tag from an MP3 or FLAC file."""
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == '.flac':
            audio = FLAC(file_path)
            # FLAC tags are stored as lists in key-value pairs
            albums = audio.get('album', [])
            return albums[0] if albums else None
        elif ext == '.mp3':
            audio = EasyID3(file_path)
            albums = audio.get('album', [])
            return albums[0] if albums else None
    except Exception as e:
        # File might be corrupted or missing tags entirely
        return None
    return None

def scan_directory(root_dir):
    """Recursively walks a directory and checks album tags for special characters."""
    matched_files_count = 0
    scanned_files_count = 0

    print(f"Scanning directory: {root_dir}\n" + "-" * 60)

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in VALID_EXTENSIONS:
                scanned_files_count += 1
                file_path = os.path.join(dirpath, filename)
                album = get_album(file_path)

                if album:
                    # Find all special characters present in the album tag
                    found_chars = set(SPECIAL_CHAR_PATTERN.findall(album))
                    if found_chars:
                        matched_files_count += 1
                        chars_str = ", ".join(f"'{c}'" for c in sorted(found_chars))
                        print(f"File: {file_path}")
                        print(f"  album Tag: \"{album}\"")
                        print(f"  Found Chars: {chars_str}\n")

    print("-" * 60)
    print(f"Scan complete. Found {matched_files_count} matching file(s) out of {scanned_files_count} audio file(s).")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = input("Enter the directory path to scan: ").strip()

    if os.path.isdir(target_dir):
        scan_directory(target_dir)
    else:
        print(f"Error: '{target_dir}' is not a valid directory.")