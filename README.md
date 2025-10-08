# Micro.blog to Hugo Migration Tools

A collection of Python scripts to help migrate and refactor content from Micro.blog to Hugo.

## Overview

These scripts automate common tasks when migrating from Micro.blog to Hugo, including standardizing frontmatter, generating slugs, and cleaning up filenames.

## Prerequisites

- Python 3.6+
- Hugo site with exported Micro.blog content
- Content files in TOML frontmatter format (`+++` delimiters)

## Quick Start

For a one-command migration, use the wrapper script:

```bash
# Preview changes without modifying files
python3 migrate.py --dry-run

# Run full migration
python3 migrate.py

# Run with options
python3 migrate.py --skip-filenames  # Skip filename cleanup
python3 migrate.py --skip-slugs      # Skip slug generation
```

The wrapper script runs all steps in the recommended order with safety checks. For more granular control, use the individual scripts below.

## Scripts

### `migrate.py` (Wrapper Script)

One-stop-shop that runs all migration steps in order.

**What it does:**
- Runs standardize_frontmatter.py
- Runs simplify_filenames.py (optional)
- Runs add_slugs.py (optional)
- Provides safety checks and progress reporting

**Usage:**
```bash
python3 migrate.py              # Full migration
python3 migrate.py --dry-run    # Preview only
python3 migrate.py --help       # Show all options
```

**Options:**
- `--dry-run` - Preview changes without modifying files
- `--skip-filenames` - Skip filename simplification
- `--skip-slugs` - Skip slug generation

### 1. `standardize_frontmatter.py`

Cleans and standardizes TOML frontmatter across all posts.

**What it does:**
- Removes empty `title`, `slug`, and `summary` fields
- Quotes unquoted date values
- Standardizes category array syntax
- Removes trailing whitespace

**Usage:**
```bash
python3 standardize_frontmatter.py
```

**Before:**
```toml
+++
title = ""
date = 2024-01-15T10:30:00-05:00
categories = [ "Writing" ]
slug = ""
+++
```

**After:**
```toml
+++
date = "2024-01-15T10:30:00-05:00"
categories = ["Writing"]
+++
```

### 2. `simplify_filenames.py`

Removes date prefixes from content filenames.

**What it does:**
- Strips `YYYY-MM-DD-` prefix from filenames
- Detects and reports collisions
- Preserves file content and metadata

**Usage:**
```bash
python3 simplify_filenames.py
```

**Example:**
- `2024-01-15-my-post.md` → `my-post.md`
- `2024-01-15-photo.md` → `photo.md`

### 3. `add_slugs.py`

Intelligently generates slugs for posts missing them.

**What it does:**
- Generates slugs from post titles (if present)
- Generates slugs from first 6 words of content (for titleless posts)
- Handles collisions by appending `-2`, `-3`, etc.
- Skips posts that already have slugs

**Usage:**
```bash
python3 add_slugs.py
```

**Logic:**
- **Titled post:** `title = "My Great Post"` → `slug = "my-great-post"`
- **Titleless post:** `First six words of the post...` → `slug = "first-six-words-of-the"`

### 4. `fix_slugs.py`

Re-generates all slugs using improved algorithm.

**What it does:**
- Regenerates slugs for all posts (replaces existing)
- Includes all words (no minimum character length filter)
- Uses 6-word excerpts for titleless posts
- Handles collisions

**Usage:**
```bash
python3 fix_slugs.py
```

Use this if you previously generated slugs with `add_slugs.py` and want to improve them.

### 5. `reorganize_content.py`

Attempts to split content into separate directories by type.

**What it does:**
- Creates `content/posts/` and `content/notes/` directories
- Moves titled posts to `posts/`
- Moves titleless posts to `notes/`

**Usage:**
```bash
python3 reorganize_content.py
```

**⚠️ Warning:** This may break themes that expect a single `content/post/` directory. Test thoroughly and consider using categories/taxonomies instead.

## Recommended Migration Workflow

### Option 1: One-Command Migration (Easiest)

1. **Export content from Micro.blog**
   - Use Hugo export feature from your Micro.blog settings
   - Extract to your Hugo site's `content/post/` directory

2. **Download migration scripts**
   ```bash
   cd your-hugo-site/
   git clone https://github.com/shawnyeager/microblog-to-hugo scripts/migration
   cd scripts/migration
   ```

3. **Preview changes**
   ```bash
   python3 migrate.py --dry-run
   ```

4. **Run migration**
   ```bash
   python3 migrate.py
   ```

5. **Update Hugo config** for slug-based permalinks
   ```toml
   [permalinks]
     post = "/:slug/"
   ```

6. **Test and verify**
   ```bash
   cd ../..  # Return to Hugo site root
   hugo server
   ```

### Option 2: Step-by-Step (More Control)

1. **Export content from Micro.blog**
   - Use Hugo export feature from your Micro.blog settings
   - Extract to your Hugo site's `content/post/` directory

2. **Standardize frontmatter**
   ```bash
   python3 standardize_frontmatter.py
   ```

3. **Simplify filenames** (optional)
   ```bash
   python3 simplify_filenames.py
   ```

4. **Generate slugs**
   ```bash
   python3 add_slugs.py
   ```

5. **Update Hugo config** for slug-based permalinks
   ```toml
   [permalinks]
     post = "/:slug/"
   ```

6. **Test and verify**
   ```bash
   hugo server
   ```

## Configuration

All scripts assume:
- Content directory: `content/post/`
- Frontmatter format: TOML with `+++` delimiters
- Encoding: UTF-8

To use with different paths, edit the `post_dir` variable in each script:
```python
post_dir = Path('content/post')  # Change this path
```

## Safety Features

- **Backup recommended:** All scripts modify files in place. Commit to git first!
- **Collision detection:** Scripts detect and report filename/slug collisions
- **Dry-run output:** Scripts print what they're changing before modifying files
- **Skip unchanged:** Scripts skip files that don't need modifications

## Use Cases

### Micro.blog to Hugo Migration
Complete migration from Micro.blog export to clean Hugo site.

### Hugo Site Refactoring
Clean up existing Hugo content with inconsistent frontmatter or naming.

### Slug Generation
Add or regenerate URL-friendly slugs for posts.

### Permalink Simplification
Remove date-based URL structures in favor of slug-only URLs.

## Compatibility

- **Tested with:** Hugo 0.151.0
- **Theme:** Should work with any Hugo theme
- **Python:** 3.6+
- **Content format:** TOML frontmatter

## Contributing

Contributions welcome! Please:
- Test scripts on a backup/branch first
- Document any new features or options
- Follow existing code style
- Add examples to the README

## License

MIT License - feel free to use, modify, and distribute.

## Related Resources

- [Hugo Documentation](https://gohugo.io/documentation/)
- [Micro.blog](https://micro.blog)

## Support

For issues or questions, please [open an issue](https://github.com/shawnyeager/microblog-to-hugo/issues).
