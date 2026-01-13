import os
import sys
import csv
import zipfile
import logging
from django.core.management.base import BaseCommand
from trademarks.models import TM_Applicant_Classifications
from django.db import transaction
from django.core.exceptions import FieldDoesNotExist


maxInt = sys.maxsize
while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BATCH_SIZE = 1000

class Command(BaseCommand):
    help = "Import TM_Applicant_Classifications data from a ZIP file containing a CSV."

    ZIP_FILE_PATH = "C:/Users/Intern_1/Documents/TM_Data/TM_applicant_classification_2024-11-20.zip"
    TEMP_EXTRACT_DIR = "C:/Users/Intern_1/Documents/TM_Data/temp_extracted/"

    CSV_TO_MODEL_MAP = {
        "Application Number - Numéro de la demande": "application_number",
        "Classification Sequence Number - Numéro de séquence de la classification": "classification_sequence_number",
        "Classification Indicator Line Sequence Number - Ligne indicatrice du numéro de séquence de la classification": "classification_indicator_line_sequence_number",
        "Nice Edition Number - Numéro d’édition de classification de Nice": "nice_edition_number",
        "Nice Classification Code - Code de de classification de Nice": "nice_classification_code",
        "Nice Classification - Classification de Nice": "nice_classification",
        "Classification indicator description - Description de l'indicateur de la classification": "classification_indicator_description",
    }

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
                    entries.append(TM_Applicant_Classifications(**cleaned))
                count += 1
                if count % BATCH_SIZE == 0:
                    with transaction.atomic():
                        TM_Applicant_Classifications.objects.bulk_create(entries, ignore_conflicts=True)
                    logging.info(f"Inserted {count} records so far.")
                    entries = []
            if entries:
                with transaction.atomic():
                    TM_Applicant_Classifications.objects.bulk_create(entries, ignore_conflicts=True)
                logging.info(f"Inserted total {count} records.")

    def clean_row(self, row):
        cleaned = {}
        for key, value in row.items():
            norm_key = key.strip()
            if norm_key in self.CSV_TO_MODEL_MAP:
                model_field = self.CSV_TO_MODEL_MAP[norm_key]
                value = value.strip() if isinstance(value, str) else value
                if model_field == "application_number":
                    try:
                        cleaned[model_field] = int(value)
                    except ValueError:
                        cleaned[model_field] = 0
                elif model_field in ["classification_indicator_line_sequence_number", "nice_edition_number", "nice_classification_code"]:
                    try:
                        cleaned[model_field] = int(value) if value else 0
                    except ValueError:
                        cleaned[model_field] = 0
                else:
                    cleaned[model_field] = value
            else:
                logging.warning(f"Unmapped CSV field '{key}' will be skipped.")
        # Ensure required integer fields have a default
        if "nice_classification_code" not in cleaned:
            cleaned["nice_classification_code"] = 0
        return cleaned if cleaned else None
