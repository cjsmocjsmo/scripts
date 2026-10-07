#!/usr/bin/env python3
import os
import sys
import logging
import eyed3

# Lame tag CRC warnings are harmless noise for this report
logging.getLogger("eyed3").setLevel(logging.ERROR)

# Allowed frames
ALLOWED_IDS = {"TIT2", "TALB", "TPE1", "TCON", "TRCK", "TPOS", "APIC"}
FRONT_COVER = 3  # ID3 APIC picture type for front cover

def inspect_mp3(filepath):
    try:
        audiofile = eyed3.load(filepath)
        if audiofile is None or audiofile.tag is None:
            return ["No ID3 tag found or unreadable"]

        extra_items = []
        
        for raw_id, frames in audiofile.tag.frame_set.items():
            frame_id = raw_id.decode("ascii", "replace") if isinstance(raw_id, bytes) else str(raw_id)
            if frame_id not in ALLOWED_IDS:
                extra_items.append(f"Frame: {frame_id} (x{len(frames)})")
            elif frame_id == "APIC":
                for frame in frames:
                    picture_type = getattr(frame, "picture_type", None)
                    if picture_type != FRONT_COVER:
                        desc = getattr(frame, "description", "")
                        extra_items.append(f"APIC Image (Description: '{desc}', Type: {picture_type})")

        return extra_items

    except Exception as e:
        return [f"Error reading file ({type(e).__name__}): {e}"]

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} /path/to/music/dir")
        sys.exit(1)

    root_dir = sys.argv[1]
    if not os.path.isdir(root_dir):
        print(f"Error: {root_dir} is not a valid directory.")
        sys.exit(1)

    print(f"Scanning '{root_dir}' for extra/non-standard tags...")
    
    flagged_count = 0
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(".mp3"):
                filepath = os.path.join(dirpath, filename)
                extra_frames = inspect_mp3(filepath)
                
                if extra_frames:
                    flagged_count += 1
                    print(f"\n[FLAGGED] {filepath}")
                    for item in extra_frames:
                        print(f"  - {item}")

    print(f"\nScan complete. Flagged {flagged_count} file(s).")

if __name__ == "__main__":
    main()