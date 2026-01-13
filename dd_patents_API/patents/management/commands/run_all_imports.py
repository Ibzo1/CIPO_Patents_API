# import os
# import subprocess
# import sys

# def run_script(script_path):
#     try:
#         # Use the same Python executable as the current script
#         result = subprocess.run([sys.executable, script_path], check=True, capture_output=True, text=True)
#         print(f"Output of {script_path}:")
#         print(result.stdout)
#     except subprocess.CalledProcessError as e:
#         print(f"Error executing {script_path}:")
#         print(e.stderr)

# # Set the directory where your scripts are located
# scripts_dir = 'C:\\Users\\azhari\\Desktop\\DB_Main\\patents\\management\\commands\\'

# # List of script filenames
# scripts = [
#     'import_abstracts.py',
#     'import_claims.py',
#     'import_disclosures.py',
#     'import_interested_party.py',
#     'import_ipc.py',
#     'import_main.py',
#     'import_priority_claims.py'
# ]

# # Run each script by constructing the full path
# for script in scripts:
#     script_path = os.path.join(scripts_dir, script)
#     if os.path.exists(script_path):
#         print(f"Running script: {script_path}")
#         run_script(script_path)
#     else:
#         print(f"Script not found: {script_path}")
from django.core.management.base import BaseCommand
import os
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Runs all import scripts in the patents/management/commands directory.'

    def handle(self, *args, **kwargs):
        # List of scripts you want to run
        scripts = [
            'import_abstracts',
            'import_claims',
            'import_disclosures',
            'import_interested_party',
            'import_ipc',
            'import_main',
            'import_priority_claims',
        ]

        # Iterate through each script and call it using call_command
        for script in scripts:
            script_path = f'patents/management/commands/{script}.py'
            if os.path.exists(script_path):
                self.stdout.write(self.style.SUCCESS(f'Running script: {script}'))
                try:
                    call_command(script)
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f'Error running script {script}: {str(e)}'))
            else:
                self.stderr.write(self.style.WARNING(f'Script not found: {script_path}'))

        self.stdout.write(self.style.SUCCESS('All scripts executed.'))
