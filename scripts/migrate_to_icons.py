#!/usr/bin/env python3
"""
Migrate inline SVGs to unplugin-icons components
"""

import os
import re
from pathlib import Path

# Common SVG patterns mapped to Lucide icons
SVG_TO_ICON_MAP = {
    # Navigation and UI
    'M4 6h16M4 12h16M4 18h16': 'IconLucideMenu',  # Hamburger menu
    'M6 18L18 6M6 6l12 12': 'IconLucideX',  # Close/X
    'M10 19l-7-7m0 0l7-7m-7 7h18': 'IconLucideArrowLeft',  # Back arrow
    'M14 5l7 7m0 0l-7 7m7-7H3': 'IconLucideArrowRight',  # Forward arrow
    'M19 9l-7 7-7-7': 'IconLucideChevronDown',  # Chevron down
    'M5 15l7-7 7 7': 'IconLucideChevronUp',  # Chevron up
    'M9 5l7 7-7 7': 'IconLucideChevronRight',  # Chevron right
    'M15 19l-7-7 7-7': 'IconLucideChevronLeft',  # Chevron left
    
    # Actions
    'M12 6v6m0 0v6m0-6h6m-6 0H6': 'IconLucidePlus',  # Plus/Add
    'M12 4v16m8-8H4': 'IconLucidePlus',  # Plus variant
    'M20 12H4': 'IconLucideMinus',  # Minus
    'M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16': 'IconLucideTrash2',  # Delete/Trash
    'M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z': 'IconLucideEdit',  # Edit/Pencil
    
    # Status and Feedback
    'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z': 'IconLucideCheckCircle',  # Success/Check circle
    'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z': 'IconLucideXCircle',  # Error/X circle
    'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z': 'IconLucideAlertTriangle',  # Warning
    'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z': 'IconLucideInfo',  # Info
    'M5 13l4 4L19 7': 'IconLucideCheck',  # Simple check
    
    # File and Data
    'M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z': 'IconLucideDownload',  # Download
    'M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12': 'IconLucideUpload',  # Upload
    
    # Search and Filter
    'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z': 'IconLucideSearch',  # Search
    'M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z': 'IconLucideFilter',  # Filter
    
    # User and Account
    'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z': 'IconLucideUser',  # User
    'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z': 'IconLucideUsers',  # Users
    
    # Communication
    'M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z': 'IconLucideMail',  # Email
    'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9': 'IconLucideBell',  # Notification bell
    
    # Charts and Analytics
    'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z': 'IconLucideBarChart3',  # Bar chart
    'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6': 'IconLucideTrendingUp',  # Trending up
    'M13 17h8m0 0V9m0 8l-8-8-4 4-6-6': 'IconLucideTrendingDown',  # Trending down
    
    # Settings and Tools
    'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z': 'IconLucideSettings',  # Settings gear
    'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z': 'IconLucideLock',  # Lock
    
    # E-commerce
    'M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z': 'IconLucideShoppingCart',  # Shopping cart
    'M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z': 'IconLucideShoppingBag',  # Shopping bag
    
    # Time
    'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z': 'IconLucideClock',  # Clock
    'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z': 'IconLucideCalendar',  # Calendar
    
    # Money
    'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z': 'IconLucideDollarSign',  # Dollar/Money
    
    # Three dots menu
    'M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z': 'IconLucideMoreVertical',  # Vertical dots
    'M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z': 'IconLucideMoreHorizontal',  # Horizontal dots
}

def extract_svg_path(svg_html):
    """Extract the path data from an SVG element"""
    path_match = re.search(r'd="([^"]+)"', svg_html)
    if path_match:
        return path_match.group(1)
    return None

def find_matching_icon(svg_html):
    """Find the best matching icon for an SVG"""
    path = extract_svg_path(svg_html)
    if path:
        # Check for exact matches
        for svg_pattern, icon in SVG_TO_ICON_MAP.items():
            if svg_pattern in path or path in svg_pattern:
                return icon
        
        # Check for partial matches (for complex paths)
        for svg_pattern, icon in SVG_TO_ICON_MAP.items():
            if len(svg_pattern) > 20:  # Only check longer patterns
                if svg_pattern[:20] in path or path[:20] in svg_pattern:
                    return icon
    
    # Try to guess based on common attributes
    if 'chevron' in svg_html.lower():
        if 'down' in svg_html.lower():
            return 'IconLucideChevronDown'
        elif 'up' in svg_html.lower():
            return 'IconLucideChevronUp'
        elif 'left' in svg_html.lower():
            return 'IconLucideChevronLeft'
        elif 'right' in svg_html.lower():
            return 'IconLucideChevronRight'
    
    return None

def replace_svg_with_icon(file_path, dry_run=False):
    """Replace SVGs in a Vue file with icon components"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    original_content = content
    replacements = []
    
    # Find all SVG elements
    svg_pattern = r'<svg[^>]*>.*?</svg>'
    svgs = re.findall(svg_pattern, content, re.DOTALL)
    
    for svg in svgs:
        icon = find_matching_icon(svg)
        if icon:
            # Extract classes if present
            class_match = re.search(r'class="([^"]*)"', svg)
            classes = class_match.group(1) if class_match else 'w-5 h-5'
            
            # Create the icon component
            icon_component = f'<{icon} class="{classes}" />'
            
            # Replace the SVG with the icon component
            content = content.replace(svg, icon_component)
            replacements.append((svg[:50] + '...', icon))
    
    if not dry_run and replacements:
        with open(file_path, 'w') as f:
            f.write(content)
    
    return replacements

def main():
    base_dir = '/home/hmesfin/development/working-on/cookiecutter-djvue/{{cookiecutter.project_slug}}/frontend/src'
    
    # Find all Vue files
    vue_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.vue'):
                vue_files.append(os.path.join(root, file))
    
    total_replacements = 0
    
    print("🔍 Analyzing SVGs in Vue components...\n")
    
    for file_path in vue_files:
        replacements = replace_svg_with_icon(file_path, dry_run=True)
        if replacements:
            rel_path = os.path.relpath(file_path, base_dir)
            print(f"📄 {rel_path}")
            for svg, icon in replacements:
                print(f"   ✓ {icon}")
            print()
            total_replacements += len(replacements)
    
    if total_replacements > 0:
        print(f"\n📊 Found {total_replacements} SVGs that can be replaced with icons")
        
        # Check for command line argument
        import sys
        if '--apply' in sys.argv:
            print("\n🚀 Applying replacements...")
            actual_replacements = 0
            for file_path in vue_files:
                replacements = replace_svg_with_icon(file_path, dry_run=False)
                actual_replacements += len(replacements)
            
            print(f"\n✅ Successfully replaced {actual_replacements} SVGs with icon components!")
            print("\n⚠️  Remember to test the components to ensure icons display correctly.")
            print("💡 You may need to import some icons or adjust sizes.")
        else:
            print("\n💡 To apply these replacements, run: python migrate_to_icons.py --apply")
    else:
        print("No replaceable SVGs found or all SVGs are already using icon components.")

if __name__ == '__main__':
    main()