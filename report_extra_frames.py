#!/usr/bin/env python3
import os
import sys
import eyed3

# Allowed frames and image descriptions
ALLOWED_IDS = {"TIT2", "TALB", "TPE1", "TCON", "TRCK", "TPOS", "APIC"}
ALLOWED_APIC_DESCS = {"", "Cover (front)", "Front Cover"}

def inspect_mp3(filepath):
    try:
        audiofile = eyed3.load(filepath)
        if audiofile is None or audiofile.tag is None:
            return ["No ID3 tag found or unreadable"]

        extra_items = []
        
        # Check standard ID3 frames
        for frame in audiofile.tag.frame_set.values():
            frame_id = frame.id
            if frame_id not in ALLOWED_IDS:
                extra_items.append(f"Frame: {frame_id}")
            elif frame_id == "APIC":
                # Ensure it's a front cover image
                desc = getattr(frame, "description", "")
                picture_type = getattr(frame, "picture_type", None)
                
                # eyed3 picture_type 3 is usually Front Cover
                is_front_cover = (
                    desc in ALLOWED_APIC_DESCS or 
                    picture_type == 3
                )
                if not is_front_cover:
                    extra_items.append(f"APIC Image (Description: '{desc}', Type: {picture_type})")

        return extra_items

    except Exception as e:
        return [f"Error reading file: {e}"]

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