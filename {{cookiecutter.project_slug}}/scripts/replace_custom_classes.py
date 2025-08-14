#!/usr/bin/env python3

"""
Script to replace custom CSS classes with TailwindCSS utilities
"""

import re
from pathlib import Path

# Mapping of custom classes to Tailwind classes
CLASS_MAPPINGS = {
    # Page structure
    'page-header': 'flex items-center justify-between mb-8',
    'page-title': 'text-3xl font-bold text-gray-900',
    'page-description': 'text-gray-600 mt-2',
    'header-actions': 'flex items-center gap-3',
    'header-left': 'flex-1',
    'back-link': 'inline-flex items-center gap-2 text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors',
    
    # Cards and sections
    'card': 'bg-white rounded-lg shadow-md p-6',
    'panel-content': 'space-y-6',
    'panel-title': 'text-2xl font-semibold text-gray-900 mb-4',
    'section-header': 'mb-6',
    'section-title': 'text-xl font-semibold text-gray-900 mb-2',
    'section-description': 'text-gray-600',
    'form-section': 'bg-white rounded-lg shadow-md p-6 mb-6',
    'form-sections': 'space-y-6',
    
    # Forms
    'form-grid': 'grid grid-cols-1 md:grid-cols-2 gap-6',
    'form-group': 'mb-6',
    'form-actions': 'flex justify-end gap-3 mt-8',
    'order-form': 'space-y-6',
    'profile-form': 'space-y-6',
    'auth-form': 'space-y-6',
    'full-width': 'md:col-span-2',
    
    # Stats and metrics
    'stats-grid': 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8',
    'stat-card': 'bg-white rounded-lg shadow-md p-6',
    'stat-icon': 'w-12 h-12 rounded-full flex items-center justify-center mb-4',
    'stat-content': 'space-y-1',
    'stat-label': 'text-sm font-medium text-gray-600',
    'stat-value': 'text-3xl font-bold text-gray-900',
    'metric-card': 'bg-white rounded-lg shadow-md p-6',
    'metric-value': 'text-3xl font-bold text-gray-900',
    'metric-label': 'text-sm font-medium text-gray-600 mb-2',
    'metric-comparison': 'text-sm text-gray-500',
    
    # Profile specific
    'profile-content': 'space-y-6',
    'profile-header': 'bg-white rounded-lg shadow-md p-8 mb-6',
    'profile-header-content': 'flex items-center gap-6',
    'profile-avatar': 'relative',
    'avatar-image': 'w-24 h-24 rounded-full object-cover',
    'avatar-placeholder': 'w-24 h-24 rounded-full bg-indigo-500 text-white flex items-center justify-center text-2xl font-bold',
    'avatar-change-btn': 'absolute bottom-0 right-0 p-2 bg-white rounded-full shadow-lg hover:bg-gray-50 transition-colors',
    'profile-info': 'flex-1',
    'profile-name': 'text-2xl font-bold text-gray-900',
    'profile-email': 'text-gray-600',
    'profile-role': 'inline-block mt-2 px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm font-medium',
    
    # Settings specific
    'settings-content': 'grid grid-cols-1 lg:grid-cols-4 gap-6',
    'settings-nav': 'lg:col-span-1',
    'settings-panel': 'lg:col-span-3',
    'nav-list': 'space-y-1',
    'nav-item': 'block px-4 py-2 text-sm font-medium rounded-lg transition-colors cursor-pointer',
    'settings-group': 'mb-8',
    'group-title': 'text-lg font-semibold text-gray-900 mb-4',
    'setting-item': 'flex items-center justify-between py-4 border-b border-gray-200 last:border-0',
    'setting-info': 'flex-1',
    'setting-description': 'text-sm text-gray-500 mt-1',
    'settings-actions': 'flex justify-end gap-3 mt-6',
    
    # Orders/tables
    'filters-section': 'flex gap-4 mb-6',
    'search-box': 'relative flex-1',
    'search-icon': 'absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400',
    'search-input': 'w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
    'filter-select': 'px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
    'orders-table': 'bg-white rounded-lg shadow-md overflow-hidden',
    'table-wrapper': 'overflow-x-auto',
    'table-header': 'bg-gray-50',
    'table-body': 'bg-white divide-y divide-gray-200',
    'table-card': 'bg-white rounded-lg shadow-md overflow-hidden',
    'table-title': 'text-lg font-semibold text-gray-900 p-6',
    'products-table': 'bg-white rounded-lg shadow-md p-6',
    
    # Order specific
    'order-header': 'flex items-center justify-between mb-2',
    'order-number': 'font-medium text-gray-900',
    'order-customer': 'text-sm text-gray-600',
    'order-date': 'text-sm text-gray-500',
    'order-total': 'font-semibold text-gray-900',
    'order-status': 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
    'payment-badge': 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
    'status-badge': 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
    'summary-grid': 'bg-gray-50 rounded-lg p-4 space-y-2',
    'summary-row': 'flex justify-between',
    'summary-label': 'text-gray-600',
    'summary-value': 'font-semibold text-gray-900',
    'product-total': 'font-semibold text-gray-900',
    
    # Charts
    'charts-grid': 'grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8',
    'chart-card': 'space-y-4',
    'chart-legend': 'flex gap-4 mt-2',
    'legend-item': 'flex items-center gap-2 text-sm text-gray-600',
    'legend-dot': 'w-3 h-3 rounded-full',
    'chart-tabs': 'flex gap-2 mt-2',
    'tab-btn': 'px-3 py-1 text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors',
    'traffic-legend': 'mt-4 space-y-2',
    'traffic-item': 'flex items-center justify-between',
    'traffic-info': 'flex items-center gap-2',
    'traffic-dot': 'w-3 h-3 rounded-full',
    'traffic-name': 'text-sm text-gray-600',
    'traffic-value': 'text-sm font-medium text-gray-900',
    
    # Modals
    'modal-overlay': 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50',
    'modal': 'bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto',
    'modal-header': 'flex items-center justify-between p-6 border-b border-gray-200',
    'modal-title': 'text-xl font-semibold text-gray-900',
    'modal-close': 'p-2 hover:bg-gray-100 rounded-lg transition-colors',
    'modal-body': 'p-6',
    'modal-footer': 'flex justify-end gap-3 p-6 border-t border-gray-200',
    
    # Actions and buttons
    'action-menu': 'relative',
    'action-btn': 'p-2 hover:bg-gray-100 rounded-lg transition-colors',
    'action-buttons': 'flex gap-2',
    'dropdown-menu': 'absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-10',
    'dropdown-item': 'flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors',
    'btn-icon': 'p-2 hover:bg-gray-100 rounded-lg transition-colors',
    'btn-text': 'text-sm font-medium text-indigo-600 hover:text-indigo-500 transition-colors',
    
    # User specific
    'filters-bar': 'flex gap-4 mb-6',
    'users-table': 'bg-white rounded-lg shadow-md overflow-hidden',
    'user-avatar': 'w-10 h-10 rounded-full',
    'user-info': 'flex items-center gap-3',
    'user-name': 'font-medium text-gray-900',
    'user-email': 'text-sm text-gray-500',
    
    # Analytics specific
    'period-selector': 'px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
    
    # Integration cards
    'integrations-grid': 'grid grid-cols-1 md:grid-cols-2 gap-6',
    'integration-card': 'bg-white rounded-lg shadow-md p-6',
    'integration-header': 'flex items-center justify-between mb-4',
    'integration-info': 'flex items-center gap-3',
    'integration-icon': 'w-12 h-12 rounded-lg flex items-center justify-center',
    'integration-details': 'flex-1',
    'integration-name': 'font-semibold text-gray-900',
    'integration-description': 'text-sm text-gray-600',
    'integration-status': 'flex items-center gap-2 text-sm',
    
    # Empty states
    'empty-state': 'text-center py-12',
    'empty-icon': 'w-16 h-16 mx-auto mb-4 text-gray-400',
    'empty-title': 'text-xl font-semibold text-gray-900 mb-2',
    'empty-message': 'text-gray-600',
    
    # Pagination
    'pagination': 'flex items-center justify-between mt-6',
    'pagination-info': 'text-sm text-gray-700',
    'pagination-controls': 'flex gap-2',
    'pagination-btn': 'px-3 py-1 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed',
}

