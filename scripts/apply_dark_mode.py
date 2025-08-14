#!/usr/bin/env python3

"""
Script to automatically apply dark mode classes to Vue components in a cookiecutter template
Usage: python scripts/apply_dark_mode.py [options]

Options:
  --dir PATH       Directory to process (default: {{cookiecutter.project_slug}}/frontend/src)
  --dry-run        Show what would be changed without modifying files
  --verbose        Show detailed processing information
  --backup         Create backup files before modifying
  --analyze        Analyze files without making changes
  --interactive    Prompt for confirmation on each file
"""

import os
import re
import sys
import glob
import shutil
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Color mappings for automatic dark mode conversion
COLOR_MAPPINGS = {
    # Backgrounds
    'bg-white': 'dark:bg-gray-900',
    'bg-gray-50': 'dark:bg-gray-900',
    'bg-gray-100': 'dark:bg-gray-800',
    'bg-gray-200': 'dark:bg-gray-700',
    'bg-gray-300': 'dark:bg-gray-600',
    'bg-red-50': 'dark:bg-red-900/20',
    'bg-green-50': 'dark:bg-green-900/20',
    'bg-blue-50': 'dark:bg-blue-900/20',
    'bg-yellow-50': 'dark:bg-yellow-900/20',
    'bg-indigo-50': 'dark:bg-indigo-900/20',
    'bg-purple-50': 'dark:bg-purple-900/20',
    
    # Text colors
    'text-gray-900': 'dark:text-gray-100',
    'text-gray-800': 'dark:text-gray-200',
    'text-gray-700': 'dark:text-gray-300',
    'text-gray-600': 'dark:text-gray-400',
    'text-gray-500': 'dark:text-gray-500',
    'text-gray-400': 'dark:text-gray-600',
    'text-black': 'dark:text-white',
    
    # Borders
    'border-gray-200': 'dark:border-gray-700',
    'border-gray-300': 'dark:border-gray-600',
    'border-gray-400': 'dark:border-gray-500',
    
    # Divide colors (for borders between elements)
    'divide-gray-200': 'dark:divide-gray-700',
    'divide-gray-300': 'dark:divide-gray-600',
    
    # Ring colors (for focus states)
    'ring-gray-200': 'dark:ring-gray-700',
    'ring-gray-300': 'dark:ring-gray-600',
    
    # Placeholder colors
    'placeholder-gray-400': 'dark:placeholder-gray-600',
    'placeholder-gray-500': 'dark:placeholder-gray-500',
}

# Hover state mappings
HOVER_MAPPINGS = {
    'hover:bg-gray-50': 'dark:hover:bg-gray-800',
    'hover:bg-gray-100': 'dark:hover:bg-gray-700',
    'hover:bg-gray-200': 'dark:hover:bg-gray-600',
    'hover:text-gray-900': 'dark:hover:text-gray-100',
    'hover:text-gray-800': 'dark:hover:text-gray-200',
    'hover:text-gray-700': 'dark:hover:text-gray-300',
    'hover:text-gray-600': 'dark:hover:text-gray-400',
    'hover:border-gray-300': 'dark:hover:border-gray-600',
    'hover:border-gray-400': 'dark:hover:border-gray-500',
}

# Focus state mappings
FOCUS_MAPPINGS = {
    'focus:border-indigo-500': 'dark:focus:border-indigo-400',
    'focus:ring-indigo-500': 'dark:focus:ring-indigo-400',
    'focus:bg-gray-50': 'dark:focus:bg-gray-800',
}

# Shadow adjustments for dark mode
SHADOW_MAPPINGS = {
    'shadow-sm': 'dark:shadow-lg dark:shadow-gray-900/30',
    'shadow': 'dark:shadow-xl dark:shadow-gray-900/30',
    'shadow-md': 'dark:shadow-xl dark:shadow-gray-900/40',
    'shadow-lg': 'dark:shadow-2xl dark:shadow-gray-900/50',
    'shadow-xl': 'dark:shadow-2xl dark:shadow-gray-900/60',
}

# Combine all mappings
ALL_MAPPINGS = {
    **COLOR_MAPPINGS,
    **HOVER_MAPPINGS,
    **FOCUS_MAPPINGS,
    **SHADOW_MAPPINGS,
}

