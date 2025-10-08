#!/usr/bin/env python3
"""
Fix slugs that were generated with overly aggressive word filtering.
Regenerates slugs from content, including all words (not just 3+ chars).
"""

import re
from pathlib import Path

def slugify(text):
    """Convert text to URL-friendly slug."""
    slug = text.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    slug = slug.strip('-')
    return slug

def extract_first_words(text, num_words=6):
    """Extract first N meaningful words from text."""
    # Remove markdown images
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # Remove markdown links but keep link text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove markdown formatting
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

def fix_slug_in_post(file_path, used_slugs):
    """Regenerate slug for a post."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split frontmatter and body
    parts = content.split('+++', 2)
    if len(parts) < 3:
        return False

    frontmatter = parts[1]
    body = parts[2].strip()

    # Check if post has a title
    title_match = re.search(r'^title\s*=\s*"(.+)"', frontmatter, re.MULTILINE)

    if title_match:
        # Use title for slug
        base_slug = slugify(title_match.group(1))
    else:
        # Use first words of body for slug
        first_words = extract_first_words(body)
        if not first_words:
            return False
        base_slug = slugify(first_words)

    # Handle collisions
    slug = base_slug
    counter = 2
    while slug in used_slugs:
        slug = f"{base_slug}-{counter}"
        counter += 1

    used_slugs.add(slug)

    # Check if slug needs updating
    current_slug_match = re.search(r'^slug\s*=\s*"(.+)"', frontmatter, re.MULTILINE)
    if current_slug_match and current_slug_match.group(1) == slug:
        return False  # Slug is already correct

    # Update or add slug
    if current_slug_match:
        new_frontmatter = re.sub(
            r'^slug\s*=\s*"[^"]+"',
            f'slug = "{slug}"',
            frontmatter,
            flags=re.MULTILINE
        )
    else:
        # Add slug after title or date
        lines = frontmatter.strip().split('\n')
        new_lines = []
        slug_added = False

        for line in lines:
            new_lines.append(line)
            if not slug_added and (line.startswith('title =') or line.startswith('date =')):
                new_lines.append(f'slug = "{slug}"')
                slug_added = True

        if not slug_added:
            new_lines.insert(0, f'slug = "{slug}"')

        new_frontmatter = '\n'.join(new_lines)

    new_content = f'+++\n{new_frontmatter}\n+++\n{body}\n'

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True

def main():
    post_dir = Path('content/post')
    used_slugs = set()
    fixed_count = 0

    for md_file in sorted(post_dir.glob('*.md')):
        if fix_slug_in_post(md_file, used_slugs):
            fixed_count += 1
            print(f"Fixed: {md_file.name}")

    print(f"\nTotal slugs fixed: {fixed_count}")

if __name__ == '__main__':
    main()
