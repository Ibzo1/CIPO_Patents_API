import os
import sys
import psycopg2
import django
from django.conf import settings
import csv
import logging
import zipfile
import tempfile

# Add the project directory to the Python path
sys.path.append('c:/Users/Intern_1/Documents/GitHub/dd_patents_database')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DB_Main.settings')
django.setup()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

directory = 'c:/Users/Intern_1/Documents/PT_Data/PT_abstract'
table_name = 'patents_pt_abstract'

# Logs to track progress
processed_files_log = 'processed_abstract_files.log'
processed_rows_log = 'processed_abstract_rows.log'

def is_file_processed(filename):
    """Check if a file has been processed by reading the log file."""
    if not os.path.exists(processed_files_log):
        return False
    with open(processed_files_log, 'r') as f:
        processed_files = f.read().splitlines()
    return filename in processed_files

def mark_file_processed(filename):
    """Mark a file as processed by writing to the log file."""
    with open(processed_files_log, 'a') as f:
        f.write(f"{filename}\n")

def get_last_processed_row(filename):
    """Retrieve the last processed row number for a given file."""
    if not os.path.exists(processed_rows_log):
        return 0
    with open(processed_rows_log, 'r') as f:
        for line in f:
            log_filename, last_row = line.strip().split(',')
            if log_filename == filename:
                return int(last_row)
    return 0

def mark_row_processed(filename, row_number):
    """Update the last processed row number for a given file."""
    lines = []
    if os.path.exists(processed_rows_log):
        with open(processed_rows_log, 'r') as f:
            lines = f.readlines()

    with open(processed_rows_log, 'w') as f:
        updated = False
        for line in lines:
            log_filename, last_row = line.strip().split(',')
            if log_filename == filename:
                f.write(f"{filename},{row_number}\n")
                updated = True
            else:
                f.write(line)
        if not updated:
            f.write(f"{filename},{row_number}\n")

def clean_value(value, max_length=None):
    if value is not None:
        value = ''.join(char for char in value if char.isprintable()).strip()
        if max_length:
            value = value[:max_length]
    return value

def update_or_create_record(row, cur, conn):
    query = f"""
    INSERT INTO patents_pt_abstract (patent_number_id, abstract_text_sequence_number, language_of_filing_code, abstract_language_code, abstract_text)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (patent_number_id, abstract_text_sequence_number)
    DO UPDATE SET
    language_of_filing_code = EXCLUDED.language_of_filing_code,
    abstract_language_code = EXCLUDED.abstract_language_code,
    abstract_text = EXCLUDED.abstract_text;
    """
    values = (
        row['Patent Number - Numéro du brevet'],
        row['Abstract text sequence number - Texte de l’abrégé numéro de séquence'],
        row['Language of Filing Code - Langue du type de dépôt'],
        row['Abstract Language Code - Code de la langue du résumé'],
        row['Abstract Text - Texte de l’abrégé']
    )
    try:
        cur.execute(query, values)
        conn.commit()
    except Exception as e:
        logging.error(f"Error executing query for patent number {row['Patent Number - Numéro du brevet']}: {e}")
        conn.rollback()

try:
    conn = psycopg2.connect(
        database=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT']
    )
    logging.info("Database connection established successfully.")

    csv.field_size_limit(10 * 1024 * 1024)  # Increase the CSV field size limit

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if is_file_processed(filename):
            logging.info(f"Skipping already processed file: {filename}")
            continue

        last_processed_row = get_last_processed_row(filename)

        if filename.endswith('.zip'):
            with tempfile.TemporaryDirectory() as temp_dir:
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                    logging.info(f"Extracted {filename} to temporary directory.")

                    for csv_filename in os.listdir(temp_dir):
                        if csv_filename.endswith('.csv'):
                            csv_path = os.path.join(temp_dir, csv_filename)
                            logging.info(f"Processing CSV file: {csv_path}")
                            with open(csv_path, 'r', encoding='utf-8') as infile:
                                reader = csv.DictReader(infile, delimiter='|')
                                with conn.cursor() as cur:
                                    for row_number, row in enumerate(reader, start=1):
                                        if row_number <= last_processed_row:
                                            continue  # Skip rows already processed
                                        update_or_create_record(row, cur, conn)
                                        mark_row_processed(filename, row_number)

            mark_file_processed(filename)

        elif filename.endswith('.csv'):
            logging.info(f"Processing standalone CSV file: {filepath}")
            with open(filepath, 'r', encoding='utf-8') as infile:
                reader = csv.DictReader(infile, delimiter='|')
                with conn.cursor() as cur:
                    for row_number, row in enumerate(reader, start=1):
                        if row_number <= last_processed_row:
                            continue  # Skip rows already processed
                        update_or_create_record(row, cur, conn)
                        mark_row_processed(filename, row_number)

            mark_file_processed(filename)

    conn.commit()
    logging.info("Import completed successfully.")

except psycopg2.Error as e:
    logging.error(f"Database error: {e}")
    if 'conn' in locals():
        conn.rollback()
finally:
    if 'conn' in locals():
        conn.close()
        logging.info("Database connection closed.")
