import os
import sys
import psycopg2
import django
from django.conf import settings
import csv
import logging

# Add the project directory to the Python path
sys.path.append('C:/Users/azhari/Desktop/DB_Main')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DB_Main.settings')
django.setup()

directory = 'c:/Users/azhari/OneDrive - ISED-ISDE/Documents/PT_All/PT_claim'
table_name = 'patents_pt_claim'

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_value(value, max_length=None):
    """Clean the value by stripping whitespace and removing non-printable characters. Optionally trim to max_length."""
    if value is not None:
        value = ''.join(char for char in value if char.isprintable()).strip()
        if max_length:
            value = value[:max_length]
    return value

def preprocess_and_import_csv(input_file, conn, chunk_size=1000):
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, delimiter='|')
        fieldnames = reader.fieldnames
        
        chunk = []
        row_count = 0
        
        for row in reader:
            for key in row:
                if 'date' in key.lower() and row[key] in ['NULL', '-1', '']:
                    row[key] = ''
                if key == 'Language of Filing Code - Langue du type de dépôt':
                    row[key] = clean_value(row[key], max_length=2)
            chunk.append(row)
            row_count += 1
            
            if row_count % chunk_size == 0:
                logging.info(f"Processing and importing rows {row_count-chunk_size+1} to {row_count}")
                process_chunk(chunk, conn)
                chunk = []
        
        if chunk:
            logging.info(f"Processing and importing rows {row_count-len(chunk)+1} to {row_count}")
            process_chunk(chunk, conn)

def process_chunk(chunk, conn):
    with open('temp_chunk.csv', 'w', encoding='utf-8', newline='') as temp_file:
        fieldnames = chunk[0].keys()
        writer = csv.DictWriter(temp_file, fieldnames=fieldnames, delimiter='|')
        writer.writeheader()
        for row in chunk:
            writer.writerow(row)
    
    import_rows('temp_chunk.csv', conn)

def import_rows(file_path, conn):
    with open(file_path, 'r', encoding='utf-8') as temp_file:
        try:
            with conn.cursor() as cur:
                logging.info(f"Starting bulk copy for {file_path}")
                cur.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV HEADER DELIMITER '|' NULL 'NULL'", temp_file)
                logging.info(f"Successfully copied data from {file_path}")
        except psycopg2.errors.UniqueViolation as e:
            logging.warning(f"Duplicate key error encountered: {e}. Attempting to update existing records.")
            conn.rollback()
            with conn.cursor() as cur:
                temp_file.seek(0)
                reader = csv.DictReader(temp_file, delimiter='|')
                for row in reader:
                    update_or_create_record(row, cur)
            conn.commit()
        except psycopg2.Error as e:
            logging.error(f"Error during bulk copy: {e}")
            conn.rollback()
            with conn.cursor() as cur:
                temp_file.seek(0)
                reader = csv.DictReader(temp_file, delimiter='|')
                for row in reader:
                    try:
                        update_or_create_record(row, cur)
                    except psycopg2.Error as inner_e:
                        logging.error(f"Error updating/creating record: {inner_e}")
            conn.commit()

def update_or_create_record(row, cur):
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
    logging.info(f"Executing query for patent number {row['Patent Number - Numéro du brevet']} ") #with values {value}
    cur.execute(query, values)

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
            logging.info(f"Preprocessing file: {filepath}")
            preprocess_and_import_csv(filepath, conn)
    
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
