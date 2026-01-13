import os
import csv
import zipfile
import logging
from datetime import datetime
from django.core.management.base import BaseCommand
from trademarks.models import TM_Representation
from django.db import models
from django.core.exceptions import FieldDoesNotExist

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Command(BaseCommand):
    help = "Import TM_Representation data from a ZIP file containing a CSV."

    ZIP_FILE_PATH = "C:/Users/Intern_1/Documents/TM_Data/TM_representation_2024-11-20.zip"
    TEMP_EXTRACT_DIR = "C:/Users/Intern_1/Documents/TM_Data/temp_extracted/"

    # Mapping from normalized (stripped) CSV header keys to TM_Representation model field names.
    CSV_TO_MODEL_MAP = {
        "Application Number - Numéro de la demande": "application_number",
        "Representation Type Code - Code de type de représentation": "representation_type_code",
        "Vienna Code - Code de Vienne": "vienna_code",
        "Vienna Division Number - Numéro de division de Vienne": "vienna_division_number",
        "Vienna Section Number - Numéro de section de Vienne": "vienna_section_number",
        "Vienna Description - Description de Vienne en Anglais": "vienna_description",
        "Vienna Description Fr - Description de Vienne en Français": "vienna_description_fr",
        "Filename Short - Nom du fichier": "file_name",
        "File Format Short - Format du fichier": "file_format",
        "Image Colour Claimed Sequence Number - Numéro d'ordre de revendication de couleur": "image_colour_claimed_sequence_number",
        "Image Colour Claimed - Revendication de couleur": "image_colour_claimed",
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
            total_rows = sum(1 for _ in open(file_path, 'r', encoding='utf-8')) - 1
            csvfile.seek(0)
            logging.info(f"Processing '{file_path}' with {total_rows} rows.")
            for row in reader:
                cleaned = self.clean_row(row)
                if cleaned:
                    entries.append(TM_Representation(**cleaned))
            TM_Representation.objects.bulk_create(entries, ignore_conflicts=True)
            logging.info(f"Inserted {len(entries)} records.")

    def clean_row(self, row):
        cleaned = {}
        # Normalize the CSV header keys by stripping spaces.
        for key, value in row.items():
            norm_key = key.strip()
            if norm_key in self.CSV_TO_MODEL_MAP:
                model_field = self.CSV_TO_MODEL_MAP[norm_key]
                if isinstance(value, list):
                    value = ','.join(map(str, value))
                value = value.strip() if isinstance(value, str) else value
                if model_field in ["application_number", "representation_type_code", "vienna_code", "vienna_division_number", "vienna_section_number", "image_colour_claimed_sequence_number"]:
                    try:
                        cleaned[model_field] = int(value)
                    except ValueError:
                        cleaned[model_field] = None
                else:
                    cleaned[model_field] = value
            else:
                logging.warning(f"Unmapped CSV field '{key}' will be skipped.")
        return cleaned if cleaned else None
