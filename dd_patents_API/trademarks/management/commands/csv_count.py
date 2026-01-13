import os
import csv
import zipfile

def count_rows_in_zip(zip_file_path, temp_extract_dir):
    # Ensure the temporary directory exists
    os.makedirs(temp_extract_dir, exist_ok=True)
    
    # Extract the ZIP file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_extract_dir)
    
    # Find all CSV files in the temporary directory
    csv_files = [f for f in os.listdir(temp_extract_dir) if f.lower().endswith('.csv')]
    total_rows = 0

    for csv_filename in csv_files:
        csv_path = os.path.join(temp_extract_dir, csv_filename)
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter='|')
            header = next(reader, None)  # Skip header row
            row_count = sum(1 for row in reader)
            print(f"{csv_filename}: {row_count} rows (excluding header)")
            total_rows += row_count

    print(f"Total rows in all CSV files: {total_rows}")

    # Clean up: delete extracted CSV files
    for csv_filename in csv_files:
        os.remove(os.path.join(temp_extract_dir, csv_filename))

if __name__ == "__main__":
    # Update this path to point to your ZIP file
    zip_file_path = 'C:/Users/Intern_1/Documents/TM_Data/TM_mark_description.zip'
    temp_extract_dir = 'C:/Users/Intern_1/Documents/TM_Data/temp_extracted'
    
    count_rows_in_zip(zip_file_path, temp_extract_dir)
