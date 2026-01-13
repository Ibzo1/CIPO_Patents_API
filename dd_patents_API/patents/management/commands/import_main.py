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
table_name = 'patents_pt_main'

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.DictReader(infile, delimiter='|')
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='|')
        writer.writeheader()
        
        for row in reader:
            for key in row:
                if 'date' in key.lower() and row[key] in ['NULL', '-1', '']:
                    logging.info(f"Replacing invalid date value in {key} from {row[key]} to ''")
                    row[key] = ''
            writer.writerow(row)

try:
    # Establish a connection to the PostgreSQL database using Django settings
    conn = psycopg2.connect(
        database=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT']
    )

    # Create a cursor
    cur = conn.cursor()

    # Increase the field size limit
    cur.execute("SET work_mem TO '50MB'")

    # List CSV files in the directory, preprocess, and copy them into the table
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)
            preprocessed_filepath = filepath.replace('.csv', '_preprocessed.csv')
            logging.info(f"Preprocessing file: {filepath}")
            preprocess_csv(filepath, preprocessed_filepath)
            
            with open(preprocessed_filepath, 'r', encoding='utf-8') as csv_file:
                try:
                    cur.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV HEADER DELIMITER '|' NULL 'NULL'", csv_file)
                    logging.info(f"Successfully copied data from {preprocessed_filepath}")
                except psycopg2.Error as e:
                    logging.error(f"Error copying data from {preprocessed_filepath}: {e}")
    
    # Commit the changes and close the connection
    conn.commit()

except psycopg2.Error as e:
    logging.error(f"Error connecting to the database: {e}")

finally:
    # Close the cursor and connection in the finally block
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()
