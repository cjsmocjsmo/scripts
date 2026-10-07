import os
import re
import sys
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3

# Define target file extensions
VALID_EXTENSIONS = {'.mp3', '.flac'}

# Regular expression matching any character that is NOT a letter, number, or standard space
SPECIAL_CHAR_PATTERN = re.compile(r'[^a-zA-Z0-9\s]')

def get_artist(file_path):
    """Extracts the artist tag from an MP3 or FLAC file."""
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == '.flac':
            audio = FLAC(file_path)
            # FLAC tags are stored as lists in key-value pairs
            artists = audio.get('artist', [])
            return artists[0] if artists else None
        elif ext == '.mp3':
            audio = EasyID3(file_path)
            artists = audio.get('artist', [])
            return artists[0] if artists else None
    except Exception as e:
        # File might be corrupted or missing tags entirely
        return None
    return None

def scan_directory(root_dir):
    """Recursively walks a directory and checks artist tags for special characters."""
    matched_files_count = 0
    scanned_files_count = 0

    print(f"Scanning directory: {root_dir}\n" + "-" * 60)

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in VALID_EXTENSIONS:
                scanned_files_count += 1
                file_path = os.path.join(dirpath, filename)
                artist = get_artist(file_path)

                if artist:
                    # Find all special characters present in the artist tag
                    found_chars = set(SPECIAL_CHAR_PATTERN.findall(artist))
                    if found_chars:
                        matched_files_count += 1
                        chars_str = ", ".join(f"'{c}'" for c in sorted(found_chars))
                        print(f"File: {file_path}")
                        print(f"  Artist Tag: \"{artist}\"")
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