import os
import sys
from mutagen.mp3 import MP3
from mutagen.flac import FLAC

def has_embedded_cover(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext == '.mp3':
            audio = MP3(filepath)
            # MP3 files store cover art in APIC ID3 frames
            return bool(audio.tags and any(key.startswith('APIC') for key in audio.tags.keys()))
        elif ext == '.flac':
            audio = FLAC(filepath)
            # FLAC files store cover art in the pictures block list
            return bool(audio.pictures)
    except Exception:
        # If metadata reading fails, treat as missing/invalid metadata
        return False
    return False

def check_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.mp3', '.flac')):
                filepath = os.path.join(root, file)
                if not has_embedded_cover(filepath):
                    print(filepath)

if __name__ == "__main__":
    # Pass the folder path as an argument, or default to current directory
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    
    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    check_directory(target_dir)