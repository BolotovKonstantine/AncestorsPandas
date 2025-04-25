#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def main():
    """Run administrative tasks."""
    # Add the parent directory to the Python path
    parent_dir = str(Path(__file__).resolve().parent.parent)
    sys.path.insert(0, parent_dir)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ancestors_web.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
