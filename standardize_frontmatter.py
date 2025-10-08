#!/usr/bin/env python3
"""
Standardize Hugo post frontmatter:
- Remove empty title fields
- Remove explicit slug fields (Hugo auto-generates)
- Standardize date format with quotes
- Standardize category array syntax
"""

import re
from pathlib import Path

def standardize_frontmatter(file_path):
    """Process a single markdown file to standardize frontmatter."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split frontmatter and body
    parts = content.split('+++', 2)
    if len(parts) < 3:
        print(f"Skipping {file_path}: No valid TOML frontmatter")
        return False

    frontmatter = parts[1]
    body = parts[2]

    lines = frontmatter.strip().split('\n')
    new_lines = []
    modified = False

    for line in lines:
        line = line.rstrip()

        # Remove empty title fields
        if re.match(r'^title\s*=\s*""?\s*$', line):
            modified = True
            continue

        # Remove explicit slug fields
        if line.startswith('slug ='):
            modified = True
            continue

        # Standardize date format (add quotes if missing)
        date_match = re.match(r'^date\s*=\s*([^"\s].+)$', line)
        if date_match:
            date_value = date_match.group(1).strip()
            line = f'date = "{date_value}"'
            modified = True

        # Standardize categories array syntax
        if line.startswith('categories ='):
            # Convert [ "foo" ] to ["foo"]
            line = re.sub(r'\[\s+', '[', line)
            line = re.sub(r'\s+\]', ']', line)
            # Ensure spaces after commas
            line = re.sub(r',(\S)', r', \1', line)
            if '[ ' in frontmatter or ' ]' in frontmatter:
                modified = True

        # Remove empty summary fields
        if re.match(r'^summary\s*=\s*""?\s*$', line):
            modified = True
            continue

        new_lines.append(line)

    if modified:
        new_frontmatter = '\n'.join(new_lines)
        new_content = f'+++\n{new_frontmatter}\n+++{body}'

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True

    return False

def main():
    post_dir = Path('content/post')
    modified_count = 0

    for md_file in sorted(post_dir.glob('*.md')):
        if standardize_frontmatter(md_file):
            modified_count += 1
            print(f"Modified: {md_file.name}")

    print(f"\nTotal files modified: {modified_count}")

if __name__ == '__main__':
    main()
