#!/usr/bin/env python3
"""
Script to convert CSS classes to TailwindCSS in Vue components.
This handles the home module views that are using custom CSS.
"""

import re
import os
from pathlib import Path

# CSS to TailwindCSS class mappings
CSS_TO_TAILWIND = {
    # Container and layout
    'container': 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8',
    'hero-section': 'bg-gradient-to-br from-indigo-500 to-purple-600 text-white py-20',
    'hero-content': 'text-center max-w-4xl mx-auto',
    'hero-title': 'text-5xl font-bold mb-4',
    'hero-description': 'text-xl opacity-95',
    
    # Mission section
    'mission-section': 'py-20 bg-white dark:bg-gray-900',
    'mission-grid': 'grid grid-cols-1 lg:grid-cols-2 gap-16 items-center',
    'mission-content': 'space-y-6',
    'mission-text': 'text-gray-600 dark:text-gray-400 leading-relaxed',
    'mission-image': 'flex justify-center',
    'image-placeholder': 'w-64 h-64 bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center',
    
    # Values section
    'values-section': 'py-20 bg-gray-50 dark:bg-gray-800',
    'section-header': 'text-center mb-12',
    'section-title': 'text-4xl font-bold text-gray-900 dark:text-gray-100 mb-4',
    'section-description': 'text-xl text-gray-600 dark:text-gray-400',
    'values-grid': 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8',
    'value-card': 'bg-white dark:bg-gray-800 rounded-lg shadow-md p-6',
    'value-icon': 'w-16 h-16 rounded-full flex items-center justify-center text-white mb-4',
    'value-title': 'text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2',
    'value-description': 'text-gray-600 dark:text-gray-400',
    
    # Team section
    'team-section': 'py-20 bg-white dark:bg-gray-900',
    'team-grid': 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8',
    'team-member': 'text-center',
    'member-avatar': 'w-32 h-32 rounded-full mx-auto mb-4 bg-gray-200 dark:bg-gray-700',
    'member-name': 'text-lg font-semibold text-gray-900 dark:text-gray-100',
    'member-role': 'text-sm text-gray-600 dark:text-gray-400 mb-3',
    'member-social': 'flex justify-center gap-3',
    'social-link': 'text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors',
    'social-icon': 'w-5 h-5',
    
    # CTA section
    'cta-section': 'py-20 bg-gradient-to-br from-indigo-500 to-purple-600 text-white text-center',
    'cta-content': 'max-w-3xl mx-auto',
    'cta-title': 'text-4xl font-bold mb-4',
    'cta-description': 'text-xl mb-8 opacity-95',
    'cta-buttons': 'flex gap-4 justify-center',
    
    # Features section
    'features-section': 'py-20 bg-white dark:bg-gray-900',
    'features-grid': 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8',
    'feature-card': 'bg-white dark:bg-gray-800 rounded-lg shadow-md p-6',
    'feature-icon': 'w-16 h-16 rounded-full flex items-center justify-center text-white mb-4',
    'feature-title': 'text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2',
    'feature-description': 'text-gray-600 dark:text-gray-400',
    
    # Comparison section
    'comparison-section': 'py-20 bg-gray-50 dark:bg-gray-800',
    'comparison-table': 'bg-white dark:bg-gray-900 rounded-lg shadow-lg overflow-hidden',
    
    # Tech stack section
    'tech-section': 'py-20 bg-white dark:bg-gray-900',
    'tech-grid': 'grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8',
    'tech-item': 'text-center',
    'tech-logo': 'w-20 h-20 mx-auto mb-3 rounded-lg bg-gray-100 dark:bg-gray-800 flex items-center justify-center',
    'tech-name': 'text-sm font-medium text-gray-700 dark:text-gray-300',
    'tech-description': 'text-xs text-gray-500 dark:text-gray-500',
    
    # Pricing section
    'pricing-section': 'py-0 pb-20 -mt-12',
    'pricing-grid': 'grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-6xl mx-auto',
    'pricing-card': 'bg-white dark:bg-gray-800 rounded-lg shadow-md p-6',
    'featured-badge': 'absolute -top-px left-1/2 transform -translate-x-1/2 bg-gradient-to-r from-indigo-500 to-purple-600 text-white px-6 py-1 rounded-b-lg text-sm font-semibold',
    'plan-header': 'text-center mb-8',
    'plan-name': 'text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2',
    'plan-description': 'text-gray-600 dark:text-gray-400 text-sm',
    'plan-price': 'text-center mb-2',
    'currency': 'text-2xl text-gray-600 dark:text-gray-400 align-top',
    'amount': 'text-6xl font-bold text-gray-900 dark:text-gray-100',
    'period': 'text-lg text-gray-600 dark:text-gray-400',
    'savings': 'text-center text-green-600 dark:text-green-400 text-sm font-semibold mb-8',
    'features-list': 'space-y-3 mb-8',
    'feature-item': 'flex items-start gap-3 text-gray-600 dark:text-gray-400',
    'check-icon': 'w-5 h-5 text-green-500 flex-shrink-0 mt-0.5',
    
    # Enterprise section
    'enterprise-section': 'py-20 bg-gray-50 dark:bg-gray-800',
    'enterprise-card': 'bg-white dark:bg-gray-800 rounded-lg shadow-md p-6',
    'enterprise-content': 'lg:col-span-2',
    'enterprise-title': 'text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4',
    'enterprise-description': 'text-gray-600 dark:text-gray-400 mb-6 leading-relaxed',
    'enterprise-features': 'grid grid-cols-1 md:grid-cols-2 gap-3 text-gray-600 dark:text-gray-400',
    'enterprise-action': 'text-center',
    'enterprise-note': 'mt-3 text-gray-600 dark:text-gray-400 text-sm',
    
    # FAQ section
    'faq-section': 'py-20 bg-white dark:bg-gray-900',
    'faq-grid': 'max-w-3xl mx-auto',
    'faq-item': 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg mb-4 overflow-hidden transition-shadow hover:shadow-md cursor-pointer',
    'faq-question': 'p-5 flex justify-between items-center',
    'faq-answer': 'px-5 pb-5 text-gray-600 dark:text-gray-400 leading-relaxed',
    'chevron-icon': 'w-5 h-5 text-gray-600 dark:text-gray-400 transition-transform',
    
    # Guarantee section
    'guarantee-section': 'py-20 bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20',
    'guarantee-content': 'text-center max-w-2xl mx-auto',
    'guarantee-icon': 'w-20 h-20 mx-auto mb-6 bg-white dark:bg-gray-800 rounded-full flex items-center justify-center shadow-md',
    'guarantee-title': 'text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4',
    'guarantee-description': 'text-gray-600 dark:text-gray-400 text-lg leading-relaxed',
    
    # Contact section
    'contact-section': 'py-20 bg-white dark:bg-gray-900',
    'contact-grid': 'grid grid-cols-1 lg:grid-cols-2 gap-12',
    'contact-form': 'bg-white dark:bg-gray-800 rounded-lg shadow-md p-8',
    'form-header': 'mb-8',
    'form-title': 'text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2',
    'form-description': 'text-gray-600 dark:text-gray-400',
    'form-row': 'grid grid-cols-1 md:grid-cols-2 gap-6',
    'form-group': 'mb-6',
    'form-input': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400 focus:border-indigo-500 dark:focus:border-indigo-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100',
    'checkbox-label': 'flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400',
    'form-actions': 'flex gap-4',
    'contact-info': 'space-y-8',
    'info-section': 'bg-white dark:bg-gray-800 rounded-lg shadow-md p-8',
    'info-title': 'text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4',
    'info-content': 'space-y-4',
    'info-item': 'flex items-start gap-3',
    'info-icon': 'w-6 h-6 text-indigo-600 dark:text-indigo-400 flex-shrink-0',
    'info-text': 'text-gray-600 dark:text-gray-400',
    'social-section': 'bg-white dark:bg-gray-800 rounded-lg shadow-md p-8',
    'social-title': 'text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4',
    'social-description': 'text-gray-600 dark:text-gray-400 mb-6',
    'social-links': 'flex gap-4',
    
    # Map section
    'map-section': 'py-20 bg-gray-50 dark:bg-gray-800',
    'map-container': 'h-96 bg-gray-200 dark:bg-gray-700 rounded-lg relative overflow-hidden',
    'map-placeholder': 'absolute inset-0 flex items-center justify-center',
    'map-overlay': 'absolute inset-0 bg-black bg-opacity-20 flex items-center justify-center',
    'map-content': 'text-center text-white',
    'map-icon': 'w-16 h-16 mx-auto mb-4',
    
    # Buttons
    'btn': 'px-6 py-3 rounded-lg font-medium transition-all duration-200',
    'btn-primary': 'bg-indigo-600 text-white hover:bg-indigo-700',
    'btn-secondary': 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600',
    'btn-outline': 'border-2 border-indigo-600 text-indigo-600 hover:bg-indigo-600 hover:text-white dark:border-indigo-400 dark:text-indigo-400 dark:hover:bg-indigo-400 dark:hover:text-gray-900',
    'btn-white': 'bg-white text-indigo-600 hover:bg-gray-100',
    'btn-lg': 'px-8 py-4 text-lg',
    'btn-block': 'w-full',
    
    # Utilities
    'mb-6': 'mb-6',
    'text-center': 'text-center',
    'error-message': 'text-red-500 text-sm mt-1',
    'success-message': 'text-green-500 text-sm mt-1',
}

