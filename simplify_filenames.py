#!/usr/bin/env python3
"""
Simplify Hugo post filenames by removing date prefix.
Hugo uses the date from frontmatter, so dates in filenames are redundant.

Renames: 2025-10-06-collectivism-is-cancerous.md -> collectivism-is-cancerous.md
"""

import re
from pathlib import Path

def simplify_filename(file_path):
    """Remove YYYY-MM-DD prefix from filename."""
    filename = file_path.name

    # Match YYYY-MM-DD- prefix
    match = re.match(r'^\d{4}-\d{2}-\d{2}-(.+)$', filename)
    if not match:
        return None  # No date prefix to remove

    new_filename = match.group(1)
    new_path = file_path.parent / new_filename

    # Check for collision
    if new_path.exists():
        print(f"SKIP (collision): {filename} -> {new_filename}")
        return None

    file_path.rename(new_path)
    return new_filename

def main():
    posts_dir = Path('content/posts')
    notes_dir = Path('content/notes')

    renamed_count = 0

    for directory in [posts_dir, notes_dir]:
        print(f"\nProcessing {directory}/...")
        for md_file in sorted(directory.glob('*.md')):
            new_name = simplify_filename(md_file)
            if new_name:
                renamed_count += 1
                print(f"  {md_file.name} -> {new_name}")

    print(f"\nTotal files renamed: {renamed_count}")

if __name__ == '__main__':
    main()
