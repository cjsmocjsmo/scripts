import sqlite3
import os
from pathlib import Path

# --- Configuration ---
THUMBS_DIR = Path('/usr/share/rusic/thumbs/')
DB_PATH = '/usr/share/rusic/db/rusic.db'

# Update this query to match your specific table and column names
QUERY = "SELECT fullpath FROM album_images;"

def get_filesystem_images():
    """Returns a set of all filenames currently in the thumbs directory."""
    if not THUMBS_DIR.exists():
        print(f"Error: Directory {THUMBS_DIR} not found.")
        return set()
    
    # Grabs only files, ignores subdirectories
    return {f.name for f in THUMBS_DIR.iterdir() if f.is_file()}

def get_database_images():
    """Returns a set of filenames expected according to the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(QUERY)
        
        # Extract the first column from each row into a set
        db_images = {row[0] for row in cursor.fetchall()}
        
        conn.close()
        # print(db_images)
        db_paths = []
        for img in db_images:
            baz = os.path.basename(img)
            db_paths.append(baz)
        print(db_paths[1])
        dbpathz = set(db_paths)
        return dbpathz
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

def main():
    fs_images = get_filesystem_images()
    db_images = get_database_images()
    print(next(iter(fs_images), None))
    print(next(iter(db_images), None))

    if not fs_images or not db_images:
        print("Missing data from filesystem or database. Exiting.")
        return

    # Set difference: what is in the filesystem but NOT in the database
    orphaned_images = fs_images - db_images
    
    # Set difference: what is in the database but NOT in the filesystem (optional diagnostic)
    missing_images = db_images - fs_images

    print(f"Total in filesystem: {len(fs_images)}")
    print(f"Total in database:   {len(db_images)}")
    print("-" * 30)
    
    if orphaned_images:
        print(f"\nFound {len(orphaned_images)} extra images in '{THUMBS_DIR}':")
        for img in sorted(orphaned_images):
            print(f" - {img}")
    else:
        print("\nNo extra images found in the directory.")

    if missing_images:
        print(f"\nWarning: Found {len(missing_images)} records in the DB missing from the directory.")

if __name__ == '__main__':
    main()