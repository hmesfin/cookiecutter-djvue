#!/usr/bin/env python3
"""
Script to migrate remaining inline SVGs to unplugin-icons Lucide components.
This handles more complex SVG patterns like error/alert icons and location icons.
"""

import re
import os
from pathlib import Path

# Additional SVG to Icon mappings for remaining patterns
ADDITIONAL_SVG_MAPPINGS = {
    # Error/Alert icon
    'M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z': 'IconLucideAlertCircle',
    
    # Shield/Security icon
    'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z': 'IconLucideShieldCheck',
    
    # Phone icon
    'M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z': 'IconLucidePhone',
    
    # Location/Map icon (both paths together)
    'M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z.*M15 11a3 3 0 11-6 0 3 3 0 016 0z': 'IconLucideMapPin',
    
    # Lightbulb icon
    'M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z': 'IconLucideLightbulb',
}

def replace_svg_with_icon(content, svg_path, icon_name):
    """Replace SVG pattern with Lucide icon component."""
    
    # Pattern for single-path SVGs
    single_path_pattern = r'<svg[^>]*>\s*<path[^>]*d="' + re.escape(svg_path) + '"[^>]*>\s*</path>\s*</svg>'
    
    # Pattern for multi-path SVGs (for location icon)
    if 'M17.657 16.657' in svg_path:
        # Special handling for location icon with two paths
        multi_path_pattern = r'<svg[^>]*>\s*<path[^>]*d="M17\.657[^"]*"[^>]*>\s*</path>\s*<path[^>]*d="M15 11[^"]*"[^>]*>\s*</path>\s*</svg>'
        content = re.sub(multi_path_pattern, f'<{icon_name} class="w-6 h-6" />', content, flags=re.DOTALL)
    else:
        # Standard single path replacement
        content = re.sub(single_path_pattern, f'<{icon_name} class="w-6 h-6" />', content, flags=re.DOTALL)
    
    # Also handle cases with class attributes on SVG
    pattern_with_class = r'<svg\s+class="[^"]*"[^>]*>\s*<path[^>]*d="' + re.escape(svg_path) + '"[^>]*>\s*</path>\s*</svg>'
    content = re.sub(pattern_with_class, f'<{icon_name} class="w-6 h-6" />', content, flags=re.DOTALL)
    
    return content

def migrate_file(file_path):
    """Process a single Vue file to replace SVGs with icons."""
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    replacements = 0
    
    for svg_path, icon_name in ADDITIONAL_SVG_MAPPINGS.items():
        before_count = content.count('<svg')
        content = replace_svg_with_icon(content, svg_path, icon_name)
        after_count = content.count('<svg')
        if before_count != after_count:
            replacements += (before_count - after_count)
            print(f"  Replaced SVG with {icon_name}")
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Updated with {replacements} replacements")
    else:
        print(f"  No changes needed")
    
    return replacements

def main():
    # Files that still have SVGs based on our grep search
    files_to_check = [
        '{{cookiecutter.project_slug}}/frontend/src/modules/home/views/AboutView.vue',
        '{{cookiecutter.project_slug}}/frontend/src/modules/auth/views/EmailVerificationDoneView.vue',
        '{{cookiecutter.project_slug}}/frontend/src/modules/auth/views/EmailVerificationView.vue',
        '{{cookiecutter.project_slug}}/frontend/src/modules/home/views/ContactView.vue',
        '{{cookiecutter.project_slug}}/frontend/src/modules/home/views/PricingView.vue',
    ]
    
    # Get the project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    total_replacements = 0
    
    for file_path in files_to_check:
        full_path = project_root / file_path
        if full_path.exists():
            replacements = migrate_file(full_path)
            total_replacements += replacements
        else:
            print(f"File not found: {full_path}")
    
    print(f"\n✨ Migration complete! Replaced {total_replacements} inline SVGs with Lucide icons.")
    print("\nNote: Some SVGs are intentionally kept:")
    print("- Data URI SVGs for placeholder images")
    print("- Social media icons (Twitter, LinkedIn, GitHub)")
    print("- Dynamic SVGs with :d bindings")

if __name__ == '__main__':
    main()