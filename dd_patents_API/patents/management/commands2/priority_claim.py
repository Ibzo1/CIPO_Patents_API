import os
import sys
import psycopg2
import django
from django.conf import settings
import logging
import csv
import zipfile
import io

# Add the project directory to the Python path
sys.path.append('c:/Users/Intern_1/Documents/GitHub/dd_patents_database')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DB_Main.settings')
django.setup()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

directory = 'c:/Users/Intern_1/Documents/PT_Data/PT_priority_claim'  # directory containing the zips
table_name = 'patents_pt_priority_claim'  # update with your actual table name

# Database connection function (using settings from Django)
def connect_db():
    try:
        conn = psycopg2.connect(
            database=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )
        logging.info("Database connection established.")
        return conn
    except Exception as e:
        logging.error(f"Error establishing database connection: {e}")
        return None

# Function to clean values before inserting
def clean_value(value, max_length=None):
    if value is not None:
        value = ''.join(char for char in value if char.isprintable()).strip()
        if max_length:
            value = value[:max_length]
    return value

# Function to update or create records in the database
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
        clean_value(row['Patent Number - Numéro du brevet']),
        clean_value(row['Foreign Application/Patent Number - Numéro du brevet étranger / national']),
        clean_value(row['Priority Claim Kind Code - Code de type de revendications de priorité']),
        clean_value(row['Priority Claim Country Code - Code du pays d\'origine de revendications de priorité']),
        clean_value(row['Priority Claim Country - Pays d\'origine de revendications de priorité']),
        clean_value(row['Priority Claim Calendar Dt - Date de revendications de priorité'])
    )
    try:
        cur.execute(query, values)
        conn.commit()
    except Exception as e:
        logging.error(f"Error executing query for patent number {row['Patent Number - Numéro du brevet']}: {e}")
        conn.rollback()

# Function to process CSV file inside the zip
def process_zip_file(zip_path, conn):
    logging.info(f"Processing ZIP file: {zip_path}")
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        csv_files = zip_ref.namelist()
        for csv_file in csv_files:
            logging.info(f"Processing CSV file: {csv_file}")
            
            # Open the CSV file within the zip file and decode it to text
            with zip_ref.open(csv_file) as infile:
                with io.TextIOWrapper(infile, encoding='utf-8') as text_file:
                    reader = csv.DictReader(text_file, delimiter='|')
                    with conn.cursor() as cur:
                        for row in reader:
                            if all(field in row for field in ['Patent Number - Numéro du brevet', 'Foreign Application/Patent Number - Numéro du brevet étranger / national']):
                                try:
                                    update_or_create_record(row, cur, conn)
                                except Exception as e:
                                    logging.error(f"Error processing row: {e}")
                            else:
                                logging.warning(f"Skipping row with missing required fields: {row}")
                conn.commit()  # Commit after processing the batch

# Main function to process all zip files in the directory
def process_all_zips(directory, conn):
    for filename in os.listdir(directory):
        if filename.endswith('.zip'):
            zip_path = os.path.join(directory, filename)
            logging.info(f"Starting processing for {zip_path}")
            process_zip_file(zip_path, conn)

# Entry point for the script
if __name__ == "__main__":
    conn = connect_db()
    if conn:
        try:
            process_all_zips(directory, conn)
        except Exception as e:
            logging.error(f"Error processing zip files: {e}")
        finally:
            conn.close()
            logging.info("Database connection closed.")
    else:
        logging.error("Failed to establish database connection.")
