import os
import sys
import psycopg2
import django
from django.conf import settings
import csv
import logging
from datetime import datetime
import zipfile
import tempfile

# Add the project directory to the Python path
sys.path.append('c:/Users/Intern_1/Documents/GitHub/dd_patents_database')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DB_Main.settings')
django.setup()

# Directory for ZIP files
directory = 'c:/Users/Intern_1/Documents/PT_Data/PT_interested_party'
table_name = 'pt_interested_party'

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='interested_party_import.log',
    filemode='w'
)

# Increase the field size limit for CSV files
csv.field_size_limit(2**20)

BATCH_SIZE = 1000

def clean_value(value, max_length=None):
    """Clean and truncate values to avoid exceeding database limits."""
    if value is not None:
        value = ''.join(char for char in value if char.isprintable()).strip()
        if max_length:
            value = value[:max_length]
    return value

def parse_date(date_str):
    """Parse date strings into datetime objects or return None for invalid dates."""
    if date_str in ('', 'NULL', None):
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None

def update_or_create_record(row, cur):
    """Insert or update a record in the database."""
    query = f"""
    INSERT INTO {table_name} (
        patent_number_id, agent_type_code, applicant_type_code, interested_party_type_code, 
        interested_party_type, owner_enable_date, ownership_end_date, party_name, 
        party_address_line_1, party_address_line_2, party_address_line_3, party_address_line_4, 
        party_address_line_5, party_city, party_province_code, party_province, 
        party_postal_code, party_country_code, party_country
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (patent_number_id, party_name, owner_enable_date)
    DO UPDATE SET
        agent_type_code = EXCLUDED.agent_type_code,
        applicant_type_code = EXCLUDED.applicant_type_code,
        interested_party_type_code = EXCLUDED.interested_party_type_code,
        interested_party_type = EXCLUDED.interested_party_type,
        ownership_end_date = EXCLUDED.ownership_end_date,
        party_address_line_1 = EXCLUDED.party_address_line_1,
        party_address_line_2 = EXCLUDED.party_address_line_2,
        party_address_line_3 = EXCLUDED.party_address_line_3,
        party_address_line_4 = EXCLUDED.party_address_line_4,
        party_address_line_5 = EXCLUDED.party_address_line_5,
        party_city = EXCLUDED.party_city,
        party_province_code = EXCLUDED.party_province_code,
        party_province = EXCLUDED.party_province,
        party_postal_code = EXCLUDED.party_postal_code,
        party_country_code = EXCLUDED.party_country_code,
        party_country = EXCLUDED.party_country;
    """
    values = (
        clean_value(row['Patent Number - Numéro du brevet'], max_length=50),
        clean_value(row['Agent Type Code - Code du type d\'agent'], max_length=50),
        clean_value(row['Applicant Type Code - Code du type de demandeur'], max_length=50),
        clean_value(row['Interested Party Type Code - Code du type de partie intéressée'], max_length=10),
        clean_value(row['Interested Party Type - Type de partie intéressée'], max_length=50),
        parse_date(row['Owner Enable Date - Date d’activation par le propriétaire']),
        parse_date(row['Ownership End date - Date de désactivation par le propriétaire']),
        clean_value(row['Party Name - Nom de la partie'], max_length=255),
        clean_value(row['Party Address Line 1 - Ligne 1 de l\'adresse de la partie'], max_length=255),
        clean_value(row['Party Address Line 2 - Ligne 2 de l\'adresse de la partie'], max_length=255),
        clean_value(row['Party Address Line 3 - Ligne 3 de l\'adresse de la partie'], max_length=255),
        clean_value(row['Party Address Line 4 - Ligne 4 de l\'adresse de la partie'], max_length=255),
        clean_value(row['Party Address Line 5 - Ligne 5 de l\'adresse de la partie'], max_length=255),
        clean_value(row['Party City - Ville de la partie'], max_length=100),
        clean_value(row['Party Province Code - Code de la province de la partie'], max_length=10),
        clean_value(row['Party Province - Étiquette de la province de la partie'], max_length=100),
        clean_value(row['Party Postal Code - Code postal de la partie'], max_length=20),
        clean_value(row['Party Country Code - Code du pays de la partie'], max_length=2),
        clean_value(row['Party Country - Pays de la partie'], max_length=100),
    )
    cur.execute(query, values)

def process_csv_file(csv_path, conn):
    """Process a single CSV file."""
    logging.info(f"Processing CSV file: {csv_path}")
    with open(csv_path, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, delimiter='|')
        with conn.cursor() as cur:
            batch = []
            skipped_rows = 0
            for row in reader:
                try:
                    batch.append(row)
                    if len(batch) == BATCH_SIZE:
                        insert_batch(batch, cur)
                        conn.commit()
                        batch = []
                except psycopg2.errors.ForeignKeyViolation as e:
                    skipped_rows += 1
                    logging.warning(f"Skipped row due to foreign key violation: {row}. Error: {e}")
                except Exception as e:
                    logging.error(f"Error processing row: {e}")
            if batch:
                insert_batch(batch, cur)
                conn.commit()
            logging.info(f"CSV file processed. Skipped rows: {skipped_rows}")

def insert_batch(batch, cur):
    """Insert a batch of records."""
    for row in batch:
        try:
            update_or_create_record(row, cur)
        except psycopg2.errors.ForeignKeyViolation as e:
            logging.warning(f"Foreign key violation for row: {row}. Error: {e}")
        except Exception as e:
            logging.error(f"Error processing row: {e}")

def process_zip_file(zip_path, conn):
    """Process a ZIP file containing CSVs."""
    logging.info(f"Processing ZIP file: {zip_path}")
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
            logging.info(f"Extracted {zip_path} to temporary directory.")
            for csv_filename in os.listdir(temp_dir):
                if csv_filename.endswith('.csv'):
                    csv_path = os.path.join(temp_dir, csv_filename)
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
        if filename.endswith('.zip'):
            process_zip_file(filepath, conn)
        elif filename.endswith('.csv'):
            process_csv_file(filepath, conn)

    logging.info("Import process completed successfully.")

except psycopg2.Error as e:
    logging.error(f"Database connection error: {e}")
finally:
    if 'conn' in locals() and conn:
        conn.close()
        logging.info("Database connection closed.")
