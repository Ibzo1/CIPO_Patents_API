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
table_name = 'patents_pt_priority_claim'

# Define the mapping from CSV headers to database columns
COLUMN_MAPPING = {
    'Patent Number - Numéro du brevet': 'patent_number_id',
    'Foreign Application/Patent Number - Numéro du brevet étranger / national': 'foreign_application_patent_number',
    'Priority Claim Kind Code - Code de type de revendications de priorité': 'priority_claim_kind_code',
    "Priority Claim Country Code - Code du pays d'origine de revendications de priorité": 'priority_claim_country_code',
    "Priority Claim Country - Pays d'origine de revendications de priorité": 'priority_claim_country',
    'Priority Claim Calendar Dt - Date de revendications de priorité': 'priority_claim_calendar_dt'
}

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_value(value, max_length=None):
    """Clean the value by stripping whitespace and removing non-printable characters. Optionally trim to max_length."""
    if value is not None:
        value = ''.join(char for char in value if char.isprintable()).strip()
        if max_length:
            value = value[:max_length]
    return value

def process_chunk(chunk, conn):
    temp_chunk_file = 'temp_chunk.csv'
    with open(temp_chunk_file, 'w', encoding='utf-8', newline='') as temp_file:
        # Use the mapped column names for the database
        writer = csv.DictWriter(temp_file, fieldnames=COLUMN_MAPPING.values(), delimiter='|')
        writer.writeheader()
        for row in chunk:
            # Rename the keys according to the COLUMN_MAPPING
            mapped_row = {db_col: row[csv_col] for csv_col, db_col in COLUMN_MAPPING.items()}
            writer.writerow(mapped_row)

    import_rows(temp_chunk_file, conn)

def import_rows(file_path, conn):
    with open(file_path, 'r', encoding='utf-8') as temp_file:
        try:
            with conn.cursor() as cur:
                logging.info(f"Starting bulk copy for {file_path}")
                # Specify the columns in the COPY command
                copy_command = f"""
                COPY {table_name} (patent_number_id, foreign_application_patent_number, priority_claim_kind_code, 
                priority_claim_country_code, priority_claim_country, priority_claim_calendar_dt) 
                FROM STDIN WITH CSV HEADER DELIMITER '|' NULL 'NULL'
                """
                cur.copy_expert(copy_command, temp_file)
                conn.commit()
                logging.info(f"Successfully copied data from {file_path}")
        except psycopg2.errors.UniqueViolation as e:
            logging.warning(f"Duplicate key error encountered: {e}. Attempting to update existing records.")
            conn.rollback()
            with conn.cursor() as cur:
                temp_file.seek(0)
                reader = csv.DictReader(temp_file, delimiter='|')
                for row in reader:
                    update_or_create_record(row, cur, conn)
        except psycopg2.Error as e:
            logging.error(f"Error during bulk copy: {e}")
            conn.rollback()
            with conn.cursor() as cur:
                temp_file.seek(0)
                reader = csv.DictReader(temp_file, delimiter='|')
                for row in reader:
                    try:
                        update_or_create_record(row, cur, conn)
                    except psycopg2.Error as inner_e:
                        logging.error(f"Error updating/creating record for patent number {row['patent_number_id']}: {inner_e}")
            conn.commit()

def update_or_create_record(row, cur, conn):
    query = f"""
    INSERT INTO {table_name} (patent_number_id, foreign_application_patent_number, priority_claim_kind_code, 
    priority_claim_country_code, priority_claim_country, priority_claim_calendar_dt)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (patent_number_id, foreign_application_patent_number)
    DO UPDATE SET
    priority_claim_kind_code = EXCLUDED.priority_claim_kind_code,
    priority_claim_country_code = EXCLUDED.priority_claim_country_code,
    priority_claim_country = EXCLUDED.priority_claim_country,
    priority_claim_calendar_dt = EXCLUDED.priority_claim_calendar_dt;
    """
    values = (
        row['patent_number_id'],
        row['foreign_application_patent_number'],
        row['priority_claim_kind_code'],
        row['priority_claim_country_code'],
        row['priority_claim_country'],
        row['priority_claim_calendar_dt']
    )
    try:
        logging.info(f"Executing query for patent number {row['patent_number_id']} with values {values}")
        cur.execute(query, values)
        conn.commit()
    except Exception as e:
        logging.error(f"Error executing query for patent number {row['patent_number_id']}: {e}")
        conn.rollback()

def preprocess_and_import_csv(file_path, conn, chunk_size=1000):
    with open(file_path, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, delimiter='|')
        chunk = []
        for i, row in enumerate(reader, start=1):
            # Clean and map the row
            mapped_row = {}
            for csv_col, db_col in COLUMN_MAPPING.items():
                value = row[csv_col]
                if 'date' in csv_col.lower() and value in ['NULL', '-1', '']:
                    value = ''
                mapped_row[db_col] = clean_value(value, max_length=50 if db_col == 'foreign_application_patent_number' else None)
            # Validate mandatory fields
            if not mapped_row['patent_number_id']:
                logging.warning(f"Missing patent_number_id in row {i}. Skipping.")
                continue
            chunk.append(mapped_row)
            if i % chunk_size == 0:
                logging.info(f"Processing and importing rows {i - chunk_size + 1} to {i}")
                process_chunk(chunk, conn)
                chunk = []
        if chunk:
            logging.info(f"Processing and importing rows {i - len(chunk) + 1} to {i}")
            process_chunk(chunk, conn)

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