class DarkModeApplicator:
    def __init__(self, args):
        self.args = args
        self.stats = {
            'files_processed': 0,
            'files_modified': 0,
            'classes_added': 0,
            'errors': [],
            'skipped': [],
        }
        
    def print_header(self):
        """Print script header"""
        print(f"\n{Colors.HEADER}🌙 Dark Mode Class Application Tool{Colors.ENDC}")
        print("=" * 50)
        print(f"Directory: {Colors.CYAN}{self.args.dir}{Colors.ENDC}")
        print(f"Mode: {Colors.WARNING if self.args.dry_run else Colors.GREEN}"
              f"{'DRY RUN' if self.args.dry_run else 'LIVE'}{Colors.ENDC}")
        print("=" * 50 + "\n")

    def find_vue_files(self) -> List[Path]:
        """Find all Vue files in the specified directory"""
        pattern = os.path.join(self.args.dir, '**/*.vue')
        files = glob.glob(pattern, recursive=True)
        
        # Filter out node_modules and backup files
        filtered_files = []
        for file in files:
            if 'node_modules' not in file and not file.endswith('.backup'):
                filtered_files.append(Path(file))
                
        return filtered_files

    def extract_template(self, content: str) -> Optional[Tuple[str, int, int]]:
        """Extract template section from Vue file content"""
        match = re.search(r'<template>(.*?)</template>', content, re.DOTALL)
        if match:
            return match.group(1), match.start(1), match.end(1)
        return None

    def apply_dark_classes(self, template: str) -> Tuple[str, int, Dict[str, int]]:
        """Apply dark mode classes to template content"""
        modified = False
        classes_added = 0
        changes = defaultdict(int)
        
        def replace_class(match):
            nonlocal modified, classes_added
            classes = match.group(1)
            class_list = classes.split()
            new_classes = []
            
            for class_name in class_list:
                if class_name in ALL_MAPPINGS:
                    dark_class = ALL_MAPPINGS[class_name]
                    # Check if dark class is not already present
                    if dark_class not in classes:
                        new_classes.append(dark_class)
                        changes[f"{class_name} → {dark_class}"] += 1
                        classes_added += 1
                        modified = True
            
            if new_classes:
                return f'class="{classes} {" ".join(new_classes)}"'
            return match.group(0)
        
        # Process class attributes
        template = re.sub(r'class="([^"]*)"', replace_class, template)
        
        return template, classes_added, changes

    def process_file(self, file_path: Path) -> bool:
        """Process a single Vue file"""
        if self.args.verbose:
            print(f"Processing: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract template section
            template_data = self.extract_template(content)
            if not template_data:
                if self.args.verbose:
                    print(f"  {Colors.WARNING}No template section found{Colors.ENDC}")
                self.stats['skipped'].append(str(file_path))
                return False
            
            template, start_pos, end_pos = template_data
            
            # Apply dark mode classes
            new_template, classes_added, changes = self.apply_dark_classes(template)
            
            if classes_added > 0:
                # Check for interactive mode
                if self.args.interactive:
                    print(f"\n{Colors.CYAN}{file_path}{Colors.ENDC}")
                    print(f"  Changes to apply ({classes_added} classes):")
                    for change, count in changes.items():
                        print(f"    {change} ({count}x)")
                    
                    response = input(f"  Apply changes? (y/n/s=skip): ").lower()
                    if response == 's':
                        self.stats['skipped'].append(str(file_path))
                        return False
                    elif response != 'y':
                        return False
                
                # Backup if requested
                if self.args.backup and not self.args.dry_run:
                    backup_path = f"{file_path}.backup"
                    shutil.copy2(file_path, backup_path)
                    if self.args.verbose:
                        print(f"  Created backup: {backup_path}")
                
                # Apply changes
                new_content = content[:start_pos] + new_template + content[end_pos:]
                
                if self.args.dry_run:
                    print(f"{Colors.YELLOW}Would modify:{Colors.ENDC} {file_path}")
                    print(f"  {Colors.GREEN}+ {classes_added} dark classes{Colors.ENDC}")
                    if self.args.verbose:
                        for change, count in changes.items():
                            print(f"    {change} ({count}x)")
                else:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"{Colors.GREEN}✓ Modified:{Colors.ENDC} {file_path} "
                          f"({classes_added} dark classes added)")
                
                self.stats['files_modified'] += 1
                self.stats['classes_added'] += classes_added
                return True
            
            elif self.args.verbose:
                print(f"  {Colors.BLUE}No changes needed{Colors.ENDC}")
            
            return False
            
        except Exception as e:
            error_msg = f"{file_path}: {str(e)}"
            self.stats['errors'].append(error_msg)
            print(f"{Colors.FAIL}✗ Error processing {file_path}: {e}{Colors.ENDC}")
            return False
        finally:
            self.stats['files_processed'] += 1

    def analyze_files(self, files: List[Path]):
        """Analyze files for dark mode readiness"""
        print(f"\n{Colors.HEADER}📊 Dark Mode Analysis Report{Colors.ENDC}")
        print("=" * 50)
        
        analysis = {
            'total_files': len(files),
            'files_with_dark': [],
            'files_without_dark': [],
            'class_frequency': defaultdict(int),
            'potential_changes': 0,
        }
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                has_dark = 'dark:' in content
                if has_dark:
                    analysis['files_with_dark'].append(file_path)
                else:
                    analysis['files_without_dark'].append(file_path)
                
                # Count potential classes
                for class_name in ALL_MAPPINGS.keys():
                    count = content.count(f'"{class_name}"') + content.count(f"'{class_name}'")
                    if count > 0:
                        analysis['class_frequency'][class_name] += count
                        analysis['potential_changes'] += count
                        
            except Exception as e:
                print(f"{Colors.FAIL}Error analyzing {file_path}: {e}{Colors.ENDC}")
        
        # Print analysis results
        print(f"\nTotal Vue files: {analysis['total_files']}")
        print(f"Files with dark mode classes: {Colors.GREEN}{len(analysis['files_with_dark'])}{Colors.ENDC}")
        print(f"Files without dark mode classes: {Colors.WARNING}{len(analysis['files_without_dark'])}{Colors.ENDC}")
        print(f"Potential dark classes to add: {Colors.CYAN}{analysis['potential_changes']}{Colors.ENDC}")
        
        if analysis['class_frequency']:
            print(f"\n{Colors.HEADER}Top 10 Classes Needing Dark Variants:{Colors.ENDC}")
            sorted_classes = sorted(analysis['class_frequency'].items(), 
                                   key=lambda x: x[1], reverse=True)[:10]
            for class_name, count in sorted_classes:
                dark_class = ALL_MAPPINGS.get(class_name, 'N/A')
                print(f"  {class_name}: {count}x → {Colors.CYAN}{dark_class}{Colors.ENDC}")
        
        if analysis['files_without_dark'] and len(analysis['files_without_dark']) <= 20:
            print(f"\n{Colors.HEADER}Files needing dark mode:{Colors.ENDC}")
            for file_path in analysis['files_without_dark'][:20]:
                print(f"  - {file_path}")

    def run(self):
        """Main execution"""
        self.print_header()
        
        # Find Vue files
        files = self.find_vue_files()
        print(f"Found {Colors.CYAN}{len(files)}{Colors.ENDC} Vue files\n")
        
        if not files:
            print(f"{Colors.WARNING}No Vue files found in {self.args.dir}{Colors.ENDC}")
            return
        
        # Analyze mode
        if self.args.analyze:
            self.analyze_files(files)
            return
        
        # Process files
        for file_path in files:
            self.process_file(file_path)
        
        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print processing summary"""
        print(f"\n{'=' * 50}")
        print(f"{Colors.HEADER}📊 Summary{Colors.ENDC}")
        print("=" * 50)
        print(f"Files processed: {self.stats['files_processed']}")
        print(f"Files modified: {Colors.GREEN}{self.stats['files_modified']}{Colors.ENDC}")
        print(f"Dark classes added: {Colors.CYAN}{self.stats['classes_added']}{Colors.ENDC}")
        
        if self.stats['skipped']:
            print(f"Files skipped: {Colors.WARNING}{len(self.stats['skipped'])}{Colors.ENDC}")
        
        if self.stats['errors']:
            print(f"\n{Colors.FAIL}⚠️ Errors: {len(self.stats['errors'])}{Colors.ENDC}")
            for error in self.stats['errors'][:5]:
                print(f"  - {error}")
        
        if self.args.dry_run:
            print(f"\n{Colors.WARNING}📝 This was a dry run. No files were modified.{Colors.ENDC}")
            print("Remove --dry-run flag to apply changes.")
        
        if self.args.backup and not self.args.dry_run and self.stats['files_modified'] > 0:
            print(f"\n{Colors.BLUE}💾 Backup files created with .backup extension{Colors.ENDC}")

def main():
    parser = argparse.ArgumentParser(
        description='Apply dark mode classes to Vue components',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--dir',
        default='{{cookiecutter.project_slug}}/frontend/src',
        help='Directory to process (default: {{cookiecutter.project_slug}}/frontend/src)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without modifying files'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed processing information'
    )
    parser.add_argument(
        '--backup',
        action='store_true',
        help='Create backup files before modifying'
    )
    parser.add_argument(
        '--analyze',
        action='store_true',
        help='Analyze files without making changes'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Prompt for confirmation on each file'
    )
    
    args = parser.parse_args()
    
    # Check if directory exists
    if not os.path.exists(args.dir):
        print(f"{Colors.FAIL}Error: Directory '{args.dir}' does not exist{Colors.ENDC}")
        sys.exit(1)
    
    # Run the applicator
    applicator = DarkModeApplicator(args)
    applicator.run()

if __name__ == '__main__':
    main()