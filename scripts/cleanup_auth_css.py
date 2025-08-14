#!/usr/bin/env python3
"""
Remove CSS styles from auth views for TailwindCSS-only consistency
"""

import os
import re

def remove_css_styles(file_path):
    """Remove style sections from auth components when using TailwindCSS"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Only process if TailwindCSS is being used
    if 'cookiecutter.css_framework == \'tailwindcss\'' not in content:
        return 0
    
    # Pattern to match the style section that should be removed for TailwindCSS
    # This matches the conditional style section that's only for non-Tailwind
    pattern = r'<style scoped>\s*{% if cookiecutter\.css_framework == \'none\' -%}.*?{%- endif %}\s*</style>'
    
    # Remove the style section
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Also clean up any remaining empty style tags
    content = re.sub(r'<style scoped>\s*</style>\s*', '', content)
    
    if content != original_content:
        with open(file_path, 'w') as f:
            f.write(content)
        return 1
    return 0

def main():
    base_dir = '/home/hmesfin/development/working-on/cookiecutter-djvue/{{cookiecutter.project_slug}}/frontend/src'
    
    # Auth views to clean up
    auth_views = [
        'modules/auth/views/LoginView.vue',
        'modules/auth/views/RegisterView.vue',
        'modules/auth/views/ForgotPasswordView.vue',
        'modules/auth/views/ResetPasswordView.vue'
    ]
    
    total_updated = 0
    
    for view_path in auth_views:
        full_path = os.path.join(base_dir, view_path)
        if os.path.exists(full_path):
            updated = remove_css_styles(full_path)
            if updated:
                print(f"✓ Removed CSS from {view_path}")
                total_updated += 1
            else:
                print(f"  No CSS to remove from {view_path}")
        else:
            print(f"  File not found: {view_path}")
    
    # Also check DashboardLayout
    layout_path = os.path.join(base_dir, 'layouts/DashboardLayout.vue')
    if os.path.exists(layout_path):
        updated = remove_css_styles(layout_path)
        if updated:
            print(f"✓ Removed CSS from layouts/DashboardLayout.vue")
            total_updated += 1
        else:
            print(f"  No CSS to remove from layouts/DashboardLayout.vue")
    
    print(f"\nTotal components cleaned: {total_updated}")

if __name__ == '__main__':
    main()