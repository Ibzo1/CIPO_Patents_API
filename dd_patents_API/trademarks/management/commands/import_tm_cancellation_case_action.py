import os
import csv
import sys
import zipfile
import logging
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from trademarks.models import TM_Cancellation_Case_Action
from django.core.exceptions import FieldDoesNotExist

# Expand CSV field size limit
import csv
max_int = sys.maxsize
while True:
    try:
        csv.field_size_limit(max_int)
        break
    except OverflowError:
        max_int = int(max_int / 10)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
BATCH_SIZE = 1000

class Command(BaseCommand):
    help = "Import TM_Cancellation_Case_Action data from a ZIP file containing a CSV."

    ZIP_FILE_PATH = "C:/Users/Intern_1/Documents/TM_Data/TM_cancellation_case_action_2024-11-20.zip"
    TEMP_EXTRACT_DIR = "C:/Users/Intern_1/Documents/TM_Data/temp_extracted/"

    CSV_TO_MODEL_MAP = {
    "Application Number - Numéro de la demande": "application_number",
    "Additional Comment - Information supplémentaire": "additional_comment",
    "Proceeding Effective Date - Date d’entrée en vigueur de l’action": "proceeding_effective_date",
    "Section 44/45 Case Number - Numéro du cas de l’article 44/45": "section_44_45_case_number",
    "Legal Proceeding Type Description in English - Description du type de procédure juridique en anglais": "legal_proceeding_type_description_english",
    "Legal Proceeding Type Description in French - Description du type de procédure juridique en français": "legal_proceeding_type_description_french",
    "Section 44/45 Filing Date - Date de soumission de l’article 44/45": "section_44_45_filing_date",
    "WIPO Section 44/45 Status Category Code - Catégorie du statut de l’article 44/45 selon l’OMPI": "wipo_section_44_45_status_category_code",
    "Section 44/45 Status Code - Code du statut de l’article 44/45": "section_44_45_status_code",
    "Section 44/45 Status Date - Date du statut de l’article 44/45": "section_44_45_status_date",
    "Section 44/45 Stage Code - Code de l’étape de l’article 44/45": "section_44_45_stage_code",
    "Section 44/45 case status - Statut du cas sous l’article 44/45": "section_44_45_case_status",
    "Section 44/45 actions code - Code d’action de l'article  44/45": "section_44_45_actions_code",
}


    DEFAULT_DATE = datetime(1970, 1, 1).date()

    def handle(self, *args, **options):
        logging.info(f"ZIP File Path: {self.ZIP_FILE_PATH}")
        logging.info(f"Temp Extract Dir: {self.TEMP_EXTRACT_DIR}")

        os.makedirs(self.TEMP_EXTRACT_DIR, exist_ok=True)
        zip_filename = os.path.basename(self.ZIP_FILE_PATH)
        logging.info(f"Starting for ZIP: {zip_filename}")

        try:
            with zipfile.ZipFile(self.ZIP_FILE_PATH, 'r') as zip_ref:
                zip_ref.extractall(self.TEMP_EXTRACT_DIR)
            logging.info(f"Extracted '{zip_filename}' to '{self.TEMP_EXTRACT_DIR}'.")
        except Exception as e:
            logging.error(f"Failed extracting '{zip_filename}': {e}")
            return

        csv_files = [f for f in os.listdir(self.TEMP_EXTRACT_DIR) if f.lower().endswith('.csv')]
        if not csv_files:
            logging.error("No CSV found in extracted directory.")
            return

        csv_path = os.path.join(self.TEMP_EXTRACT_DIR, csv_files[0])
        logging.info(f"Found CSV: {csv_files[0]}")
        self.process_csv(csv_path)
        os.remove(csv_path)
        logging.info(f"Deleted temp CSV: {csv_path}")

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
                    entries.append(TM_Cancellation_Case_Action(**cleaned))
                count += 1
                if count % BATCH_SIZE == 0:
                    with transaction.atomic():
                        TM_Cancellation_Case_Action.objects.bulk_create(entries, ignore_conflicts=True)
                    logging.info(f"Inserted {count} records so far.")
                    entries = []
            if entries:
                with transaction.atomic():
                    TM_Cancellation_Case_Action.objects.bulk_create(entries, ignore_conflicts=True)
                logging.info(f"Inserted total {count} records.")

    def clean_row(self, row):
        from datetime import datetime
        cleaned = {}
        for key, value in row.items():
            if not key:
                continue
            norm_key = key.strip()
            if norm_key in self.CSV_TO_MODEL_MAP:
                field = self.CSV_TO_MODEL_MAP[norm_key]
                value = value.strip() if isinstance(value, str) else value
                if field in ["application_number", "section_44_45_case_number",
                             "wipo_section_44_45_status_category_code", "section_44_45_status_code",
                             "section_44_45_stage_code", "section_44_45_actions_code"]:
                    try:
                        cleaned[field] = int(value) if value else 0
                    except ValueError:
                        cleaned[field] = 0
                elif field in ["proceeding_effective_date", "section_44_45_filing_date", "section_44_45_status_date"]:
                    cleaned[field] = self.parse_date(value) or self.DEFAULT_DATE
                else:
                    # text field
                    cleaned[field] = value or ""
            else:
                logging.warning(f"Unmapped field '{key}', skipping.")
        return cleaned if cleaned else None

    def parse_date(self, val):
        if not val:
            return None
        try:
            return datetime.strptime(val, "%Y-%m-%d").date()
        except ValueError:
            return None