def replace_classes_in_file(file_path):
    """Replace custom classes with Tailwind utilities in a file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = 0
    
    # Replace class attributes
    for old_class, new_class in CLASS_MAPPINGS.items():
        # Match exact class name
        pattern = rf'class="([^"]*\b{re.escape(old_class)}\b[^"]*)"'
        
        def replace_class(match):
            nonlocal changes
            full_class = match.group(1)
            # Replace the old class with new class
            new_full_class = full_class.replace(old_class, new_class)
            changes += 1
            return f'class="{new_full_class}"'
        
        content = re.sub(pattern, replace_class, content)
    
    # Write back if changes were made
    if changes > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Updated {file_path.name}: {changes} replacements")
    else:
        print(f"  No changes needed in {file_path.name}")
    
    return changes

def main():
    base_path = Path('/home/hmesfin/development/working-on/cookiecutter-djvue/{{cookiecutter.project_slug}}/frontend/src')
    
    # Process all Vue files
    vue_files = list(base_path.rglob('*.vue'))
    
    total_changes = 0
    for file_path in vue_files:
        if 'node_modules' not in str(file_path):
            changes = replace_classes_in_file(file_path)
            total_changes += changes
    
    print(f"\n✅ Total replacements: {total_changes}")

if __name__ == '__main__':
    main()