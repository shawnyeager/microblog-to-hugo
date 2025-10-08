#!/usr/bin/env python3
"""
Micro.blog to Hugo Migration Wrapper

One-stop-shop script that runs all migration steps in the recommended order.
Can be run with --dry-run to preview changes without modifying files.

Usage:
    python3 migrate.py                    # Run full migration
    python3 migrate.py --dry-run          # Preview changes only
    python3 migrate.py --skip-filenames   # Skip filename simplification
    python3 migrate.py --skip-slugs       # Skip slug generation
"""

import argparse
import subprocess
import sys
from pathlib import Path

def run_script(script_name, description, dry_run=False):
    """Run a migration script and report results."""
    print(f"\n{'='*70}")
    print(f"Step: {description}")
    print(f"Script: {script_name}")
    print(f"{'='*70}\n")

    if dry_run:
        print(f"[DRY RUN] Would execute: python3 {script_name}")
        print("Run without --dry-run to actually perform this step.\n")
        return True

    try:
        result = subprocess.run(
            ['python3', script_name],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:", result.stderr)
        print(f"✓ {description} completed successfully\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed")
        print(f"Error: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"✗ Script not found: {script_name}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Micro.blog to Hugo migration wrapper script',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 migrate.py                    # Run full migration
  python3 migrate.py --dry-run          # Preview all steps
  python3 migrate.py --skip-filenames   # Skip filename simplification
  python3 migrate.py --skip-slugs       # Skip slug generation

Steps executed (in order):
  1. Standardize frontmatter
  2. Simplify filenames (optional)
  3. Generate slugs

For more control, run individual scripts directly.
        """
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without modifying files'
    )
    parser.add_argument(
        '--skip-filenames',
        action='store_true',
        help='Skip filename simplification step'
    )
    parser.add_argument(
        '--skip-slugs',
        action='store_true',
        help='Skip slug generation step'
    )

    args = parser.parse_args()

    # Verify we're in the right directory
    if not Path('content/post').exists():
        print("Error: content/post directory not found")
        print("Run this script from your Hugo site root directory")
        sys.exit(1)

    print("="*70)
    print("Micro.blog to Hugo Migration")
    print("="*70)

    if args.dry_run:
        print("\n⚠️  DRY RUN MODE - No files will be modified")
    else:
        print("\n⚠️  This will modify files in place!")
        print("Make sure you have committed your work to git first.")
        response = input("\nContinue? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Migration cancelled")
            sys.exit(0)

    success = True

    # Step 1: Standardize frontmatter (always run)
    if not run_script(
        'standardize_frontmatter.py',
        'Standardize frontmatter formatting',
        args.dry_run
    ):
        success = False

    # Step 2: Simplify filenames (optional)
    if not args.skip_filenames:
        if not run_script(
            'simplify_filenames.py',
            'Remove date prefixes from filenames',
            args.dry_run
        ):
            success = False
    else:
        print("\n[SKIPPED] Filename simplification")

    # Step 3: Generate slugs (optional)
    if not args.skip_slugs:
        if not run_script(
            'add_slugs.py',
            'Generate intelligent slugs for posts',
            args.dry_run
        ):
            success = False
    else:
        print("\n[SKIPPED] Slug generation")

    # Final summary
    print("\n" + "="*70)
    if args.dry_run:
        print("DRY RUN COMPLETE")
        print("="*70)
        print("\nNo files were modified.")
        print("Run without --dry-run to perform the migration.")
    elif success:
        print("MIGRATION COMPLETE")
        print("="*70)
        print("\n✓ All steps completed successfully!")
        print("\nNext steps:")
        print("1. Review changes with: git diff")
        print("2. Test your site with: hugo server")
        print("3. Update hugo.toml permalinks to: post = '/:slug/'")
        print("4. Commit changes: git add . && git commit -m 'Migrate from Micro.blog'")
    else:
        print("MIGRATION INCOMPLETE")
        print("="*70)
        print("\n✗ Some steps failed. Review errors above.")
        print("You can:")
        print("- Fix issues and re-run this script")
        print("- Run individual scripts manually")
        print("- Revert changes with: git checkout .")
        sys.exit(1)

if __name__ == '__main__':
    main()
