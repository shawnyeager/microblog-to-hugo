---
title: "Migrating from Micro.blog to Hugo: A Complete Guide"
date: 2025-10-08
slug: migrating-from-microblog-to-hugo
categories: ["Writing"]
summary: "How I migrated 331 posts from Micro.blog to a self-hosted Hugo site, including automation scripts and lessons learned."
---

After years of using Micro.blog, I decided to migrate to a self-hosted Hugo site. Here's how I did it, the challenges I faced, and the tools I built to automate the process.

## Why Migrate?

Micro.blog is excellent for its simplicity and community, but I wanted:
- Full control over my site's structure and URLs
- The flexibility to use any theme or layout
- A Git-based workflow for content management
- The ability to customize every aspect of the publishing pipeline

## The Migration Process

### Step 1: Export from Micro.blog

Micro.blog provides a Hugo export feature in your account settings. This exports all your posts as Markdown files with TOML frontmatter, preserving:
- Post content and metadata
- Images (copied to a static folder)
- Categories and tags
- Original post dates

The export gave me 331 posts dating back to 2020, all in a format Hugo could read immediately.

### Step 2: Choose a Theme

I forked the mnml theme from Micro.blog and adapted it for Hugo as [mnml-hugo](https://github.com/shawnyeager/mnml-hugo). This gave me a familiar aesthetic while allowing customization.

### Step 3: Clean Up the Mess

The exported content had several issues:
- Filenames prefixed with dates (`2024-01-15-my-post.md`)
- Inconsistent frontmatter formatting
- Empty title and slug fields
- Date-based permalink structure

This is where automation became essential.

## The Refactoring Scripts

I created a set of Python scripts to automate the cleanup. You can run them individually for granular control, or use the wrapper script for a one-command migration:

```bash
# One-command migration with safety checks
python3 migrate.py --dry-run  # Preview changes
python3 migrate.py            # Run migration
```

The individual scripts:

### 1. Standardize Frontmatter

The export had inconsistent TOML formatting:
```toml
title = ""
date = 2024-01-15T10:30:00-05:00
categories = [ "Writing" ]
```

The script cleaned this to:
```toml
date = "2024-01-15T10:30:00-05:00"
categories = ["Writing"]
```

Removing empty fields and quoting dates made the frontmatter cleaner and more consistent.

### 2. Simplify Filenames

Date prefixes in filenames were redundant since Hugo already tracks dates in frontmatter. The script removed `YYYY-MM-DD-` prefixes from 328 files:
- `2024-01-15-my-post.md` → `my-post.md`

This made the content directory much easier to navigate.

### 3. Generate Slugs

The most challenging part: creating URL-friendly slugs for 331 posts. Micro.blog used date-based URLs, but I wanted clean, readable slugs.

The script uses different strategies:
- **For titled posts:** Slugify the title (`"My Great Post"` → `my-great-post`)
- **For notes:** Extract the first 6 words (`"First six words of the post..."` → `first-six-words-of-the`)

It handles collisions by appending numbers and includes all words (even short ones like "of" and "the") for readability.

### 4. Permalink Configuration

With slugs in place, I simplified Hugo's permalink structure:

```toml
[permalinks]
  post = "/:slug/"
```

This changed URLs from:
- `https://shawnyeager.org/2024/01/15/my-post/`

To:
- `https://shawnyeager.org/my-post/`

Cleaner, more memorable, and easier to share.

## Setting Up a CMS

Static sites are great, but editing Markdown in a text editor isn't always convenient. I evaluated several headless CMS options:

### Tina CMS
Looked promising but felt heavy and complex for my needs.

### Decap CMS (formerly Netlify CMS)
Solid option but development has slowed.

### Sveltia CMS
A modern, lightweight alternative to Decap with better UX and active development. **This is what I chose.**

Setting up Sveltia required:
1. Creating a GitHub OAuth app
2. Configuring OAuth in Netlify
3. Adding a CMS config file

Now I can create and edit posts through a clean web interface while content stays in Git.

## Challenges and Solutions

### Challenge 1: Broken Permalinks

After generating slugs, I discovered 322 posts had broken permalinks pointing to `/`. The issue: Hugo can't generate slugs for titleless posts without an explicit `slug` field. The solution was to add intelligent slug generation for all posts.

### Challenge 2: Theme Compatibility

The theme expected all content in `content/post/`, but I initially tried organizing posts into `content/posts/` and `content/notes/`. This broke the archive and homepage. I reverted to a single directory and used categories instead.

### Challenge 3: Photo Post Captions

Photo posts weren't showing captions. This turned out to be a theme bug (not related to migration). I fixed it upstream in the mnml-hugo theme.

### Challenge 4: Hugo Fast Render

After updating frontmatter, changes didn't appear until I fully restarted the Hugo server. Fast Render Mode doesn't always detect frontmatter-only changes.

## The Results

The migration was successful:
- 331 posts migrated with clean URLs
- Simplified permalink structure
- Standardized, maintainable frontmatter
- Modern CMS for content editing
- Full Git-based workflow

## Open Source Tools

I've released the migration scripts as an open-source project: [microblog-to-hugo](https://github.com/shawnyeager/microblog-to-hugo)

The toolkit includes:
- **One-command migration** with `migrate.py` wrapper script
- **Individual scripts** for granular control
- **Dry-run mode** to preview changes safely
- **Comprehensive documentation** with examples

Use cases:
- Micro.blog to Hugo migrations
- General Hugo content refactoring
- Slug generation
- Frontmatter standardization

## Lessons Learned

1. **Export early, test often** - The Micro.blog export worked flawlessly, but test it before committing to a migration.

2. **Automate repetitive tasks** - Manually editing 331 files would have been error-prone and time-consuming.

3. **Keep it simple** - My attempt to organize content into separate directories broke the theme. Categories work fine.

4. **URLs matter** - Choose a permalink structure you'll be happy with long-term. Changing URLs later is painful.

5. **Git is your friend** - Every change was committed to a branch, making it easy to test and revert if needed.

## Should You Migrate?

Micro.blog remains an excellent platform. Consider migrating if you:
- Want full control over hosting and infrastructure
- Need advanced customization beyond what Micro.blog offers
- Prefer a Git-based publishing workflow
- Want to experiment with different static site generators

Stay with Micro.blog if you:
- Value simplicity and "it just works"
- Appreciate the integrated community features
- Don't want to manage hosting and deployments
- Prefer the managed, hassle-free experience

## What's Next?

With the migration complete, I'm focused on:
- Writing more frequently (easier now with the CMS)
- Customizing the theme further
- Adding search functionality
- Optimizing site performance

The migration took effort, but I now have a publishing platform that's exactly what I want.

---

**Tools mentioned:**
- [Hugo](https://gohugo.io) - Static site generator
- [Micro.blog](https://micro.blog) - Hosted microblogging platform
- [Sveltia CMS](https://github.com/sveltia/sveltia-cms) - Modern headless CMS
- [mnml-hugo](https://github.com/shawnyeager/mnml-hugo) - Minimalist Hugo theme
- [microblog-to-hugo](https://github.com/shawnyeager/microblog-to-hugo) - Migration scripts
- [Netlify](https://netlify.com) - Hosting and deployment

**Questions? Feedback?** [Open an issue](https://github.com/shawnyeager/microblog-to-hugo/issues) or reach out.
