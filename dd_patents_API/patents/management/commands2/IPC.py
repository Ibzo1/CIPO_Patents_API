import os
import sys
import psycopg2
import zipfile
import csv
import logging
from django.conf import settings
from datetime import datetime
from psycopg2.extras import execute_values
import traceback

# Add the project directory to the Python path
sys.path.append('c:/Users/Intern_1/Documents/GitHub/dd_patents_database')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DB_Main.settings')
import django
django.setup()

# Define the directory for ZIP files and the table name
directory = 'c:/Users/Intern_1/Documents/PT_Data/PT_ipc'
table_schema = 'public'  # Update if your table is in a different schema
table_name = 'pt_ipc_classification'
full_table_name = f'"{table_schema}"."{table_name}"'  # Use double quotes for case sensitivity

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Field configurations for dynamic handling
FIELD_MAX_LENGTHS = {
    'patent_number_id': 50,
    'ipc_classification_sequence_number': None,  # integer
    'ipc_version_date': None,  # date
    'classification_level': 1,
    'classification_status_code': 1,
    'classification_status': 1,
    'ipc_section_code': 1,
    'ipc_section': 350,
    'ipc_class_code': 10,
    'ipc_class': 500,
    'ipc_subclass_code': 10,
    'ipc_subclass': 500,
    'ipc_main_group_code': 10,
    'ipc_group': 500,
    'ipc_subgroup_code': 10,
    'ipc_subgroup': 500,
}

CSV_TO_DB_FIELD_MAPPING = {
    'Patent Number - Numéro du brevet': 'patent_number_id',
    'IPC Classification Sequence Number - Numéro de séquence de la classification de la CIB': 'ipc_classification_sequence_number',
    'IPC Version Date - Date de la version de la CIB': 'ipc_version_date',
    'Classification Level - Niveau de classification': 'classification_level',
    'Classification Status Code - Code du statut de classification': 'classification_status_code',
    'Classification Status - Statut de classification': 'classification_status',
    'IPC Section Code - Code de la section de la CIB': 'ipc_section_code',
    'IPC Section - Section de la CIB': 'ipc_section',
    'IPC Class Code - Code de la classe de la CIB': 'ipc_class_code',
    'IPC Class - Classe de la CIB': 'ipc_class',
    'IPC Subclass Code - Code de la sous-classe de la CIB': 'ipc_subclass_code',
    'IPC Subclass - Sous-classe de la CIB': 'ipc_subclass',
    'IPC Main Group Code - Code du groupe principal de la CIB': 'ipc_main_group_code',
    'IPC Group - Groupe de la CIB': 'ipc_group',
    'IPC Subgroup Code - Code du sous-groupe de la CIB': 'ipc_subgroup_code',
    'IPC Subgroup - Sous-groupe de la CIB': 'ipc_subgroup',
}

def clean_value(value, max_length=None, field_type=str):
    """
    Cleans a field value, truncating it if it exceeds the max length and converting to the appropriate type.
    """
    if value is None or value == '':
        return None
    value = ''.join(char for char in str(value) if char.isprintable()).strip()
    if field_type == 'date':
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            logging.warning(f"Invalid date format: {value}")
            return None
    elif field_type == 'int':
        try:
            return int(value)
        except ValueError:
            logging.warning(f"Invalid integer value: {value}")
            return None
    if max_length and len(value) > max_length:
        logging.warning(f"Value truncated: {value} to {value[:max_length]}")
        return value[:max_length]
    return value

def preprocess_headers(reader):
    """
    Maps the complex CSV headers to simple field names based on the mapping dictionary.
    """
    new_fieldnames = []
    for header in reader.fieldnames:
        mapped = CSV_TO_DB_FIELD_MAPPING.get(header, header)
        new_fieldnames.append(mapped)
    reader.fieldnames = new_fieldnames
    return reader

