import sys
import subprocess
from pathlib import Path

def process_flac_directory(root_dir: str):
    root_path = Path(root_dir)
    
    if not root_path.is_dir():
        print(f"Error: Path '{root_dir}' is not a valid directory.")
        sys.exit(1)

    print(f"Scanning directory: {root_path}\n")

    # Recursively find all .flac files
    for flac_file in root_path.rglob("*.flac"):
        mp3_file = flac_file.with_suffix(".mp3")

        # Skip if the MP3 file already exists
        if mp3_file.exists():
            print(f"[SKIP] MP3 already exists: {mp3_file.name}")
            continue

        print(f"[CONVERTING] {flac_file.relative_to(root_path)}")

        # ffmpeg parameters for maximum MP3 quality:
        # -codec:a libmp3lame: Uses LAME MP3 encoder
        # -qscale:a 0: Highest VBR quality setting (V0, target ~245 kbps, max 320 kbps)
        # -map_metadata 0: Preserves tags (Artist, Album, Title, Track #, etc.)
        cmd = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel", "error",
            "-i", str(flac_file),
            "-codec:a", "libmp3lame",
            "-qscale:a", "0",
            "-map_metadata", "0",
            str(mp3_file)
        ]

        try:
            subprocess.run(cmd, check=True)
            print(f" -> Created: {mp3_file.name}")
        except subprocess.CalledProcessError as e:
            print(f" -> ERROR processing {flac_file.name}: {e}")
        except FileNotFoundError:
            print("Error: 'ffmpeg' executable not found. Ensure it is installed via apt.")
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 flac_to_mp3.py /path/to/music")
        sys.exit(1)

    target_dir = sys.argv[1]
    process_flac_directory(target_dir)