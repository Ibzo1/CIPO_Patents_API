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

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='claims_import.log')

directory = 'c:/Users/Intern_1/Documents/PT_Data/PT_claim'
table_name = 'patents_pt_claim'
processed_zips = set()

# Increase CSV field size limit, handle errors if too large
try:
    csv.field_size_limit(10 * 1024 * 1024)
except OverflowError:
    csv.field_size_limit(sys.maxsize // 2)

def clean_value(value, max_length=None):
    if value is not None:
        value = ''.join(char for char in value if char.isprintable()).strip()
        if max_length:
            value = value[:max_length]
    return value

def update_or_create_record(row, cur, conn):
    query = f"""
    INSERT INTO {table_name} (patent_number_id, claim_text_sequence_number, language_of_filing_code, claims_text)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (patent_number_id, claim_text_sequence_number)
    DO UPDATE SET
    language_of_filing_code = EXCLUDED.language_of_filing_code,
    claims_text = EXCLUDED.claims_text;
    """
    values = (
        row['Patent Number - Numéro du brevet'],
        row['Claim text sequence number - Texte des revendications numéro de séquence'],
        row['Language of Filing Code - Langue du type de dépôt'],
        row['Claims Text - Texte des revendications']
    )
    cur.execute(query, values)

def process_csv_file(file_path, conn):
    with open(file_path, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, delimiter='|')
        with conn.cursor() as cur:
            for row in reader:
                update_or_create_record(row, cur, conn)
    conn.commit()

def process_zip(zip_path, conn):
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
            logging.info(f"Extracted {zip_path}")
            for csv_filename in os.listdir(temp_dir):
                if csv_filename.endswith('.csv'):
                    csv_path = os.path.join(temp_dir, csv_filename)
                    logging.info(f"Processing CSV: {csv_path}")
                    process_csv_file(csv_path, conn)

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
        filepath = os.path.join(directory, filename)
        if filename.endswith('.zip') and filename not in processed_zips:
            try:
                logging.info(f"Processing ZIP: {filename}")
                process_zip(filepath, conn)
                processed_zips.add(filename)  # Mark ZIP as processed
            except Exception as e:
                logging.error(f"Error processing {filename}: {e}")
                conn.rollback()

    logging.info("Claims import completed successfully.")

except psycopg2.Error as e:
    logging.error(f"Database connection error: {e}")

finally:
    if 'conn' in locals():
        conn.close()
        logging.info("Database connection closed.")
