import os
import sys
import psycopg2
import django
from django.conf import settings
import logging
import csv
import zipfile
import tempfile

# Add the project directory to the Python path
sys.path.append('c:/Users/Intern_1/Documents/GitHub/dd_patents_database')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DB_Main.settings')
django.setup()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

directory = 'c:/Users/Intern_1/Documents/PT_Data/PT_disclosure'
table_name = 'patents_pt_disclosure'

def clean_value(value, max_length=None):
    if value is not None:
        value = ''.join(char for char in value if char.isprintable()).strip()
        if max_length:
            value = value[:max_length]
    return value

def update_or_create_record(row, cur, conn):
    query = f"""
    INSERT INTO {table_name} (patent_number_id, disclosure_text_sequence_number, language_of_filing_code, disclosure_text)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (patent_number_id, disclosure_text_sequence_number)
    DO UPDATE SET
    language_of_filing_code = EXCLUDED.language_of_filing_code,
    disclosure_text = EXCLUDED.disclosure_text;
    """
    values = (
        row['Patent Number - Numéro du brevet'],
        row['Disclosure text sequence number - Texte de la divulgation numéro de séquence'],
        row['Language of Filing Code - Langue du type de dépôt'],
        row['Disclosure Text - Texte de la divulgation']
    )
    try:
        cur.execute(query, values)
        conn.commit()
    except Exception as e:
        logging.error(f"Error executing query for patent number {row['Patent Number - Numéro du brevet']}: {e}")
        conn.rollback()

def process_csv_file(csv_path, conn):
    logging.info(f"Processing CSV file: {csv_path}")
    with open(csv_path, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, delimiter='|')
        with conn.cursor() as cur:
            for row in reader:
                try:
                    update_or_create_record(row, cur, conn)
                except Exception as e:
                    logging.error(f"Error processing row in file {csv_path}: {e}")

try:
    conn = psycopg2.connect(
        database=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT']
    )
    logging.info("Database connection established successfully.")

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if filename.endswith('.zip'):
            with tempfile.TemporaryDirectory() as temp_dir:
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                    logging.info(f"Extracted {filename} to temporary directory.")

                    for csv_filename in os.listdir(temp_dir):
                        if csv_filename.endswith('.csv'):
                            csv_path = os.path.join(temp_dir, csv_filename)
                            process_csv_file(csv_path, conn)

    conn.commit()
    logging.info("Import completed successfully.")

except psycopg2.Error as e:
    logging.error(f"Database connection error: {e}")
    if 'conn' in locals():
        conn.rollback()

finally:
    if 'conn' in locals():
        conn.close()
    logging.info("Database connection closed.")
