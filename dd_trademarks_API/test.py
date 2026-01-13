import os
import sys
import zipfile
import csv
import logging
import io
from collections import defaultdict
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data_assessment.log"),
        logging.StreamHandler()
    ]
)

def assess_csv_file(csv_file, filename):
    """
    Assess the structure and data quality of a single CSV file.
    """
    logging.info(f"Assessing CSV file: {filename}")
    reader = csv.DictReader(csv_file, delimiter='|')
    headers = reader.fieldnames
    logging.info(f"Headers: {headers}")

    # Initialize metrics
    total_rows = 0
    null_counts = defaultdict(int)
    unique_values = defaultdict(set)
    data_types = defaultdict(set)

    for row in reader:
        total_rows += 1
        for header in headers:
            value = row.get(header, '').strip()
            if value == '':
                null_counts[header] += 1
            else:
                unique_values[header].add(value)
                # Infer data type
                if header.lower().endswith('dt') or 'date' in header.lower():
                    try:
                        datetime.strptime(value, '%Y-%m-%d')
                        data_types[header].add('date')
                    except ValueError:
                        data_types[header].add('string')
                elif value.isdigit():
                    data_types[header].add('int')
                else:
                    try:
                        float(value)
                        data_types[header].add('float')
                    except ValueError:
                        data_types[header].add('string')

    # Log assessment results
    logging.info(f"Total Rows: {total_rows}")
    logging.info("Null/Missing Values per Column:")
    for header in headers:
        logging.info(f"  {header}: {null_counts[header]}")

    logging.info("Unique Values per Column (Sample up to 10):")
    for header in headers:
        sample = list(unique_values[header])[:10]
        logging.info(f"  {header}: {sample} ... ({len(unique_values[header])} unique)")

    logging.info("Inferred Data Types per Column:")
    for header in headers:
        types = ', '.join(data_types[header]) if data_types[header] else 'Unknown'
        logging.info(f"  {header}: {types}")

    logging.info("-" * 50)

def assess_data(directory):
    """
    Assess all CSV files within ZIP archives in the specified directory.
    """
    logging.info(f"Starting data assessment in directory: {directory}")

    for filename in os.listdir(directory):
        if filename.endswith('.zip'):
            zip_path = os.path.join(directory, filename)
            logging.info(f"Processing ZIP file: {zip_path}")
            try:
                with zipfile.ZipFile(zip_path, 'r') as z:
                    for csv_filename in z.namelist():
                        if csv_filename.endswith('.csv'):
                            logging.info(f"Extracting and assessing CSV file: {csv_filename}")
                            with z.open(csv_filename) as csv_file_binary:
                                # Wrap the binary stream with TextIOWrapper for text processing
                                csv_file_text = io.TextIOWrapper(csv_file_binary, encoding='utf-8')
                                assess_csv_file(csv_file_text, csv_filename)
            except zipfile.BadZipFile:
                logging.error(f"Bad ZIP file: {zip_path}")
            except Exception as e:
                logging.error(f"Error processing ZIP file {zip_path}: {e}")

    logging.info("Data assessment completed.")

if __name__ == "__main__":
    # Define the directory containing the ZIP files
    directory = 'c:/Users/Intern_1/Documents/PT_Data/PT_priority_claim'
    
    # Check if the directory exists
    if not os.path.isdir(directory):
        logging.error(f"The directory {directory} does not exist.")
        sys.exit(1)
    
    # Run the data assessment
    assess_data(directory)
