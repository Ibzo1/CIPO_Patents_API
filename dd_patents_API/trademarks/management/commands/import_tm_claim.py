import os
import csv
import zipfile
import logging
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from trademarks.models import TM_Claim

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Lowered batch size to reduce memory usage per bulk insert
BATCH_SIZE = 100

class Command(BaseCommand):
    help = "Import TM_Claim data from a ZIP file containing a CSV."

    ZIP_FILE_PATH = "C:/Users/Intern_1/Documents/TM_Data/TM_claim_2024-11-20.zip"
    TEMP_EXTRACT_DIR = "C:/Users/Intern_1/Documents/TM_Data/temp_extracted/"

    CSV_TO_MODEL_MAP = {
        "Application Number - Numéro de la demande ": "application_number",
        "Claim Text - Texte de revendication": "claim_text",
        "Claim Type - Type de revendication": "claim_type",
        "Claim Number - Numéro de revendication": "claim_number",
        "Claim Code - Code de revendication": "claim_code",
        "Structure Claim Date - Date de revendication structurée": "structure_claim_date",
        "Claim Year Number - Année de la revendication": "claim_year_number",
        "Claim Month Number - Mois de la revendication": "claim_month_number",
        "Claim Day Number - Jour de la revendication": "claim_day_number",
        "Claim Country Code - Code du pays de la revendication": "claim_country_code",
        "Foreign Registration Number - Numéro d’enregistrement de la revendication étrangère": "foreign_registration_number",
        "Goods Services Reference Identifier - Nom de référence des produits et services": "goods_services_reference_identifier",
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
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='|')
            # Calculate total rows for logging purposes
            total_rows = sum(1 for _ in open(file_path, 'r', encoding='utf-8')) - 1
            csvfile.seek(0)
            logging.info(f"Processing '{file_path}' with {total_rows} rows.")
            for i, row in enumerate(reader, start=1):
                cleaned = self.clean_row(row)
                if cleaned:
                    entries.append(TM_Claim(**cleaned))
                # When we hit the batch size, commit the current batch in its own transaction
                if i % BATCH_SIZE == 0:
                    with transaction.atomic():
                        TM_Claim.objects.bulk_create(entries, ignore_conflicts=True)
                    logging.info(f"Inserted {i} records so far.")
                    entries = []
            # Insert any remaining records
            if entries:
                with transaction.atomic():
                    TM_Claim.objects.bulk_create(entries, ignore_conflicts=True)
                logging.info(f"Inserted total {i} records.")

    def clean_row(self, row):
        cleaned = {}
        for key, value in row.items():
            if key in self.CSV_TO_MODEL_MAP:
                model_field = self.CSV_TO_MODEL_MAP[key]
                # If the value is a list, join it into a string
                if isinstance(value, list):
                    value = ','.join(map(str, value))
                value = value.strip() if isinstance(value, str) else value

                if model_field == "structure_claim_date":
                    cleaned[model_field] = self.parse_date(value)
                elif model_field in [
                    "application_number",
                    "claim_type",
                    "claim_number",
                    "claim_code",
                    "claim_year_number",
                    "claim_month_number",
                    "claim_day_number"
                ]:
                    try:
                        cleaned[model_field] = int(value)
                    except ValueError:
                        cleaned[model_field] = None
                elif model_field == "claim_country_code":
                    cleaned[model_field] = value[:2] if value else None
                else:
                    cleaned[model_field] = value
            else:
                logging.warning(f"Unmapped CSV field '{key}' will be skipped.")
        return cleaned if cleaned else None

    def parse_date(self, value):
        if not value:
            return None
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return None
