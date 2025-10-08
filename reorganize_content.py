#!/usr/bin/env python3
"""
Reorganize Hugo content by type:
- Posts with titles -> content/posts/
- Posts without titles -> content/notes/
"""

import re
import shutil
from pathlib import Path

def has_title(file_path):
    """Check if a post has a non-empty title."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    parts = content.split('+++', 2)
    if len(parts) < 3:
        return False

    frontmatter = parts[1]

    # Check for title field with non-empty value
    title_match = re.search(r'^title\s*=\s*"(.+)"', frontmatter, re.MULTILINE)
    return title_match and title_match.group(1).strip()

def main():
    post_dir = Path('content/post')
    posts_dir = Path('content/posts')
    notes_dir = Path('content/notes')

    titled_count = 0
    note_count = 0

    for md_file in sorted(post_dir.glob('*.md')):
        if has_title(md_file):
            dest = posts_dir / md_file.name
            shutil.move(str(md_file), str(dest))
            titled_count += 1
            print(f"Post: {md_file.name}")
        else:
            dest = notes_dir / md_file.name
            shutil.move(str(md_file), str(dest))
            note_count += 1
            print(f"Note: {md_file.name}")

    print(f"\nMoved {titled_count} titled posts to content/posts/")
    print(f"Moved {note_count} notes to content/notes/")

if __name__ == '__main__':
    main()
