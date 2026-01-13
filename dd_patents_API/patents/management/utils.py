import csv
import logging
import psycopg2

def clean_value(value, max_length=None):
    """Clean the value by stripping whitespace and removing non-printable characters. Optionally trim to max_length."""
    if value is not None:
        value = ''.join(char for char in value if char.isprintable()).strip()
        if max_length:
            value = value[:max_length]
    return value

def preprocess_csv(input_file, output_file, fieldnames):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.DictReader(infile, delimiter='|')
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='|')
        writer.writeheader()
        
        for row in reader:
            for key in row:
                if 'date' in key.lower() and row[key] in ['NULL', '-1', '']:
                    row[key] = ''
                if key in [
                    'Language of Filing Code - Langue du type de dépôt',
                    'Abstract Language Code - Code de la langue du résumé',
                    'Classification Level - Niveau de classification',
                    'Classification Status Code - Code du statut de classification',
                    'Classification Status - Statut de classification',
                    'IPC Section Code - Code de la section de la CIB'
                ]:
                    row[key] = clean_value(row[key], max_length=2 if 'Code' in key else 1)
            writer.writerow(row)
            logging.info(f"Processed row for preprocessing: {row['Patent Number - Numéro du brevet']}")

def import_rows(file_path, conn, table_name, update_or_create_record):
    with open(file_path, 'r', encoding='utf-8') as temp_file:
        try:
            with conn.cursor() as cur:
                logging.info(f"Starting bulk copy for {file_path}")
                cur.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV HEADER DELIMITER '|' NULL 'NULL'", temp_file)
                logging.info(f"Successfully copied data from {file_path}")
        except psycopg2.errors.UniqueViolation as e:
            logging.warning(f"Duplicate key error encountered: {e}. Attempting to update existing records.")
            conn.rollback()
            with conn.cursor() as cur:
                temp_file.seek(0)
                reader = csv.DictReader(temp_file, delimiter='|')
                for row in reader:
                    update_or_create_record(row, cur, conn)
            conn.commit()
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
                        logging.error(f"Error updating/creating record: {inner_e}")
            conn.commit()

def preprocess_and_import_csv(input_file, conn, table_name, update_or_create_record, fieldnames, chunk_size=1000):
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, delimiter='|')
        
        chunk = []
        for idx, row in enumerate(reader, start=1):
            for key in row:
                if 'date' in key.lower() and row[key] in ['NULL', '-1', '']:
                    row[key] = ''
                if key in [
                    'Language of Filing Code - Langue du type de dépôt',
                    'Abstract Language Code - Code de la langue du résumé',
                    'Classification Level - Niveau de classification',
                    'Classification Status Code - Code du statut de classification',
                    'Classification Status - Statut de classification',
                    'IPC Section Code - Code de la section de la CIB'
                ]:
                    row[key] = clean_value(row[key], max_length=2 if 'Code' in key else 1)
            chunk.append(row)
            
            if idx % chunk_size == 0:
                process_chunk(chunk, conn, table_name, update_or_create_record, fieldnames)
                chunk = []
                logging.info(f"Processing and importing rows {idx-chunk_size+1} to {idx}")
        
        if chunk:
            process_chunk(chunk, conn, table_name, update_or_create_record, fieldnames)
            logging.info(f"Processing and importing remaining rows")

def process_chunk(chunk, conn, table_name, update_or_create_record, fieldnames):
    with open('temp_chunk.csv', 'w', encoding='utf-8', newline='') as temp_file:
        writer = csv.DictWriter(temp_file, fieldnames=fieldnames, delimiter='|')
        writer.writeheader()
        writer.writerows(chunk)
    import_rows('temp_chunk.csv', conn, table_name, update_or_create_record)
