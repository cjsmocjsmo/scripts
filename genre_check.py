#!/usr/bin/env python3
import os
import sys
import time
from mutagen import File

def check_missing_genres(target_dir):
    start_time = time.time()
    
    stats = {
        'mp3': 0,
        'flac': 0,
        'has_genre': 0,
        'missing_genre': 0,
        'errors': 0
    }
    
    print(f"Scanning directory: {os.path.abspath(target_dir)}\n")
    print("--- Files Missing Genre ---")
    
    for root, _, files in os.walk(target_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in ('.mp3', '.flac'):
                if ext == '.mp3':
                    stats['mp3'] += 1
                else:
                    stats['flac'] += 1

                file_path = os.path.join(root, file)
                try:
                    audio = File(file_path, easy=True)
                    if audio is None or not audio.get('genre'):
                        print(file_path)
                        stats['missing_genre'] += 1
                    else:
                        stats['has_genre'] += 1
                except Exception:
                    print(f"[READ ERROR] {file_path}")
                    stats['errors'] += 1

    elapsed_time = time.time() - start_time
    total_files = stats['mp3'] + stats['flac']

    # Final Report
    print("\n" + "=" * 45)
    print("               SCAN REPORT               ")
    print("=" * 45)
    print(f"Target Directory : {os.path.abspath(target_dir)}")
    print(f"Time Elapsed     : {elapsed_time:.2f} seconds")
    print("-" * 45)
    print(f"Total Audio Files: {total_files}")
    print(f"  - MP3 Files    : {stats['mp3']}")
    print(f"  - FLAC Files   : {stats['flac']}")
    print("-" * 45)
    print(f"Files WITH Genre : {stats['has_genre']}")
    print(f"Files NO Genre   : {stats['missing_genre']}")
    print(f"Read Errors      : {stats['errors']}")
    print("=" * 45)

if __name__ == '__main__':
    search_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    check_missing_genres(search_dir)