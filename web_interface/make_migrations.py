#!/usr/bin/env python3
"""
Script to create migrations for the new models.

This script should be run from the web_interface directory.
"""

import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ancestors_web.settings')
django.setup()

# Import Django's management module
from django.core.management import call_command

def main():
    """Create migrations for the accounts and dashboard apps."""
    print("Creating migrations for accounts app...")
    call_command('makemigrations', 'accounts')
    
    print("Creating migrations for dashboard app...")
    call_command('makemigrations', 'dashboard')
    
    print("Migrations created successfully.")
    print("To apply migrations, run: python manage.py migrate")

if __name__ == "__main__":
    main()