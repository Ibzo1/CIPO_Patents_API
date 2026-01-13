import os
import sys
import psycopg2
import django
from django.conf import settings
import csv
import logging
from datetime import datetime
from ..utils import clean_value, preprocess_and_import_csv

# Add the project directory to the Python path
sys.path.append('C:/Users/azhari/Desktop/DB_Main')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DB_Main.settings')
django.setup()

directory = 'c:/Users/azhari/OneDrive - ISED-ISDE/Documents/PT_All/PT_claim'
table_name = 'pt_interested_party'

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_date(date_str):
    if date_str in ('', 'NULL', None):
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None

def update_or_create_record(row, cur, conn):
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
        row['Patent Number - Numéro du brevet'],
        row['Agent Type Code - Code du type d\'agent'],
        row['Applicant Type Code - Code du type de demandeur'],
        row['Interested Party Type Code - Code du type de partie intéressée'],
        row['Interested Party Type - Type de partie intéressée'],
        parse_date(row['Owner Enable Date - Date d’activation par le propriétaire']),
        parse_date(row['Ownership End date - Date de désactivation par le propriétaire']),
        row['Party Name - Nom de la partie'],
        row['Party Address Line 1 - Ligne 1 de l\'adresse de la partie'],
        row['Party Address Line 2 - Ligne 2 de l\'adresse de la partie'],
        row['Party Address Line 3 - Ligne 3 de l\'adresse de la partie'],
        row['Party Address Line 4 - Ligne 4 de l\'adresse de la partie'],
        row['Party Address Line 5 - Ligne 5 de l\'adresse de la partie'],
        row['Party City - Ville de la partie'],
        row['Party Province Code - Code de la province de la partie'],
        row['Party Province - Étiquette de la province de la partie'],
        row['Party Postal Code - Code postal de la partie'],
        row['Party Country Code - Code du pays de la partie'],
        row['Party Country - Pays de la partie']
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
            logging.info(f"Preprocessing file: {filepath}")
            preprocess_and_import_csv(
                filepath, 
                conn, 
                table_name, 
                update_or_create_record, 
                [
                    'Patent Number - Numéro du brevet',
                    'Agent Type Code - Code du type d\'agent',
                    'Applicant Type Code - Code du type de demandeur',
                    'Interested Party Type Code - Code du type de partie intéressée',
                    'Interested Party Type - Type de partie intéressée',
                    'Owner Enable Date - Date d’activation par le propriétaire',
                    'Ownership End date - Date de désactivation par le propriétaire',
                    'Party Name - Nom de la partie',
                    'Party Address Line 1 - Ligne 1 de l\'adresse de la partie',
                    'Party Address Line 2 - Ligne 2 de l\'adresse de la partie',
                    'Party Address Line 3 - Ligne 3 de l\'adresse de la partie',
                    'Party Address Line 4 - Ligne 4 de l\'adresse de la partie',
                    'Party Address Line 5 - Ligne 5 de l\'adresse de la partie',
                    'Party City - Ville de la partie',
                    'Party Province Code - Code de la province de la partie',
                    'Party Province - Étiquette de la province de la partie',
                    'Party Postal Code - Code postal de la partie',
                    'Party Country Code - Code du pays de la partie',
                    'Party Country - Pays de la partie'
                ]
            )

except psycopg2.Error as e:
    logging.error(f"Error connecting to the database: {e}")
    if 'conn' in locals():
        conn.rollback()

finally:
    # Close the connection in the finally block
    if 'conn' in locals():
        conn.close()

logging.info('Import completed successfully')
