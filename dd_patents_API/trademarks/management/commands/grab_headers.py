import csv
import os
import zipfile

def list_csv_headers(zip_file_path, extract_to='temp_extracted'):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    
    extracted_files = [f for f in os.listdir(extract_to) if f.lower().endswith('.csv')]
    if not extracted_files:
        print("No CSV files found in the ZIP.")
        return
    
    for csv_filename in extracted_files:
        csv_path = os.path.join(extract_to, csv_filename)
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter='|')
            headers = next(reader)
            print(f"Headers in {csv_filename}:")
            for header in headers:
                print(f" - {header}")
    
    # Clean up extracted files
    for f in extracted_files:
        os.remove(os.path.join(extract_to, f))

if __name__ == "__main__":
    zip_file_path = 'C:/Users/Intern_1/Documents/TM_Data/tm_mark_description_2024-11-20.zip'
    list_csv_headers(zip_file_path)
