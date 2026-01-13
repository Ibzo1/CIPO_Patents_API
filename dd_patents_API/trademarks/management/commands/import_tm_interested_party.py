import os
import csv
import zipfile
import logging
from django.core.management.base import BaseCommand
from trademarks.models import TM_Interested_Party
from django.db import transaction
from django.core.exceptions import FieldDoesNotExist

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
BATCH_SIZE = 1000

class Command(BaseCommand):
    help = "Import TM_Interested_Party data from a ZIP file containing a CSV."

    # Adjust these paths if needed
    ZIP_FILE_PATH = "C:/Users/Intern_1/Documents/TM_Data/TM_interested_party_2024-11-20.zip"
    TEMP_EXTRACT_DIR = "C:/Users/Intern_1/Documents/TM_Data/temp_extracted/"

    # Map CSV headers to model fields
    CSV_TO_MODEL_MAP = {
        "Application Number - Numéro de la demande": "application_number",
        "Party Type Code - Code de type de la partie intéressée": "party_type_code",
        "Party Language Code - Code de langue de la partie intéressée": "party_language_code",
        "Party Name - Nom de la partie intéressée": "party_name",
        "Party Address Line 1 - Ligne 1 de l'adresse de la partie intéressée": "party_address_line1",
        "Party Address Line 2 - Ligne 2 de l'adresse de la partie intéressée": "party_address_line2",
        "Party Address Line 3 - Ligne 3 de l'adresse de la partie intéressée": "party_address_line3",
        "Party Address Line 4 - Ligne 4 de l'adresse de la partie intéressée": "party_address_line4",
        "Party Address Line 5 - Ligne 5 de l'adresse de la partie intéressée": "party_address_line5",
        "Party Province Name - Nom de la province de la partie intéressée": "party_province_name",
        "Party Country Code - Code du pays de la partie intéressée": "party_country_code",
        "Party Postal Code - Code postal de la partie intéressée": "party_postal_code",
        "Contact Language Code - Code langue de correspondance de l'agent": "contact_language_code",
        "Contact Name - Information sur le nom du représentant": "contact_name",
        "Contact Address Line 1 - Ligne 1 de l'adresse du représentant": "contact_address_line1",
        "Contact Address Line 2 - Ligne 2 de l'adresse du représentant": "contact_address_line2",
        "Contact Address Line 3 - Ligne 3 de l'adresse du représentant": "contact_address_line3",
        "Contact Province Name - Province du représentant": "contact_province_name",
        "Contact Country Code - Pays de représentant": "contact_country_code",
        "Contact Postal Code - Code postal  du représentant": "contact_postal_code",
        "Current Owner Legal Name - Nom légal du requérant courant": "current_owner_legal_name",
        "Agent Number - Numéro de l'agent": "agent_number",
    }

    # Provide defaults for all required, non-null character fields 
    REQUIRED_DEFAULTS = {
        "party_country_code": "XX",      # CharField (max_length=2), not null
        "contact_language_code": "EN",   # CharField (max_length=2), not null
        "contact_country_code": "XX",    # CharField (max_length=2), not null
        "contact_name": "Unknown",       # CharField (max_length=255), not null
        "contact_address_line1": "Unknown",   # CharField, not null
        "current_owner_legal_name": "Unknown" # CharField, not null
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
                    entries.append(TM_Interested_Party(**cleaned))
                count += 1

                # Bulk insert in batches 
                if count % BATCH_SIZE == 0:
                    with transaction.atomic():
                        TM_Interested_Party.objects.bulk_create(entries, ignore_conflicts=True)
                    logging.info(f"Inserted {count} records so far.")
                    entries = []

            # Insert any remaining entries
            if entries:
                with transaction.atomic():
                    TM_Interested_Party.objects.bulk_create(entries, ignore_conflicts=True)
                logging.info(f"Inserted total {count} records.")

    def clean_row(self, row):
        cleaned = {}

        # Map CSV fields to model fields 
        for key, value in row.items():
            if key is None:
                continue
            norm_key = key.strip()
            if norm_key in self.CSV_TO_MODEL_MAP:
                model_field = self.CSV_TO_MODEL_MAP[norm_key]
                value = value.strip() if isinstance(value, str) else value

                # For integer fields
                if model_field in ["application_number", "agent_number"]:
                    try:
                        cleaned[model_field] = int(value) if value else 0
                    except (ValueError, TypeError):
                        cleaned[model_field] = 0
                else:
                    # For CharFields, ensure we truncate to max_length
                    max_length = self.get_char_field_max_length(model_field)
                    if isinstance(value, str) and max_length and len(value) > max_length:
                        logging.warning(f"Truncating field '{model_field}' from {len(value)} to {max_length} chars.")
                        value = value[:max_length]

                    # If this is a 2-char code field, slice to 2
                    if model_field in ["party_language_code", "party_country_code", 
                                       "contact_language_code", "contact_country_code"]:
                        if value:
                            value = value[:2]
                    
                    cleaned[model_field] = value
            else:
                logging.warning(f"Unmapped CSV field '{key}' will be skipped.")

        # Provide defaults for any required fields that are empty or missing
        for field, default_val in self.REQUIRED_DEFAULTS.items():
            # If not set or is empty
            if field not in cleaned or not cleaned[field]:
                # Force a fallback value
                # e.g., "Unknown" for text, or "XX" for 2-char codes
                cleaned[field] = default_val

        return cleaned if cleaned else None

    def get_char_field_max_length(self, field_name):
        try:
            field = TM_Interested_Party._meta.get_field(field_name)
            return getattr(field, 'max_length', None)
        except FieldDoesNotExist:
            return None