def process_rows(rows, conn):
    """
    Inserts a batch of rows into the database using execute_values for efficiency.
    """
    try:
        with conn.cursor() as cur:
            query = f"""
            INSERT INTO {full_table_name} (
                patent_number_id, ipc_classification_sequence_number, ipc_version_date, classification_level,
                classification_status_code, classification_status, ipc_section_code, ipc_section,
                ipc_class_code, ipc_class, ipc_subclass_code, ipc_subclass, ipc_main_group_code, ipc_group,
                ipc_subgroup_code, ipc_subgroup
            ) VALUES %s
            ON CONFLICT (patent_number_id, ipc_classification_sequence_number)
            DO NOTHING;
            """
            values = [
                (
                    clean_value(row.get('patent_number_id'), FIELD_MAX_LENGTHS['patent_number_id']),
                    clean_value(row.get('ipc_classification_sequence_number'), field_type='int'),
                    clean_value(row.get('ipc_version_date'), field_type='date'),
                    clean_value(row.get('classification_level'), FIELD_MAX_LENGTHS['classification_level']),
                    clean_value(row.get('classification_status_code'), FIELD_MAX_LENGTHS['classification_status_code']),
                    clean_value(row.get('classification_status'), FIELD_MAX_LENGTHS['classification_status']),
                    clean_value(row.get('ipc_section_code'), FIELD_MAX_LENGTHS['ipc_section_code']),
                    clean_value(row.get('ipc_section'), FIELD_MAX_LENGTHS['ipc_section']),
                    clean_value(row.get('ipc_class_code'), FIELD_MAX_LENGTHS['ipc_class_code']),
                    clean_value(row.get('ipc_class'), FIELD_MAX_LENGTHS['ipc_class']),
                    clean_value(row.get('ipc_subclass_code'), FIELD_MAX_LENGTHS['ipc_subclass_code']),
                    clean_value(row.get('ipc_subclass'), FIELD_MAX_LENGTHS['ipc_subclass']),
                    clean_value(row.get('ipc_main_group_code'), FIELD_MAX_LENGTHS['ipc_main_group_code']),
                    clean_value(row.get('ipc_group'), FIELD_MAX_LENGTHS['ipc_group']),
                    clean_value(row.get('ipc_subgroup_code'), FIELD_MAX_LENGTHS['ipc_subgroup_code']),
                    clean_value(row.get('ipc_subgroup'), FIELD_MAX_LENGTHS['ipc_subgroup']),
                )
                for row in rows
            ]
            execute_values(cur, query, values)
            conn.commit()
            logging.info(f"Inserted batch of {len(rows)} rows.")
    except Exception as e:
        logging.error(f"Error inserting batch: {e}\n{traceback.format_exc()}")
        conn.rollback()

def process_csv_file(csv_file, conn, zip_filename, csv_filename):
    """
    Processes a single CSV file for insertion into the database.
    """
    try:
        content = csv_file.read().decode('utf-8')
        reader = csv.DictReader(content.splitlines(), delimiter='|')
        reader = preprocess_headers(reader)
        batch = []
        batch_size = 100
        for row_number, row in enumerate(reader, start=1):
            try:
                # Map complex headers to simple field names
                mapped_row = {CSV_TO_DB_FIELD_MAPPING.get(k, k): v for k, v in row.items()}
                # Clean the row data
                cleaned_row = {k: v for k, v in mapped_row.items()}
                batch.append(cleaned_row)
                if len(batch) >= batch_size:
                    process_rows(batch, conn)
                    batch.clear()
            except Exception as e:
                logging.error(f"Skipping row {row_number} in {csv_filename} within {zip_filename} due to error: {e}\n{traceback.format_exc()}")
        if batch:
            process_rows(batch, conn)
    except Exception as e:
        logging.error(f"Error processing CSV file {csv_filename} in ZIP {zip_filename}: {e}\n{traceback.format_exc()}")

def main():
    """
    Main function to process all ZIP files in the directory.
    """
    try:
        conn = psycopg2.connect(
            database=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )
        logging.info("Database connection established.")
        for filename in os.listdir(directory):
            if filename.endswith('.zip'):
                zip_path = os.path.join(directory, filename)
                logging.info(f"Processing ZIP file: {filename}")
                with zipfile.ZipFile(zip_path, 'r') as z:
                    for csv_filename in z.namelist():
                        with z.open(csv_filename) as csv_file:
                            logging.info(f"Processing CSV file: {csv_filename} in ZIP: {filename}")
                            process_csv_file(csv_file, conn, filename, csv_filename)
    except Exception as e:
        logging.error(f"Critical error: {e}\n{traceback.format_exc()}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    main()
