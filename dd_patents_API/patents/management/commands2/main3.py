import os
import csv
import logging
import psycopg2
import django
from django.conf import settings
from datetime import datetime
import sys
import zipfile

# Add the project directory to the Python path
sys.path.append('c:/Users/Intern_1/Documents/GitHub/dd_patents_database')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DB_Main.settings')
django.setup()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

directory = 'c:/Users/Intern_1/Documents/PT_Data/PT_main'
table_name = 'patents_pt_main'
processed_files_log = 'processed_files.txt'  # Ensures processed files are tracked here
temp_extract_dir = 'c:/Users/Intern_1/Documents/PT_Data/temp_extracted'

def is_valid_date(value):
    try:
        datetime.strptime(value.strip(), "%Y-%m-%d")
        return True
    except ValueError:
        return False

MAX_LENGTH = 500  # Maximum allowed character length for constrained fields


def clean_and_prepare_file(input_file, temp_file):
    if os.path.exists(temp_file):
        logging.info(f"Temporary file {temp_file} already exists, skipping cleaning.")
        return

    processed_rows = 0
    total_rows = sum(1 for row in open(input_file, 'r', encoding='utf-8')) - 1
    with open(input_file, 'r', encoding='utf-8') as infile, open(temp_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.DictReader(infile, delimiter='|')
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames, delimiter='|')
        writer.writeheader()

        logging.info(f"Processing file {input_file} with columns: {reader.fieldnames}")

        for row in reader:
            for key, value in row.items():
                # Handle date columns
                if 'date' in key.lower():
                    if value and value not in ['NULL', '-1'] and is_valid_date(value):
                        continue
                    row[key] = ''

                # Handle boolean columns specifically
                elif key == 'License For Sale Indicator - Indicateur de la licence de vente':
                    if value in ['', 'NULL']:
                        row[key] = 'FALSE'  # Set to 'FALSE' if empty or NULL

                # Truncate values for specific columns if they exceed the max length
                elif key in ['Application/Patent Title French - Demande/Titre français du brevet', 
                             'Application/Patent Title English - Demande/Titre anglais du brevet']:
                    if len(value) > MAX_LENGTH:
                        logging.warning(f"Truncating value in '{key}' to {MAX_LENGTH} characters.")
                        row[key] = value[:MAX_LENGTH]

            writer.writerow(row)
            processed_rows += 1

            if processed_rows % 10000 == 0:
                logging.info(f"Processed {processed_rows} out of {total_rows} rows in {input_file}")

    logging.info(f"File cleaned and saved to temporary file: {temp_file}")


def copy_to_database(conn, temp_file, table_name):
    """Copies data from a temporary cleaned file to the database, handling duplicates."""
    temp_table = f"{table_name}_temp"

    with conn.cursor() as cur:
        cur.execute(f"DROP TABLE IF EXISTS {temp_table}")
        cur.execute(f"CREATE TEMP TABLE {temp_table} (LIKE {table_name} INCLUDING ALL)")
        conn.commit()

    with open(temp_file, 'r', encoding='utf-8') as f:
        with conn.cursor() as cur:
            try:
                cur.copy_expert(f"COPY {temp_table} FROM STDIN WITH CSV HEADER DELIMITER '|' NULL AS ''", f)
                conn.commit()
                logging.info(f"Successfully copied data from {temp_file} to temporary table {temp_table}")

                cur.execute(f"SELECT COUNT(*) FROM {temp_table}")
                temp_table_row_count = cur.fetchone()[0]
                logging.info(f"Row count in temp table {temp_table}: {temp_table_row_count}")

                cur.execute(f"""
                    INSERT INTO {table_name}
                    SELECT * FROM {temp_table}
                    ON CONFLICT (patent_number) DO NOTHING
                """)
                conn.commit()

                cur.execute(f"SELECT COUNT(*) FROM {table_name}")
                main_table_row_count = cur.fetchone()[0]
                logging.info(f"Row count in main table {table_name} after insertion: {main_table_row_count}")

                cur.execute(f"DROP TABLE {temp_table}")

            except psycopg2.Error as e:
                logging.error(f"Error copying data from {temp_file}: {e}")
                conn.rollback()
            else:
                conn.commit()

def mark_file_processed(filename):
    with open(processed_files_log, 'a') as log:
        log.write(f"{filename}\n")

def is_file_processed(filename):
    if not os.path.exists(processed_files_log):
        logging.info(f"Processed files log {processed_files_log} does not exist. Proceeding with processing.")
        return False
    with open(processed_files_log, 'r') as log:
        processed_files = log.read().splitlines()
    logging.info(f"Checking if file '{filename}' is already processed.")
    return filename in processed_files

def extract_zip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    logging.info(f"Extracted {zip_path} to {extract_to}")

try:
    conn = psycopg2.connect(
        database=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT']
    )
    logging.info("Database connection established.")

    zip_files = [f for f in os.listdir(directory) if f.endswith('.zip')]
    logging.info(f"Found {len(zip_files)} ZIP files in directory {directory}.")

    for zip_filename in zip_files:
        if not is_file_processed(zip_filename):
            logging.info(f"Starting processing for ZIP file: {zip_filename}")
            zip_path = os.path.join(directory, zip_filename)
            extract_zip_file(zip_path, temp_extract_dir)

            for extracted_filename in os.listdir(temp_extract_dir):
                if extracted_filename.endswith('.csv'):
                    csv_path = os.path.join(temp_extract_dir, extracted_filename)
                    temp_filepath = csv_path.replace('.csv', '_preprocessed.csv')
                    logging.info(f"Cleaning and preparing extracted CSV file for database load: {csv_path}")

                    clean_and_prepare_file(csv_path, temp_filepath)

                    if os.path.exists(temp_filepath):
                        logging.info(f"Temporary file {temp_filepath} created successfully.")
                    else:
                        logging.error(f"Failed to create temporary file {temp_filepath}. Continuing to next file.")
                        continue

                    copy_to_database(conn, temp_filepath, table_name)

            mark_file_processed(zip_filename)
            logging.info(f"ZIP file {zip_filename} marked as processed.")
            for file in os.listdir(temp_extract_dir):
                os.remove(os.path.join(temp_extract_dir, file))
        else:
            logging.info(f"ZIP file {zip_filename} is already processed, skipping.")

    conn.commit()

except psycopg2.Error as e:
    logging.error(f"Database error: {e}")
    conn.rollback()
finally:
    if 'conn' in locals() and conn:
        conn.close()
        logging.info("Database connection closed.")
