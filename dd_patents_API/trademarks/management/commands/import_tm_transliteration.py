import os
import csv
import sys
import zipfile
import logging
from django.core.management.base import BaseCommand
from trademarks.models import TM_Transliteration
from django.db import transaction
from django.core.exceptions import FieldDoesNotExist

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Increase field size limit for very large CSV fields
import csv
max_int = sys.maxsize
while True:
    # Decrease max_int until csv.field_size_limit(max_int) works
    try:
        csv.field_size_limit(max_int)
        break
    except OverflowError:
        max_int = int(max_int / 10)

BATCH_SIZE = 1000

class Command(BaseCommand):
    help = "Import TM_Transliteration data from a ZIP file containing a CSV."

    # Adjust paths as needed
    ZIP_FILE_PATH = "C:/Users/Intern_1/Documents/TM_Data/TM_transliteration_2024-11-20.zip"
    TEMP_EXTRACT_DIR = "C:/Users/Intern_1/Documents/TM_Data/temp_extracted/"

    # CSV headers -> model field mapping
    CSV_TO_MODEL_MAP = {
        "Application Number - Numéro de la demande": "application_number",
        "Mark Transliteration Text - Translittération de la marque": "mark_transliteration_text",
    }

    def handle(self, *args, **options):
        logging.info(f"ZIP File Path: {self.ZIP_FILE_PATH}")
        logging.info(f"Temp Extract Dir: {self.TEMP_EXTRACT_DIR}")

        os.makedirs(self.TEMP_EXTRACT_DIR, exist_ok=True)
        zip_filename = os.path.basename(self.ZIP_FILE_PATH)
        logging.info(f"Starting processing for ZIP file: {zip_filename}")

        # Extract ZIP
        try:
            with zipfile.ZipFile(self.ZIP_FILE_PATH, 'r') as zip_ref:
                zip_ref.extractall(self.TEMP_EXTRACT_DIR)
            logging.info(f"Extracted '{zip_filename}' to '{self.TEMP_EXTRACT_DIR}'.")
        except Exception as e:
            logging.error(f"Failed to extract '{zip_filename}': {e}")
            return

        # Find CSV
        csv_files = [f for f in os.listdir(self.TEMP_EXTRACT_DIR) if f.lower().endswith('.csv')]
        if not csv_files:
            logging.error("No CSV files found in extracted directory.")
            return

        csv_path = os.path.join(self.TEMP_EXTRACT_DIR, csv_files[0])
        logging.info(f"Processing CSV file: {csv_files[0]}")
        self.process_csv(csv_path)
        os.remove(csv_path)
        logging.info(f"Deleted temporary file: {csv_path}")

    def process_csv(self, file_path):
        entries = []
        count = 0

        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='|')
            total_rows = sum(1 for _ in open(file_path, 'r', encoding='utf-8')) - 1
            csvfile.seek(0)

            logging.info(f"Processing '{file_path}' with {total_rows} rows.")
            for row in reader:
                cleaned = self.clean_row(row)
                if cleaned:
                    entries.append(TM_Transliteration(**cleaned))
                count += 1

                if count % BATCH_SIZE == 0:
                    with transaction.atomic():
                        TM_Transliteration.objects.bulk_create(entries, ignore_conflicts=True)
                    logging.info(f"Inserted {count} records so far.")
                    entries = []

            # Insert remaining
            if entries:
                with transaction.atomic():
                    TM_Transliteration.objects.bulk_create(entries, ignore_conflicts=True)
                logging.info(f"Inserted total {count} records.")

    def clean_row(self, row):
        cleaned = {}
        for key, value in row.items():
            if key is None:
                continue

            norm_key = key.strip()
            if norm_key in self.CSV_TO_MODEL_MAP:
                field_name = self.CSV_TO_MODEL_MAP[norm_key]
                value = value.strip() if isinstance(value, str) else value

                # application_number is an integer
                if field_name == "application_number":
                    try:
                        cleaned[field_name] = int(value) if value else 0
                    except (ValueError, TypeError):
                        cleaned[field_name] = 0
                # mark_transliteration_text is a TextField (no max_length needed)
                else:
                    # If empty, default to empty string
                    cleaned[field_name] = value if value else ""
            else:
                logging.warning(f"Unmapped CSV field '{key}' will be skipped.")
        return cleaned if cleaned else None