def convert_template_classes(template_content):
    """Convert CSS classes in template to TailwindCSS."""
    for css_class, tailwind_classes in CSS_TO_TAILWIND.items():
        # Replace class="css-class" with class="tailwind-classes"
        template_content = re.sub(
            f'class="([^"]*){css_class}([^"]*)"',
            lambda m: f'class="{m.group(1)}{tailwind_classes}{m.group(2)}"',
            template_content
        )
        # Also handle :class bindings
        template_content = re.sub(
            f':class="([^"]*){css_class}([^"]*)"',
            lambda m: f':class="{m.group(1)}{tailwind_classes}{m.group(2)}"',
            template_content
        )
    
    return template_content

def remove_style_section(content):
    """Remove the <style> section from the component."""
    # Find and remove the style section
    style_pattern = r'<style[^>]*>.*?</style>\s*'
    content = re.sub(style_pattern, '', content, flags=re.DOTALL)
    return content

def process_vue_file(file_path):
    """Process a single Vue file to convert CSS to TailwindCSS."""
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file has <style> section
    if '<style' not in content:
        print(f"  No style section found, skipping")
        return False
    
    # Convert template classes
    original_content = content
    content = convert_template_classes(content)
    
    # Remove style section
    content = remove_style_section(content)
    
    # Clean up any duplicate spaces in classes
    content = re.sub(r'class="([^"]*)\s+([^"]*)"', lambda m: f'class="{" ".join(m.group(0).split())}"', content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Converted to TailwindCSS")
        return True
    
    print(f"  No changes needed")
    return False

def main():
    """Main function to convert all home module views."""
    # Get the project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Files to convert (home module views)
    views_to_convert = [
        '{{cookiecutter.project_slug}}/frontend/src/modules/home/views/AboutView.vue',
        '{{cookiecutter.project_slug}}/frontend/src/modules/home/views/FeaturesView.vue',
        '{{cookiecutter.project_slug}}/frontend/src/modules/home/views/PricingView.vue',
        '{{cookiecutter.project_slug}}/frontend/src/modules/home/views/ContactView.vue',
        '{{cookiecutter.project_slug}}/frontend/src/modules/home/views/TermsView.vue',
        '{{cookiecutter.project_slug}}/frontend/src/modules/home/views/PrivacyView.vue',
    ]
    
    converted_count = 0
    
    for view_path in views_to_convert:
        full_path = project_root / view_path
        if full_path.exists():
            if process_vue_file(full_path):
                converted_count += 1
        else:
            print(f"File not found: {full_path}")
    
    print(f"\n✨ Conversion complete! Converted {converted_count} files to TailwindCSS.")
    print("\nNote: Please review the converted files to ensure all styles are properly applied.")
    print("Some complex CSS patterns may need manual adjustment.")

if __name__ == '__main__':
    main()