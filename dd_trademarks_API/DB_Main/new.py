import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DB_Main.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    print(f"DJANGO_SETTINGS_MODULE is set to: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
