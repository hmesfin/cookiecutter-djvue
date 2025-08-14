#!/usr/bin/env python3

"""
Helper script to generate dark mode class mappings for dynamic Vue :class bindings
Usage: python scripts/dark_mode_helper.py "text-gray-900 hover:text-gray-700"

This will output the classes with their dark mode equivalents added.
"""

import sys
import re

# Import mappings from main script
from apply_dark_mode import ALL_MAPPINGS

def add_dark_classes(class_string):
    """Add dark mode classes to a class string"""
    classes = class_string.split()
    result_classes = []
    
    for cls in classes:
        result_classes.append(cls)
        if cls in ALL_MAPPINGS:
            dark_class = ALL_MAPPINGS[cls]
            if dark_class not in classes:
                result_classes.append(dark_class)
    
    return ' '.join(result_classes)

def process_ternary_expression(expression):
    """Process a ternary expression with class strings"""
    # Match ternary pattern: condition ? 'true_classes' : 'false_classes'
    pattern = r"([^?]+)\?\s*'([^']+)'\s*:\s*'([^']+)'"
    match = re.match(pattern, expression.strip())
    
    if match:
        condition = match.group(1).strip()
        true_classes = match.group(2)
        false_classes = match.group(3)
        
        true_with_dark = add_dark_classes(true_classes)
        false_with_dark = add_dark_classes(false_classes)
        
        return f"{condition}\n  ? '{true_with_dark}'\n  : '{false_with_dark}'"
    
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python dark_mode_helper.py \"class-string\"")
        print("   or: python dark_mode_helper.py --ternary \"condition ? 'true' : 'false'\"")
        sys.exit(1)
    
    if sys.argv[1] == '--ternary' and len(sys.argv) > 2:
        expression = ' '.join(sys.argv[2:])
        result = process_ternary_expression(expression)
        if result:
            print("\nUpdated expression:")
            print(result)
        else:
            print("Could not parse ternary expression")
    else:
        class_string = ' '.join(sys.argv[1:])
        result = add_dark_classes(class_string)
        print(f"\nOriginal: {class_string}")
        print(f"With dark: {result}")
        
        # Show what was added
        original = set(class_string.split())
        updated = set(result.split())
        added = updated - original
        if added:
            print(f"\nAdded dark classes:")
            for cls in sorted(added):
                print(f"  + {cls}")

if __name__ == '__main__':
    main()