import os
import zipfile
import pandas as pd
import tempfile
import logging

# Directory containing ZIP files
directory = 'c:/Users/Intern_1/Documents/PT_Data/PT_ipc'

# Output CSV file for inspection
output_csv = 'c:/Users/Intern_1/Documents/PT_Data/sample_output.csv'

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_zip_file(zip_file):
    """Extract and process CSV file from the ZIP."""
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
            logging.info(f"Extracted {zip_file} to temporary directory.")
            
            for csv_filename in os.listdir(temp_dir):
                if csv_filename.endswith('.csv'):
                    csv_path = os.path.join(temp_dir, csv_filename)
                    logging.info(f"Processing CSV file: {csv_path}")
                    process_csv_file(csv_path)

def process_csv_file(csv_file):
    """Display or save first 30 rows of the CSV."""
    try:
        # Load CSV into a pandas DataFrame
        df = pd.read_csv(csv_file, delimiter='|', encoding='utf-8', nrows=30)
        
        # Display in terminal
        print("First 30 rows of the CSV:")
        print(df.to_string(index=False))
        
        # Save to a new CSV file
        df.to_csv(output_csv, index=False)
        logging.info(f"Saved first 30 rows to {output_csv}.")
    except Exception as e:
        logging.error(f"Error processing file {csv_file}: {e}")

def process_directory(directory):
    """Process all ZIP files in the directory."""
    for filename in os.listdir(directory):
        if filename.endswith('.zip'):
            zip_path = os.path.join(directory, filename)
            process_zip_file(zip_path)

# Main execution
if __name__ == "__main__":
    try:
        process_directory(directory)
    except Exception as e:
        logging.error(f"Error: {e}")
