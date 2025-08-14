#!/usr/bin/env python3
"""
Script to fix the duplicated class attributes from the TailwindCSS conversion.
"""

import re
import os
from pathlib import Path

def fix_class_attributes(content):
    """Fix duplicated class attributes in the content."""
    
    # Fix pattern: class="class="..." -> class="..."
    content = re.sub(r'class="class="([^"]*)"', r'class="\1', content)
    
    # Fix pattern: :class="class="..." -> :class="..."
    content = re.sub(r':class="class="([^"]*)"', r':class="\1', content)
    
    # Fix duplicated class content within attributes
    # Example: class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md p-6"
    def remove_duplicate_classes(match):
        classes = match.group(1).split()
        # Remove duplicates while preserving order
        seen = set()
        unique_classes = []
        for cls in classes:
            if cls not in seen:
                seen.add(cls)
                unique_classes.append(cls)
        return f'class="{" ".join(unique_classes)}"'
    
    content = re.sub(r'class="([^"]*)"', remove_duplicate_classes, content)
    
    # Fix btn class combinations (e.g., "btn bg-indigo-600 ... px-6 py-3 ...-primary" -> proper classes)
    content = re.sub(r'(px-6 py-3 rounded-lg font-medium transition-all duration-200)-primary', 
                     r'\1 bg-indigo-600 text-white hover:bg-indigo-700', content)
    content = re.sub(r'(px-6 py-3 rounded-lg font-medium transition-all duration-200)-outline', 
                     r'\1 border-2 border-indigo-600 text-indigo-600 hover:bg-indigo-600 hover:text-white', content)
    content = re.sub(r'(px-6 py-3 rounded-lg font-medium transition-all duration-200)-white', 
                     r'\1 bg-white text-indigo-600 hover:bg-gray-100', content)
    content = re.sub(r'(px-6 py-3 rounded-lg font-medium transition-all duration-200)-lg', 
                     r'px-8 py-4 text-lg rounded-lg font-medium transition-all duration-200', content)
    
    # Fix some specific patterns
    content = re.sub(r'class="btn (bg-indigo-600[^"]*)-lg"', r'class="btn \1 px-8 py-4 text-lg"', content)
    
    # Fix nested class attributes in :class bindings
    content = re.sub(r':class="class="\[([^\]]*)\]""', r':class="[\1]"', content)
    
    # Clean up any remaining double quotes issues
    content = re.sub(r'"">', '">', content)
    
    return content

def process_vue_file(file_path):
    """Process a single Vue file to fix class attributes."""
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    content = fix_class_attributes(content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Fixed class attributes")
        return True
    
    print(f"  No changes needed")
    return False

def main():
    """Main function to fix all home module views."""
    # Get the project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Files to fix (home module views)
    views_to_fix = [
        '{{cookiecutter.project_slug}}/frontend/src/modules/home/views/AboutView.vue',
        '{{cookiecutter.project_slug}}/frontend/src/modules/home/views/FeaturesView.vue',
        '{{cookiecutter.project_slug}}/frontend/src/modules/home/views/PricingView.vue',
        '{{cookiecutter.project_slug}}/frontend/src/modules/home/views/ContactView.vue',
        '{{cookiecutter.project_slug}}/frontend/src/modules/home/views/TermsView.vue',
        '{{cookiecutter.project_slug}}/frontend/src/modules/home/views/PrivacyView.vue',
    ]
    
    fixed_count = 0
    
    for view_path in views_to_fix:
        full_path = project_root / view_path
        if full_path.exists():
            if process_vue_file(full_path):
                fixed_count += 1
        else:
            print(f"File not found: {full_path}")
    
    print(f"\n✨ Fix complete! Fixed {fixed_count} files.")

if __name__ == '__main__':
    main()