#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_voting.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
from pyngrok import ngrok

if __name__ == "__main__":
    # Start ngrok tunnel
    public_url = ngrok.connect(8000).public_url
    print(f"ngrok tunnel available at: {public_url}")

    # Add to ALLOWED_HOSTS dynamically
    from django.conf import settings
    settings.ALLOWED_HOSTS.append(public_url.split("//")[1])

    # Run Django server
    execute_from_command_line(sys.argv)
