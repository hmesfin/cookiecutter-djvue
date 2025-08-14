#!/usr/bin/env python3
"""
Update all dashboard views to use the PageHeader component
"""

import os
import re

def update_component_with_page_header(file_path):
    """Update a Vue component to use PageHeader instead of inline headers"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Extract component name from file path
    component_name = os.path.basename(file_path).replace('.vue', '')
    
    # Define the header patterns and replacements for each component
    replacements = {
        'AnalyticsView': {
            'title': 'Analytics Dashboard',
            'description': 'Track performance metrics and user engagement',
            'pattern': r'<div class="flex items-center justify-between mb-8">.*?</div>\s*</div>',
            'has_actions': False
        },
        'ProfileView': {
            'title': 'Profile Settings',
            'description': 'Manage your personal information and preferences',
            'pattern': r'<div class="flex items-center justify-between mb-8">.*?</div>',
            'has_actions': False
        },
        'SettingsView': {
            'title': 'Settings',
            'description': 'Configure your account and application preferences',
            'pattern': r'<div class="flex items-center justify-between mb-8">.*?</div>',
            'has_actions': False
        },
        'OrdersView': {
            'title': 'Orders',
            'description': 'Manage and track all customer orders',
            'pattern': r'<div class="flex items-center justify-between mb-8">.*?</button>\s*</div>',
            'has_actions': True,
            'action_content': '''<button @click="router.push('/dashboard/orders/new')" class="px-4 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
        </svg>
        New Order
      </button>'''
        },
        'NewOrderView': {
            'title': 'Create New Order',
            'description': '',
            'pattern': r'<div class="flex items-center justify-between mb-8">.*?</div>\s*</div>',
            'has_back': True,
            'back_link': '/dashboard/orders',
            'back_text': 'Back to Orders',
            'has_actions': False
        },
        'UsersView': {
            'title': 'Users',
            'description': 'Manage user accounts and permissions',
            'pattern': r'<div class="flex items-center justify-between mb-8">.*?</button>\s*</div>',
            'has_actions': True,
            'action_content': '''<button @click="showAddUserModal = true" class="px-4 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
        </svg>
        Add User
      </button>'''
        }
    }
    
    if component_name not in replacements:
        return 0
    
    config = replacements[component_name]
    
    # Build the PageHeader component usage
    page_header_props = []
    page_header_props.append(f'title="{config["title"]}"')
    
    if config.get('description'):
        page_header_props.append(f'description="{config["description"]}"')
    
    if config.get('has_back'):
        page_header_props.append(':show-back="true"')
        page_header_props.append(f'back-link="{config["back_link"]}"')
        page_header_props.append(f'back-text="{config["back_text"]}"')
    
    page_header = f'    <PageHeader\n      {" ".join(page_header_props)}\n    '
    
    if config.get('has_actions'):
        page_header += '>\n      <template #actions>\n      ' + config['action_content'] + '\n      </template>\n    </PageHeader>'
    else:
        page_header += '/>'
    
    # Replace the header pattern
    pattern = config['pattern']
    content = re.sub(pattern, page_header, content, flags=re.DOTALL)
    
    # Add PageHeader import if not present
    if 'PageHeader' not in content:
        # Check if there are existing imports
        import_match = re.search(r"(import .+ from '@/[^']+'\n)", content)
        if import_match:
            # Add after the last import
            import_statement = "import PageHeader from '@/components/PageHeader.vue'\n"
            content = content.replace(import_match.group(0), import_match.group(0) + import_statement)
        else:
            # Add at the beginning of script section
            script_match = re.search(r'(<script[^>]*>)', content)
            if script_match:
                import_statement = "\nimport PageHeader from '@/components/PageHeader.vue'\n"
                content = content.replace(script_match.group(0), script_match.group(0) + import_statement)
    
    if content != original_content:
        with open(file_path, 'w') as f:
            f.write(content)
        return 1
    return 0

def main():
    base_dir = '/home/hmesfin/development/working-on/cookiecutter-djvue/{{cookiecutter.project_slug}}/frontend/src'
    
    # Dashboard views to update
    dashboard_views = [
        'modules/dashboard/views/AnalyticsView.vue',
        'modules/dashboard/views/ProfileView.vue', 
        'modules/dashboard/views/SettingsView.vue',
        'modules/dashboard/views/OrdersView.vue',
        'modules/dashboard/views/NewOrderView.vue',
        'modules/dashboard/views/UsersView.vue'
    ]
    
    total_updated = 0
    
    for view_path in dashboard_views:
        full_path = os.path.join(base_dir, view_path)
        if os.path.exists(full_path):
            updated = update_component_with_page_header(full_path)
            if updated:
                print(f"✓ Updated {view_path}")
                total_updated += 1
            else:
                print(f"  No changes needed for {view_path}")
        else:
            print(f"✗ File not found: {view_path}")
    
    print(f"\nTotal components updated: {total_updated}")

if __name__ == '__main__':
    main()