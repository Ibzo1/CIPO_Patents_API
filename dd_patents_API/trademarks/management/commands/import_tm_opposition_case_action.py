import os
import csv
import sys
import zipfile
import logging
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from django.core.exceptions import FieldDoesNotExist
from trademarks.models import TM_Opposition_Case_Action

# Increase CSV field size limit to handle very large fields
max_int = sys.maxsize
while True:
    try:
        csv.field_size_limit(max_int)
        break
    except OverflowError:
        max_int = max_int // 10

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
BATCH_SIZE = 1000

class Command(BaseCommand):
    help = "Import TM_Opposition_Case_Action data from a ZIP file containing a CSV."

    ZIP_FILE_PATH = "C:/Users/Intern_1/Documents/TM_Data/TM_opposition_case_action_2024-11-20.zip"
    TEMP_EXTRACT_DIR = "C:/Users/Intern_1/Documents/TM_Data/temp_extracted/"
    DEFAULT_DATE = datetime(1970, 1, 1).date()

    # Additional fields that are numeric even if their name doesn't contain "number" or "code"
    EXTRA_NUMERIC_FIELDS = ["wipo_opposition_status_category"]

    CSV_TO_MODEL_MAP = {
        "Application Number - Numéro de la demande": "application_number",
        "Additional Comment - Information supplémentaire": "additional_comment",
        "Proceeding Effective Date - Date d’entrée en vigueur de l’action": "proceeding_effective_date",
        "Opposition Case Number - Numéro du cas d’opposition": "opposition_case_number",
        "Opposition Case Type English Name - Type de procédure d’opposition en anglais": "opposition_case_type_english_name",
        "Opposition Case Type French Name - Type de procédure d’opposition en français": "opposition_case_type_french_name",
        "Opposition Date - Date d’opposition": "opposition_date",
        "WIPO Opposition Category Status - Catégorie de statut selon l’OMPI": "wipo_opposition_status_category",
        "Opposition WIPO Status Date - Date de statut selon l’OMPI": "opposition_wipo_status_date",
        "WIPO Opposition Status - Statut d'oppostion selon l’OMPI": "wipo_opposition_case_status",
        "Opposition Case Status Code - Code du statut d’opposition": "opposition_case_status_code",
        "CIPO Opposition Status Date - Date du statut d’opposition de l’OPIC": "cipo_opposition_status_date",
        "Opposition Stage Code - Code de l’étape d’opposition": "opposition_stage_code",
        "Opposition Action Category - Catégorie de l’action d’opposition": "opposition_action_category",
        "Opposition Action Code - Code de l’action d’opposition": "opposition_action_code",
    }

    def handle(self, *args, **options):
        logging.info(f"ZIP File Path: {self.ZIP_FILE_PATH}")
        logging.info(f"Temp Extract Directory: {self.TEMP_EXTRACT_DIR}")

        os.makedirs(self.TEMP_EXTRACT_DIR, exist_ok=True)
        zip_filename = os.path.basename(self.ZIP_FILE_PATH)
        logging.info(f"Extracting ZIP: {zip_filename}")

        try:
            with zipfile.ZipFile(self.ZIP_FILE_PATH, "r") as zip_ref:
                zip_ref.extractall(self.TEMP_EXTRACT_DIR)
            logging.info(f"Extracted '{zip_filename}' to '{self.TEMP_EXTRACT_DIR}'.")
        except Exception as e:
            logging.error(f"Error extracting '{zip_filename}': {e}")
            return

        csv_files = [f for f in os.listdir(self.TEMP_EXTRACT_DIR) if f.lower().endswith(".csv")]
        if not csv_files:
            logging.error("No CSV files found in the extracted folder.")
            return

        csv_path = os.path.join(self.TEMP_EXTRACT_DIR, csv_files[0])
        logging.info(f"Processing CSV: {csv_files[0]}")
        self.process_csv(csv_path)
        os.remove(csv_path)
        logging.info(f"Deleted CSV: {csv_path}")

    def process_csv(self, file_path):
        entries = []
        count = 0

        with open(file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter="|")
            total_rows = sum(1 for _ in open(file_path, "r", encoding="utf-8")) - 1
            csvfile.seek(0)
            logging.info(f"Processing '{file_path}' with {total_rows} rows.")

            for row in reader:
                cleaned = self.clean_row(row)
                if cleaned is None:
                    continue  # Skip invalid row
                entries.append(TM_Opposition_Case_Action(**cleaned))
                count += 1

                if count % BATCH_SIZE == 0:
                    with transaction.atomic():
                        TM_Opposition_Case_Action.objects.bulk_create(entries, ignore_conflicts=True)
                    logging.info(f"Inserted {count} records so far.")
                    entries = []

            if entries:
                with transaction.atomic():
                    TM_Opposition_Case_Action.objects.bulk_create(entries, ignore_conflicts=True)
            logging.info(f"Inserted total {count} records.")

    def clean_row(self, row):
        cleaned = {}
        for key, val in row.items():
            if not key:
                continue
            norm_key = key.strip()
            if norm_key in self.CSV_TO_MODEL_MAP:
                field_name = self.CSV_TO_MODEL_MAP[norm_key]
                val = val.strip() if isinstance(val, str) else val

                if field_name == "application_number":
                    if not val or not val.isdigit():
                        logging.warning(f"Skipping row: invalid application_number '{val}'")
                        return None
                    cleaned[field_name] = int(val)
                elif "number" in field_name or "code" in field_name or field_name in self.EXTRA_NUMERIC_FIELDS:
                    try:
                        # Default to 0 if not purely digits
                        cleaned[field_name] = int(val) if val and val.isdigit() else 0
                    except Exception:
                        cleaned[field_name] = 0
                elif "date" in field_name:
                    parsed = self.parse_date(val)
                    cleaned[field_name] = parsed if parsed else self.DEFAULT_DATE
                else:
                    max_len = self.get_char_field_max_length(field_name)
                    if max_len and isinstance(val, str) and len(val) > max_len:
                        logging.warning(f"Truncating '{field_name}' from {len(val)} to {max_len} chars.")
                        val = val[:max_len]
                    cleaned[field_name] = val or ""
            else:
                logging.warning(f"Unmapped CSV field '{norm_key}' -> skipping.")
        if "application_number" not in cleaned:
            logging.warning("Skipping row: application_number missing after cleaning.")
            return None
        return cleaned if cleaned else None

    def parse_date(self, val):
        if not val:
            return None
        try:
            return datetime.strptime(val, "%Y-%m-%d").date()
        except ValueError:
            return None

    def get_char_field_max_length(self, field_name):
        try:
            f = TM_Opposition_Case_Action._meta.get_field(field_name)
            return getattr(f, "max_length", None)
        except FieldDoesNotExist:
            return None
