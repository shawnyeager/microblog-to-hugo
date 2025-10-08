#!/usr/bin/env python3
"""
Migrate images from static/ to assets/ for Hugo image processing.

This script moves image files from static/images/ to assets/images/ to enable
Hugo's built-in image processing (WebP conversion, responsive srcsets, etc.).

Usage:
    python3 migrate_images.py              # Migrate all images
    python3 migrate_images.py --dry-run    # Preview changes without modifying files
    python3 migrate_images.py --year 2024  # Migrate only images from 2024
"""

import argparse
import shutil
from pathlib import Path

# Image extensions to migrate
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}

def migrate_images(dry_run=False, year=None):
    """
    Move image files from static/images/ to assets/images/.

    Args:
        dry_run: If True, print actions without modifying files
        year: If specified, only migrate images from that year's directory
    """
    static_dir = Path('static/images')
    assets_dir = Path('assets/images')

    if not static_dir.exists():
        print(f"Error: {static_dir} does not exist")
        return

    # Create assets/images if it doesn't exist
    if not dry_run and not assets_dir.exists():
        assets_dir.mkdir(parents=True)
        print(f"Created {assets_dir}/")

    # Find all image files
    if year:
        pattern = f"{year}/*"
        search_path = static_dir / str(year)
        if not search_path.exists():
            print(f"Error: {search_path} does not exist")
            return
    else:
        pattern = "**/*"

    image_files = []
    for ext in IMAGE_EXTENSIONS:
        image_files.extend(static_dir.glob(f"{pattern}{ext}"))

    if not image_files:
        print(f"No images found in {static_dir}/{pattern if year else ''}")
        return

    print(f"Found {len(image_files)} image(s) to migrate")
    print()

    migrated = 0
    for img_file in sorted(image_files):
        # Get relative path from static/images/
        rel_path = img_file.relative_to(static_dir)
        dest_file = assets_dir / rel_path

        if dry_run:
            print(f"Would move: {img_file} -> {dest_file}")
        else:
            # Create parent directory if needed
            dest_file.parent.mkdir(parents=True, exist_ok=True)

            # Move the file
            shutil.move(str(img_file), str(dest_file))
            print(f"Moved: {img_file} -> {dest_file}")

        migrated += 1

    print()
    if dry_run:
        print(f"Dry run complete. Would migrate {migrated} image(s).")
        print("Run without --dry-run to perform migration.")
    else:
        print(f"Migration complete. Moved {migrated} image(s) to {assets_dir}/")
        print()
        print("Note: Use absolute paths in frontmatter (/images/...) for Hugo best practices")
        print("Hugo will automatically process images from assets/ and serve originals at /images/")

def main():
    parser = argparse.ArgumentParser(
        description='Migrate images from static/ to assets/ for Hugo processing'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without modifying files'
    )
    parser.add_argument(
        '--year',
        type=str,
        help='Only migrate images from specified year (e.g., 2024)'
    )

    args = parser.parse_args()

    migrate_images(dry_run=args.dry_run, year=args.year)

if __name__ == '__main__':
    main()
