import os
import csv
import zipfile
import logging
from datetime import datetime
from django.core.management.base import BaseCommand
from trademarks.models import TM_Main
from django.db import models
from django.core.exceptions import FieldDoesNotExist

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# 32-bit integer boundaries
MAX_INT = 2147483647
MIN_INT = -2147483648

class Command(BaseCommand):
    help = "Import TM_Main data from a ZIP file, automatically handling merged headers and clamping int fields."

    # This is the merged header for Distinctiveness+Evidence
    MERGED_HEADER = 'Distinctiveness Description - Descriotion du caractère distinctif acquis - Evidence Of Use Indicator - Indicateur de preuve d’utilisation'

    # Normal mappings for other headers
    CSV_TO_MODEL_MAP = {
        'Application Number - Numéro de la demande ': 'application_number',
        'Filing Date - Date de dépôt': 'filing_date',
        'Publication Date - Date de publication': 'publication_date',
        'Registration Date - Date d’enregistrement': 'registration_date',
        'Registration Office Country Code - Code du pays de l’office de l’enregistrement': 'registration_office_country_code',
        'Receiving Office Country Code - Code du pays de l’office récepteur': 'receiving_office_country_code',
        'Receiving Office Date - Date de réception par l’office': 'receiving_office_date',
        "Assigning Office Country Code - Code du pays de l'office de cession": 'assigning_office_country_code',
        'Registration Number - Numéro d’enregistrement': 'registration_number',
        'Legislation Description Code - Code de description de la législation (Code de Loi applicable)': 'legislation_description_code',
        'Filing Place - Pays de Dépôt': 'filing_place',
        'Application Reference Number - Numéro de référence de la demande': 'application_reference_number',
        'Application Language Code - Code de langue de la demande': 'application_language_code',
        "Expiry Date - Date d'expiration": 'expiry_date',
        'Termination Date - Date d’inactivation': 'termination_date',
        'WIPO Status Code - Code du statut de l’OMPI': 'wipo_status_code',
        'Current Status Date - Date de statut actuel ': 'current_status_date',
        'Association Category ID - Indicateur de cession partielle': 'association_category_id',
        'Association Assigning Country Code - Code du pays de la demande': 'association_assigning_country_code',
        'Associated Application Number - Numéro de la demande associée': 'associated_application_number',
        'Mark Category - Catégorie de la marque ': 'mark_category',
        'Divisional Application Country Code - Code du pays de la demande divisionnaire': 'divisional_application_country_code',
        'Divisional Application Number - numéro de la demande divisionnaire (Numéro ST.13 de la demande originale)': 'divisional_application_number',
        'Divisional Application Date - Date de la demande divisionnaire': 'divisional_application_date',
        'Internationall Registration Number - Numéro d’enregistrement international': 'international_registration_number',
        'MarkType Code - Code du type de marque ': 'marktype_code',
        'Mark Verbal Element Description - Description de l’élément Verbal de la marque (Texte de l’élément Verbal de la marque)': 'mark_verbal_element_description',
        'Mark Significant Description - Description  détaillée de la marque (Texte de l’élément verbal signifiant de la marque)': 'mark_significant_description',
        'Mark Translation Description - Description de la traduction de la marque (Traduction de la marque)': 'mark_translation_description',
        'Expungement Indicator - Indicateur de radiation': 'expungement_indicator',
        'Distinctiveness Indicator - Indicateur de caractère distinctif acquis': 'distinctiveness_indicator',
        'Evidence Of Use Description - Description de preuve d’utilisation': 'evidence_of_use_description',
        'Restriction Of Use Description - Description de la restriction d’utilisation': 'restriction_of_use_description',
        'CIPO Standard Message Description - Description de la mise en garde sur les données de marque de commerce': 'cipo_standard_message_description',
        'Opposition Start Date - Date de début d’opposition ': 'opposition_start_date',
        'Opposition End Date - Date de fin d’opposition ': 'opposition_end_date',
        'Total Nice Classifications Number - Nombre total de classification de Nice ': 'total_nice_classifications_number',
        'Foreign Application Indicator - Indicateur de demande étrangère': 'foreign_application_indicator',
        "Foreign Registration Indicator - Indicateur d'enregistrement étranger": 'foreign_registration_indicator',
        'Used In Canada Indicator - Indicateur d’utilisation au Canada': 'used_in_canada_indicator',
        "Proposed Use In Canada Indicator - Indicateur d'utilisation projetée au Canada": 'proposed_use_in_canada_indicator',
        "Classification Term Office Country Code - Code du pays de l'office du terme de classification": 'classification_term_office_country_code',
        'Classification Term Source Name - Catégorie de la source du terme de classification': 'classification_term_source_name',
        'Classification Term English Description - Description en anglais du terme de classification': 'classification_term_english_description',
        'Publication ID - Numéro et volume de la publication ': 'publication_id',
        'Publication Status - Statut de publication': 'publication_status',
        "Authorization Of Use Date - Date d’autorisation d'utilisation": 'authorization_of_use_date',
        "Authorization Code - Code d'autorisation": 'authorization_code',
        "Authorization Description - Description d'autorisation": 'authorization_description',
        'Register Code - Catégorie du registre': 'register_code',
        'Application Abandoned Date - Date d’abandon de la demande': 'application_abandoned_date',
        'CIPO Status Code - Code de statut de la marque': 'cipo_status_code',
        'Allowed Date - Date admise': 'allowed_date',
        'Renewal Date - Date de renouvellement': 'renewal_date',
        'Trademark Class Code - Code de la classe de marque ': 'trademark_class_code',
        'Geographical Indication Kind Category Code - Code du type d’indication géographique': 'geographical_indication_kind_category_code',
        'Geographical Indication Translation Sequence Number - Numéro d’ordre de traduction de l’indication géographique': 'geographical_indication_translation_sequence_number',
        'Geographical IndicationTranslationText - Texte de la traduction de l’indication géographique': 'geographical_indication_translation_text',
        'Doubtful Case Application Number - Numéro de demande du cas douteux': 'doubtful_case_application_number',
        'Doubtful Case Registration Number - Numéro d’enregistrement du cas douteux': 'doubtful_case_registration_number',
    }

    def handle(self, *args, **options):
        zip_file_path = 'C:/Users/Intern_1/Documents/TM_Data/TM_application_main.zip'
        temp_extract_dir = 'C:/Users/Intern_1/Documents/TM_Data/temp_extracted/'
        batch_size = 1000

        logging.info(f"ZIP File Path: {zip_file_path}")
        logging.info(f"Temporary Extract Directory: {temp_extract_dir}")

        self.stdout.write(self.style.NOTICE(f"ZIP File Path: {zip_file_path}"))
        self.stdout.write(self.style.NOTICE(f"Temporary Extract Directory: {temp_extract_dir}"))

        os.makedirs(temp_extract_dir, exist_ok=True)
        zip_filename = os.path.basename(zip_file_path)

        logging.info(f"Starting processing for ZIP file: {zip_filename}")
        self.stdout.write(self.style.SUCCESS(f"Starting processing for ZIP file: {zip_filename}"))

        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_extract_dir)
            logging.info(f"Extracted '{zip_filename}' to '{temp_extract_dir}'.")
            self.stdout.write(self.style.SUCCESS(f"Extracted '{zip_filename}' to '{temp_extract_dir}'."))
        except zipfile.BadZipFile:
            logging.error(f"Failed to extract '{zip_filename}': Bad ZIP file.")
            self.stdout.write(self.style.ERROR(f"Failed to extract '{zip_filename}': Bad ZIP file."))
            return
        except Exception as e:
            logging.error(f"Failed to extract '{zip_filename}': {e}")
            self.stdout.write(self.style.ERROR(f"Failed to extract '{zip_filename}': {e}"))
            return

        extracted_files = [f for f in os.listdir(temp_extract_dir) if f.lower().endswith('.csv')]
        if not extracted_files:
            logging.warning(f"No CSV files found in '{zip_filename}'.")
            self.stdout.write(self.style.WARNING(f"No CSV files found in '{zip_filename}'."))
            self.cleanup_temp_files(temp_extract_dir)
            return

        for csv_filename in extracted_files:
            csv_path = os.path.join(temp_extract_dir, csv_filename)
            logging.info(f"Processing CSV file: {csv_filename}")
            self.stdout.write(self.style.SUCCESS(f"Processing CSV file: {csv_filename}"))

            try:
                self.process_csv(csv_path, batch_size)
            except Exception as e:
                logging.error(f"Error processing '{csv_filename}': {e}")
                self.stdout.write(self.style.ERROR(f"Error processing '{csv_filename}': {e}"))
                continue

        logging.info(f"Import process for '{zip_filename}' completed successfully.")
        self.stdout.write(self.style.SUCCESS(f"Import process for '{zip_filename}' completed successfully."))
        self.cleanup_temp_files(temp_extract_dir)

    def cleanup_temp_files(self, temp_dir):
        for f in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, f)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    logging.info(f"Deleted temporary file: {file_path}")
                    self.stdout.write(self.style.NOTICE(f"Deleted temporary file: {file_path}"))
            except Exception as e:
                logging.error(f"Failed to delete '{file_path}': {e}")
                self.stdout.write(self.style.ERROR(f"Failed to delete '{file_path}': {e}"))

    def process_csv(self, file_path, batch_size):
        tm_main_objects = []
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='|')
            total_rows = sum(1 for _ in open(file_path, 'r', encoding='utf-8')) - 1
            csvfile.seek(0)

            logging.info(f"Processing '{file_path}' with {total_rows} rows.")
            self.stdout.write(self.style.NOTICE(f"Processing '{file_path}' with {total_rows} rows."))

            for i, row in enumerate(reader, start=1):
                cleaned_row = self.clean_row(row)
                if cleaned_row:
                    tm_main_objects.append(TM_Main(**cleaned_row))

                if i % batch_size == 0:
                    self.bulk_insert(tm_main_objects)
                    tm_main_objects = []
                    logging.info(f"Inserted {i} records so far.")
                    self.stdout.write(self.style.SUCCESS(f"Inserted {i} records so far."))

            if tm_main_objects:
                self.bulk_insert(tm_main_objects)
                logging.info(f"Inserted {i} records in total.")
                self.stdout.write(self.style.SUCCESS(f"Inserted {i} records in total."))

    def bulk_insert(self, objects):
        TM_Main.objects.bulk_create(objects, ignore_conflicts=True)

    def clean_row(self, row):
        cleaned = {}

        for key, value in row.items():
            if not value:
                continue

            # If the CSV has that single merged header we handle it separately
            if key == 'Distinctiveness Description - Descriotion du caractère distinctif acquis - Evidence Of Use Indicator - Indicateur de preuve d’utilisation':
                cleaned['distinctiveness_description'] = value.strip()
                # Attempt to parse 'TRUE' or 'FALSE'
                upper_val = value.upper()
                if 'TRUE' in upper_val:
                    cleaned['evidence_of_use_indicator'] = True
                elif 'FALSE' in upper_val:
                    cleaned['evidence_of_use_indicator'] = False
                else:
                    # default
                    cleaned['evidence_of_use_indicator'] = False
            # Otherwise, normal fields
            elif key in self.CSV_TO_MODEL_MAP:
                model_field = self.CSV_TO_MODEL_MAP[key]
                if isinstance(value, list):
                    logging.warning(f"Field '{key}' has list value {value}. Joining into a single string.")
                    value = ','.join(map(str, value))

                value = value.strip() if isinstance(value, str) else value

                # If model_field ends in 'date'
                if 'date' in model_field:
                    if self.is_valid_date(value):
                        cleaned[model_field] = value
                    else:
                        cleaned[model_field] = None
                elif 'indicator' in model_field:
                    cleaned[model_field] = True if value and value.upper() == 'TRUE' else False
                elif 'number' in model_field or 'code' in model_field:
                    try:
                        num_val = int(value)
                        # Clamp to 32-bit int range
                        if num_val > MAX_INT:
                            num_val = MAX_INT
                        elif num_val < MIN_INT:
                            num_val = MIN_INT
                        cleaned[model_field] = num_val
                    except ValueError:
                        cleaned[model_field] = None
                elif self.is_char_field(model_field):
                    max_length = self.get_char_field_max_length(model_field)
                    if value and len(value) > max_length:
                        logging.warning(f"Truncating field '{model_field}' from length {len(value)} to {max_length}.")
                        cleaned[model_field] = value[:max_length]
                    else:
                        cleaned[model_field] = value
                elif self.is_text_field(model_field):
                    cleaned[model_field] = value
                else:
                    cleaned[model_field] = value
            else:
                logging.warning(f"Unmapped CSV field '{key}' will be skipped.")

        return cleaned if cleaned else None

    def is_valid_date(self, value):
        if not value:
            return False
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def is_char_field(self, field_name):
        try:
            field = TM_Main._meta.get_field(field_name)
            return isinstance(field, models.CharField)
        except FieldDoesNotExist:
            logging.warning(f"Field '{field_name}' does not exist in TM_Main model.")
            return False

    def is_text_field(self, field_name):
        try:
            field = TM_Main._meta.get_field(field_name)
            return isinstance(field, models.TextField)
        except FieldDoesNotExist:
            logging.warning(f"Field '{field_name}' does not exist in TM_Main model.")
            return False

    def get_char_field_max_length(self, field_name):
        try:
            field = TM_Main._meta.get_field(field_name)
            if hasattr(field, 'max_length'):
                return field.max_length
            return 255
        except FieldDoesNotExist:
            logging.warning(f"Field '{field_name}' does not exist in TM_Main model.")
            return 255
