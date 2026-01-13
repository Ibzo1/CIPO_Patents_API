import os
import csv
import sys
import zipfile
import logging
from django.core.management.base import BaseCommand

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Command(BaseCommand):
    help = "Analyze TM_Opposition_Case_Action CSV by printing first 30 rows without inserting."

    ZIP_FILE_PATH = "C:/Users/Intern_1/Documents/TM_Data/TM_opposition_case_action_2024-11-20.zip"
    TEMP_EXTRACT_DIR = "C:/Users/Intern_1/Documents/TM_Data/temp_extracted/"

    def handle(self, *args, **options):
        logging.info(f"ZIP File Path: {self.ZIP_FILE_PATH}")
        logging.info(f"Temporary Extract Directory: {self.TEMP_EXTRACT_DIR}")

        # 1) Create temp dir if needed
        os.makedirs(self.TEMP_EXTRACT_DIR, exist_ok=True)

        zip_filename = os.path.basename(self.ZIP_FILE_PATH)
        logging.info(f"Extracting ZIP file: {zip_filename}")

        # 2) Extract ZIP
        try:
            with zipfile.ZipFile(self.ZIP_FILE_PATH, "r") as zip_ref:
                zip_ref.extractall(self.TEMP_EXTRACT_DIR)
            logging.info(f"Extracted '{zip_filename}' into '{self.TEMP_EXTRACT_DIR}'.")
        except Exception as e:
            logging.error(f"Failed extracting '{zip_filename}': {e}")
            return

        # 3) Locate CSV
        csv_files = [f for f in os.listdir(self.TEMP_EXTRACT_DIR) if f.lower().endswith(".csv")]
        if not csv_files:
            logging.error("No CSV files found after extraction.")
            return

        csv_path = os.path.join(self.TEMP_EXTRACT_DIR, csv_files[0])
        logging.info(f"Found CSV: {csv_files[0]}")

        # 4) Print the first 30 rows
        self.analyze_csv(csv_path)

        # 5) Clean up extracted CSV (if you want to keep it, remove this line)
        os.remove(csv_path)
        logging.info(f"Deleted CSV file: {csv_path}")

    def analyze_csv(self, file_path):
        logging.info(f"Analyzing first 30 rows in '{file_path}'...")
        with open(file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter="|")
            
            for i, row in enumerate(reader, start=1):
                # Print row number and the raw data
                print(f"\n=== ROW {i} ===")
                for k, v in row.items():
                    print(f"{k!r}: {v!r}")

                if i >= 30:
                    break
