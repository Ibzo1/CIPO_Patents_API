import os
import csv
import zipfile
import logging
from django.core.management.base import BaseCommand
from trademarks.models import TM_Mark_Description
from django.db import transaction

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Command(BaseCommand):
    help = "Import TM_Mark_Description data from a ZIP file containing a CSV."

    ZIP_FILE_PATH = "C:/Users/Intern_1/Documents/TM_Data/TM_mark_description.zip"
    TEMP_EXTRACT_DIR = "C:/Users/Intern_1/Documents/TM_Data/temp_extracted/"

    def handle(self, *args, **options):
        logging.info(f"ZIP File Path: {self.ZIP_FILE_PATH}")
        logging.info(f"Temporary Extract Directory: {self.TEMP_EXTRACT_DIR}")

        os.makedirs(self.TEMP_EXTRACT_DIR, exist_ok=True)
        zip_filename = os.path.basename(self.ZIP_FILE_PATH)

        logging.info(f"Starting processing for ZIP file: {zip_filename}")
        try:
            with zipfile.ZipFile(self.ZIP_FILE_PATH, 'r') as zip_ref:
                zip_ref.extractall(self.TEMP_EXTRACT_DIR)
            logging.info(f"Extracted '{zip_filename}' to '{self.TEMP_EXTRACT_DIR}'.")
        except Exception as e:
            logging.error(f"Failed to extract '{zip_filename}': {e}")
            return

        csv_files = [f for f in os.listdir(self.TEMP_EXTRACT_DIR) if f.lower().endswith('.csv')]
        if not csv_files:
            logging.error("No CSV files found in the extracted directory.")
            return

        csv_path = os.path.join(self.TEMP_EXTRACT_DIR, csv_files[0])
        logging.info(f"Processing CSV file: {csv_files[0]}")
        self.process_csv(csv_path)

        os.remove(csv_path)
        logging.info(f"Deleted temporary file: {csv_path}")

    def process_csv(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='|')
            total_rows = sum(1 for _ in open(file_path, 'r', encoding='utf-8')) - 1
            csvfile.seek(0)
            logging.info(f"Processing '{file_path}' with {total_rows} rows.")

            entries = []
            for row in reader:
                cleaned = self.clean_row(row)
                if cleaned:
                    entries.append(TM_Mark_Description(**cleaned))
            TM_Mark_Description.objects.bulk_create(entries, ignore_conflicts=True)
            logging.info(f"Inserted {len(entries)} records.")

    def clean_row(self, row):
        cleaned = {}
        # Use row.get with the exact header including trailing space if present.
        app_num = row.get("Application Number - Numéro de la demande ", "").strip()
        lang_code = row.get("Language Code - Code de la langue", "").strip()
        mark_desc = row.get("Mark Description - Description de la marque", "").strip()

        if not app_num or not lang_code or not mark_desc:
            logging.warning("Missing one of the required fields; skipping row.")
            return None

        try:
            cleaned["application_number"] = int(app_num)
        except ValueError:
            logging.warning(f"Invalid application number: {app_num}")
            return None

        cleaned["language_code"] = lang_code
        cleaned["mark_description"] = mark_desc
        return cleaned
