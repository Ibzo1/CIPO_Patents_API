import os
import sys
import psycopg2
import django
from django.conf import settings
import logging
import csv
from ..utils import clean_value, preprocess_and_import_csv

# Add the project directory to the Python path
sys.path.append('C:/Users/azhari/Desktop/DB_Main')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DB_Main.settings')
django.setup()

directory = r'c:\\Users\\azhari\\OneDrive - ISED-ISDE\\Documents\\PT_All\\PT_disclosure'
table_name = 'patents_pt_disclosure'

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        logging.info(f"Executing query for patent number {row['Patent Number - Numéro du brevet']} with values {values}")
        cur.execute(query, values)
        conn.commit()
    except Exception as e:
        logging.error(f"Error executing query for patent number {row['Patent Number - Numéro du brevet']}: {e}")
        conn.rollback()

try:
    # Establish a connection to the PostgreSQL database using Django settings
    conn = psycopg2.connect(
        database=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT']
    )

    # Increase the field size limit
    csv.field_size_limit(10 * 1024 * 1024)  # 10 MB

    # List CSV files in the directory, preprocess, and import them
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)
            logging.info(f"Preprocessing and importing file: {filepath}")
            preprocess_and_import_csv(filepath, conn, table_name, update_or_create_record, 
                                      ['Patent Number - Numéro du brevet', 
                                       'Disclosure text sequence number - Texte de la divulgation numéro de séquence', 
                                       'Language of Filing Code - Langue du type de dépôt', 
                                       'Disclosure Text - Texte de la divulgation'],
                                      chunk_size=1000)
    
    # Commit the changes and close the connection
    conn.commit()

except psycopg2.Error as e:
    logging.error(f"Error connecting to the database: {e}")
    if 'conn' in locals():
        conn.rollback()

finally:
    # Close the connection in the finally block
    if 'conn' in locals():
        conn.close()

logging.info('Import completed successfully')
