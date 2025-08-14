#!/usr/bin/env python3
"""
Script to fix remaining CSS classes that weren't converted to TailwindCSS.
"""

import re
import os
from pathlib import Path

def fix_remaining_css_classes(content):
    """Fix remaining CSS classes to TailwindCSS."""
    
    # Map of CSS classes to TailwindCSS equivalents
    replacements = {
        # Info classes
        'info-bg-white': 'bg-white dark:bg-gray-800',
        'info-description': 'text-gray-600 dark:text-gray-400 mb-6',
        'info-label': 'text-sm font-medium text-gray-500 dark:text-gray-400 mb-1',
        'info-value': 'text-gray-900 dark:text-gray-100',
        
        # Hero classes  
        'hero-subtitle': 'text-xl opacity-95',
        
        # Content classes
        'content-section': 'py-20 bg-white dark:bg-gray-900',
        'content-max-w-7xl': 'max-w-7xl',
        
        # Terms and Privacy classes
        'terms-view': 'min-h-screen bg-white dark:bg-gray-900',
        'terms-section': 'mb-12',
        'policy-section': 'mb-12',
        
        # Form classes
        'checkbox-input': 'w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500',
        'submit-message': 'mt-4 p-3 rounded-lg text-sm',
        
        # Pricing classes
        'billing-toggle': 'mt-8 flex items-center justify-center gap-4',
        'toggle': 'relative inline-block w-14 h-7',
        'toggle-slider': 'absolute cursor-pointer inset-0 bg-gray-300 rounded-full transition-colors peer-checked:bg-indigo-600',
        'badge': 'ml-2 px-2 py-1 bg-green-100 text-green-800 text-xs font-semibold rounded-full',
        
        # Other classes
        'acknowledgment': 'mt-12 p-6 bg-gray-50 dark:bg-gray-800 rounded-lg text-sm text-gray-600 dark:text-gray-400',
    }
    
    for old_class, new_class in replacements.items():
        # Replace class="old-class" with class="new-class"
        content = re.sub(f'class="{old_class}"', f'class="{new_class}"', content)
        # Replace class="old-class other-classes" with class="new-class other-classes"
        content = re.sub(f'class="{old_class} ', f'class="{new_class} ', content)
        # Replace class="other-classes old-class" with class="other-classes new-class"
        content = re.sub(f' {old_class}"', f' {new_class}"', content)
        # Replace in middle of class list
        content = re.sub(f' {old_class} ', f' {new_class} ', content)
    
    # Fix :class bindings for submit-message
    content = re.sub(r':class="\[\'submit-message\', submitStatus\]"', 
                     ':class="[\'mt-4 p-3 rounded-lg text-sm\', submitStatus === \'success\' ? \'bg-green-50 text-green-800 border border-green-200\' : \'bg-red-50 text-red-800 border border-red-200\']"', 
                     content)
    
    # Fix toggle input visibility
    content = re.sub(r'<input type="checkbox" v-model="isAnnual">',
                     '<input type="checkbox" v-model="isAnnual" class="sr-only peer">',
                     content)
    
    # Fix active state for billing toggle
    content = re.sub(r':class="\{ active: (!?)isAnnual \}"',
                     r':class="{ \'text-gray-900 dark:text-gray-100 font-semibold\': \1isAnnual, \'text-gray-500 dark:text-gray-400\': !\1isAnnual }"',
                     content)
    
    return content

def process_vue_file(file_path):
    """Process a single Vue file to fix CSS classes."""
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    content = fix_remaining_css_classes(content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Fixed remaining CSS classes")
        return True
    
    print(f"  No changes needed")
    return False

def main():
    """Main function to fix remaining CSS classes."""
    # Get the project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Files to fix
    views_to_fix = [
        '{{cookiecutter.project_slug}}/frontend/src/modules/home/views/ContactView.vue',
        '{{cookiecutter.project_slug}}/frontend/src/modules/home/views/TermsView.vue',
        '{{cookiecutter.project_slug}}/frontend/src/modules/home/views/PrivacyView.vue',
        '{{cookiecutter.project_slug}}/frontend/src/modules/home/views/PricingView.vue',
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