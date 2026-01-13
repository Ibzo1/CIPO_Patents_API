import os
import sys
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Run the Django application.")
    parser.add_argument('--dev', action='store_true', help="Run in development mode (Django runserver)")
    parser.add_argument('--prod', action='store_true', help="Run in production mode (Waitress)")
    parser.add_argument('--migrate', action='store_true', help="Run database migrations")
    
    args = parser.parse_args()
    
    port = os.getenv('PORT', '8082')
    
    if args.dev:
        print(f"Starting Development Server on port {port}...")
        os.system(f"python manage.py runserver 0.0.0.0:{port}")
    elif args.prod:
        print(f"Starting Production Server (Waitress) on port {port}...")
        # Ensure the correct WSGI application is targeted
        os.system(f"waitress-serve --listen=127.0.0.1:{port} DB_Main.wsgi:application")
    elif args.migrate:
        print("Running Database Migrations...")
        os.system("python manage.py migrate")
    else:
        print("Please specify a mode: --dev, --prod, or --migrate")
        sys.exit(1)

if __name__ == "__main__":
    main()
