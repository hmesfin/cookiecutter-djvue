#!/usr/bin/env python3
"""
Migrate all components to use emerald-600 as primary color and DRY component classes.
"""

import re
import os
from pathlib import Path

# Color mapping from indigo/blue to emerald
COLOR_REPLACEMENTS = {
    # Primary colors
    'bg-indigo-600': 'bg-emerald-600',
    'bg-indigo-500': 'bg-emerald-600',
    'bg-indigo-700': 'bg-emerald-700',
    'bg-blue-600': 'bg-emerald-600',
    'bg-blue-500': 'bg-emerald-600',
    'bg-blue-700': 'bg-emerald-700',
    
    # Dark mode primary
    'dark:bg-indigo-500': 'dark:bg-emerald-500',
    'dark:bg-indigo-600': 'dark:bg-emerald-500',
    'dark:bg-indigo-400': 'dark:bg-emerald-400',
    'dark:bg-blue-500': 'dark:bg-emerald-500',
    'dark:bg-blue-600': 'dark:bg-emerald-500',
    
    # Text colors
    'text-indigo-600': 'text-emerald-600',
    'text-indigo-500': 'text-emerald-600',
    'text-indigo-700': 'text-emerald-700',
    'text-blue-600': 'text-emerald-600',
    'text-blue-500': 'text-emerald-600',
    
    # Dark mode text
    'dark:text-indigo-400': 'dark:text-emerald-400',
    'dark:text-indigo-500': 'dark:text-emerald-400',
    'dark:text-blue-400': 'dark:text-emerald-400',
    
    # Hover states
    'hover:bg-indigo-700': 'hover:bg-emerald-700',
    'hover:bg-indigo-600': 'hover:bg-emerald-700',
    'hover:bg-blue-700': 'hover:bg-emerald-700',
    'hover:bg-blue-600': 'hover:bg-emerald-700',
    'dark:hover:bg-indigo-600': 'dark:hover:bg-emerald-600',
    'dark:hover:bg-blue-600': 'dark:hover:bg-emerald-600',
    
    # Borders
    'border-indigo-600': 'border-emerald-600',
    'border-indigo-500': 'border-emerald-600',
    'border-blue-600': 'border-emerald-600',
    'border-blue-500': 'border-emerald-600',
    'dark:border-indigo-400': 'dark:border-emerald-400',
    'dark:border-blue-400': 'dark:border-emerald-400',
    
    # Focus states
    'focus:ring-indigo-500': 'focus:ring-emerald-500',
    'focus:ring-indigo-600': 'focus:ring-emerald-500',
    'focus:ring-blue-500': 'focus:ring-emerald-500',
    'focus:border-indigo-500': 'focus:border-emerald-500',
    'focus:border-blue-500': 'focus:border-emerald-500',
    'dark:focus:ring-indigo-400': 'dark:focus:ring-emerald-400',
    'dark:focus:border-indigo-400': 'dark:focus:border-emerald-400',
    
    # Background light shades
    'bg-indigo-50': 'bg-emerald-50',
    'bg-indigo-100': 'bg-emerald-100',
    'bg-blue-50': 'bg-emerald-50',
    'dark:bg-indigo-900/20': 'dark:bg-emerald-900/20',
    'dark:bg-blue-900/20': 'dark:bg-emerald-900/20',
}

# Component class replacements (for common patterns)
COMPONENT_REPLACEMENTS = {
    # Long button classes to btn classes
    r'px-4 py-2 (?:text-sm )?font-medium (?:text-white )?bg-emerald-600 (?:dark:bg-emerald-500 )?hover:bg-emerald-700 (?:dark:hover:bg-emerald-600 )?rounded-(?:md|lg) (?:transition-(?:colors|all))?': 'btn btn-primary',
    
    # Secondary buttons
    r'px-4 py-2 (?:text-sm )?font-medium text-gray-700 (?:dark:text-gray-300 )?bg-gray-100 (?:dark:bg-gray-700 )?hover:bg-gray-200 (?:dark:hover:bg-gray-600 )?rounded-(?:md|lg) (?:transition-(?:colors|all))?': 'btn btn-secondary',
    
    # Form inputs - more specific pattern
    r'w-full px-3 py-2 border border-gray-300 rounded-(?:md|lg) focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 bg-white dark:bg-gray-[78]00 dark:border-gray-600 dark:text-gray-100 dark:focus:ring-emerald-400 dark:focus:border-emerald-400': 'form-input',
    
    # Form labels
    r'(?:block )?text-(?:sm )?(?:font-medium )?text-gray-(?:700|900) dark:text-gray-(?:100|300)(?:\s+mb-\d)?': 'form-label',
    
    # Links
    r'text-emerald-600 hover:text-emerald-700 dark:text-emerald-400 dark:hover:text-emerald-300': 'link',
}

def migrate_colors(content):
    """Replace old color scheme with emerald colors."""
    for old, new in COLOR_REPLACEMENTS.items():
        content = content.replace(old, new)
    return content

def migrate_to_component_classes(content):
    """Replace long utility chains with component classes where appropriate."""
    # Skip migration for certain patterns that shouldn't be replaced
    skip_patterns = [
        r'<style',  # Don't replace in style blocks
        r'@apply',  # Don't replace in @apply directives
        r'class:\s*[\'"`]',  # Don't replace in dynamic class bindings
    ]
    
    for skip_pattern in skip_patterns:
        if re.search(skip_pattern, content, re.IGNORECASE):
            return content
    
    # Apply component replacements carefully
    for pattern, replacement in COMPONENT_REPLACEMENTS.items():
        # Only replace in class attributes, not in style blocks
        content = re.sub(
            f'class="([^"]*){pattern}([^"]*)"',
            f'class="\\1{replacement}\\2"',
            content
        )
    
    return content

def process_file(file_path):
    """Process a single file."""
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # First migrate colors
    content = migrate_colors(content)
    
    # Then optionally migrate to component classes
    # Note: For now, we'll focus on color migration only
    # Component class migration can be done selectively
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Migrated to emerald color scheme")
        return True
    
    print(f"  No changes needed")
    return False

def main():
    """Main function."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Find all Vue and TypeScript/JavaScript files
    vue_files = list(Path(project_root / '{{cookiecutter.project_slug}}/frontend/src').rglob('*.vue'))
    ts_files = list(Path(project_root / '{{cookiecutter.project_slug}}/frontend/src').rglob('*.ts'))
    js_files = list(Path(project_root / '{{cookiecutter.project_slug}}/frontend/src').rglob('*.js'))
    
    all_files = vue_files + ts_files + js_files
    
    migrated_count = 0
    
    for file_path in all_files:
        if process_file(file_path):
            migrated_count += 1
    
    print(f"\n✨ Migration complete! Migrated {migrated_count} files to emerald color scheme.")
    print("\nNext steps:")
    print("1. Review the changes")
    print("2. Test the application")
    print("3. Optionally apply component classes for further DRY optimization")

if __name__ == '__main__':
    main()