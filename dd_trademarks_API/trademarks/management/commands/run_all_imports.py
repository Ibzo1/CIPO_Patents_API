import os
import subprocess
import sys
import logging

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_script(script_name):
    """
    Executes a given Python script using the same interpreter and waits for it to complete.
    """
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    if not os.path.exists(script_path):
        logging.warning(f"Script not found, skipping: {script_path}")
        return

    logging.info("="*20 + f" RUNNING SCRIPT: {script_name} " + "="*20)
    try:
        # Use sys.executable to ensure the same Python interpreter is used
        result = subprocess.run(
            [sys.executable, script_path], 
            check=True, 
            capture_output=True, 
            text=True,
            encoding='utf-8' # Explicitly set encoding
        )
        logging.info(f"Successfully executed {script_name}.")
        # Print the stdout from the script to see its logging messages
        if result.stdout:
            print(result.stdout)
        # Print any errors that might not have caused a crash
        if result.stderr:
            logging.warning(f"Stderr from {script_name}:\n{result.stderr}")

    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing {script_name}:")
        logging.error(f"Return Code: {e.returncode}")
        logging.error(f"STDOUT:\n{e.stdout}")
        logging.error(f"STDERR:\n{e.stderr}")
        # Stop the entire process if one script fails
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred while trying to run {script_name}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Define the scripts in the correct order of execution to respect database dependencies.
    # Parent tables must be loaded before their children.
    scripts_to_run = [
        # --- LEVEL 0 (No Dependencies) ---
        'import_tm_main.py',
        
        # --- LEVEL 1 (Depend on tm_main) ---
        'import_tm_mark_description.py',
        'import_tm_cipo_classifications.py',
        'import_tm_applicant_classifications.py',
        'import_tm_representation.py',
        'import_tm_claim.py',
        'import_tm_priority_claim.py',
        'import_tm_event.py',
        'import_tm_footnote.py',
        'import_tm_footnote_formatted.py',
        'import_tm_interested_party.py',
        'import_tm_cancellation_case.py',
        'import_tm_opposition_case.py',
        'import_tm_transliteration.py',
        'import_tm_application_text.py',
        'import_tm_application_disclaimer.py',
        'import_tm_heading.py',
        
        # --- LEVEL 2 (Depend on other child tables) ---
        'import_tm_cancellation_case_action.py',
        'import_tm_opposition_case_action.py'
    ]

    for script in scripts_to_run:
        run_script(script)

    logging.info("="*20 + " ALL SCRIPTS EXECUTED SUCCESSFULLY " + "="*20)