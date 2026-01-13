import zipfile
import csv
import random
import os

# Paths to your ZIP file and the desired output location for the smaller CSV
zip_file_path = 'c:/Users/Intern_1/Documents/PT_Data/PT_priority_claim/PT_priority_claim_1_to_2000000_2024-10-11.zip'
output_csv_path = 'c:/Users/Intern_1/Documents/PT_Data/PT_priority_claim/sampled_30_rows.csv'
extract_to_dir = 'c:/Users/Intern_1/Documents/PT_Data/PT_priority_claim/extracted'

def extract_csv_from_zip(zip_path, extract_to):
    """Extract the first CSV file found in the ZIP archive."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            # Find the first CSV file in the extracted files
            csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]
            if not csv_files:
                raise FileNotFoundError("No CSV file found in the ZIP archive.")
            csv_file = csv_files[0]
            extracted_csv_path = os.path.join(extract_to, csv_file)
            print(f"Extracted CSV file: {extracted_csv_path}")
            return extracted_csv_path
    except zipfile.BadZipFile:
        print(f"Error: The file {zip_path} is not a valid ZIP archive.")
        raise
    except Exception as e:
        print(f"An error occurred while extracting the ZIP file: {e}")
        raise

def sample_csv(input_path, output_path, sample_size=30):
    """Sample specified number of rows from the input CSV and save to a new CSV."""
    try:
        with open(input_path, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile, delimiter='|')
            rows = []
            for row in reader:
                # Ensure all fields are present
                if None in row or any(field is None for field in row.values()):
                    print(f"Skipping row with missing fields: {row}")
                    continue
                rows.append(row)
            
            if len(rows) < sample_size:
                print(f"Warning: Requested sample size {sample_size} is greater than available rows {len(rows)}.")
                sampled_rows = rows
            else:
                sampled_rows = random.sample(rows, sample_size)
            
            with open(output_path, mode='w', newline='', encoding='utf-8') as outfile:
                fieldnames = reader.fieldnames
                writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='|')
                writer.writeheader()
                writer.writerows(sampled_rows)
            
            print(f"Sampled {len(sampled_rows)} rows and saved to {output_path}")
    except FileNotFoundError:
        print(f"Error: The file {input_path} does not exist.")
        raise
    except ValueError as ve:
        print(f"ValueError: {ve}")
        raise
    except Exception as e:
        print(f"An error occurred while sampling the CSV file: {e}")
        raise

def main():
    # Ensure the extraction directory exists
    os.makedirs(extract_to_dir, exist_ok=True)
    
    # Extract the CSV file from the ZIP
    try:
        extracted_csv_path = extract_csv_from_zip(zip_file_path, extract_to_dir)
    except Exception as e:
        print("Failed to extract CSV from ZIP.")
        return
    
    # Sample 30 rows from the extracted CSV
    try:
        sample_csv(extracted_csv_path, output_csv_path, sample_size=30)
    except Exception as e:
        print("Failed to sample CSV.")
        return

if __name__ == "__main__":
    main()
