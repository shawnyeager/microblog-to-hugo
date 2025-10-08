#!/usr/bin/env python3
"""
Add slug fields to all Hugo posts.
- Posts with titles: generate slug from title
- Posts without titles: generate slug from first few words of content
"""

import re
from pathlib import Path
from collections import defaultdict

def slugify(text):
    """Convert text to URL-friendly slug."""
    # Convert to lowercase
    slug = text.lower()
    # Remove special characters, keep alphanumeric and spaces
    slug = re.sub(r'[^\w\s-]', '', slug)
    # Replace whitespace with hyphens
    slug = re.sub(r'[-\s]+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug

def extract_first_words(text, num_words=4):
    """Extract first N meaningful words from text."""
    # Remove markdown images, links, and formatting
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'[*_`]', '', text)

    # Split into words and filter
    words = text.split()
    meaningful_words = []

    for word in words:
        # Skip emojis and symbols, but keep all words with letters
        if re.search(r'[a-zA-Z]', word):
            meaningful_words.append(word)
            if len(meaningful_words) >= num_words:
                break

    return ' '.join(meaningful_words)

def add_slug_to_post(file_path, used_slugs):
    """Add slug field to a post if missing."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split frontmatter and body
    parts = content.split('+++', 2)
    if len(parts) < 3:
        print(f"SKIP: {file_path.name} - No valid frontmatter")
        return None

    frontmatter = parts[1]
    body = parts[2].strip()

    # Check if slug already exists
    if re.search(r'^slug\s*=', frontmatter, re.MULTILINE):
        return None

    # Extract title if exists
    title_match = re.search(r'^title\s*=\s*"([^"]+)"', frontmatter, re.MULTILINE)

    if title_match:
        # Generate slug from title
        base_slug = slugify(title_match.group(1))
    else:
        # Generate slug from first words of content
        first_words = extract_first_words(body)
        if not first_words:
            # Fallback to filename without extension
            base_slug = file_path.stem
        else:
            base_slug = slugify(first_words)

    # Handle collisions
    slug = base_slug
    counter = 2
    while slug in used_slugs:
        slug = f"{base_slug}-{counter}"
        counter += 1

    used_slugs[slug] += 1

    # Add slug to frontmatter (after title if exists, otherwise after date)
    lines = frontmatter.strip().split('\n')
    new_lines = []
    slug_added = False

    for i, line in enumerate(lines):
        new_lines.append(line)

        # Add slug after title if title exists
        if not slug_added and title_match and line.startswith('title ='):
            new_lines.append(f'slug = "{slug}"')
            slug_added = True
        # Otherwise add after date
        elif not slug_added and line.startswith('date ='):
            new_lines.append(f'slug = "{slug}"')
            slug_added = True

    new_frontmatter = '\n'.join(new_lines)
    new_content = f'+++\n{new_frontmatter}\n+++\n\n{body}\n'

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return slug

def main():
    post_dir = Path('content/post')
    used_slugs = defaultdict(int)
    added_count = 0

    for md_file in sorted(post_dir.glob('*.md')):
        slug = add_slug_to_post(md_file, used_slugs)
        if slug:
            added_count += 1
            print(f"  {md_file.name} → {slug}")

    print(f"\nTotal slugs added: {added_count}")
    print(f"Unique slugs: {len(used_slugs)}")

    # Check for collisions
    collisions = {slug: count for slug, count in used_slugs.items() if count > 1}
    if collisions:
        print(f"\nSlug collisions detected: {len(collisions)}")
        for slug, count in sorted(collisions.items()):
            print(f"  {slug}: {count} occurrences")

if __name__ == '__main__':
    main()
