#!/usr/bin/env python
"""
Pre-generation hook for cookiecutter-djvue.
Validates inputs and sets up necessary variables.
"""
import re
import sys


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'


def validate_project_slug():
    """Validate project_slug is a valid Python module name."""
    project_slug = '{{ cookiecutter.project_slug }}'
    if not re.match(MODULE_REGEX, project_slug):
        print(f'ERROR: The project slug ({project_slug}) is not a valid Python module name.')
        print('Please use only letters, numbers, and underscores.')
        sys.exit(1)


def validate_python_version():
    """Validate Python version is supported."""
    python_version = '{{ cookiecutter.python_version }}'
    try:
        major, minor = python_version.split('.')
        major, minor = int(major), int(minor)
        if major < 3 or (major == 3 and minor < 8):
            print(f'ERROR: Python version {python_version} is not supported.')
            print('Please use Python 3.8 or higher.')
            sys.exit(1)
    except (ValueError, AttributeError):
        print(f'ERROR: Invalid Python version format: {python_version}')
        print('Please use format like "3.12"')
        sys.exit(1)


def validate_email():
    """Validate email format."""
    email = '{{ cookiecutter.author_email }}'
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        print(f'WARNING: The email address ({email}) might not be valid.')
        print('Please make sure to update it if needed.')


def main():
    """Run all pre-generation hooks."""
    validate_project_slug()
    validate_python_version()
    validate_email()
    
    print('Pre-generation checks passed!')
    print(f'Creating project: {{ cookiecutter.project_name }}')
    print(f'Project slug: {{ cookiecutter.project_slug }}')
    print(f'Author: {{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>')
    print('')


if __name__ == '__main__':
    main()