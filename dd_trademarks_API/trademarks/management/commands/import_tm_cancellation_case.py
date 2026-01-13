import os
import pandas as pd
import sqlalchemy
from sqlalchemy.types import Integer, Boolean, Date, Text
import zipfile
import logging
from dotenv import load_dotenv
import numpy as np

# --- Configuration ---
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- 1. GENERAL CONFIGURATION ---
CHUNK_SIZE = 100000 
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Mostafa75")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "TM_data")

# --- Type Conversion Configuration ---
TYPE_CONVERSIONS = {
    'tm_cancellation_case': {
        'date_cols': ['section_44_45_filing_date', 'section_44_45_status_date'],
        'int_cols': [
            'section_44_45_case_number',
            'wipo_section_44_45_status_category_code', 
            'section_44_45_status_code', 
            'agent_number_of_plaintiff'
        ]
    }
}

def setup_database(engine, table_name, create_sql):
    """
    Drops and recreates a table to ensure a clean slate.
    """
    logging.info(f"Setting up the database schema for {table_name}...")
    try:
        with engine.connect() as connection:
            with connection.begin() as transaction:
                logging.info(f"Dropping existing {table_name} table if it exists...")
                connection.execute(sqlalchemy.text(f"DROP TABLE IF EXISTS public.{table_name} CASCADE;"))
                
                logging.info(f"Creating new {table_name} table...")
                connection.execute(sqlalchemy.text(create_sql))
        logging.info(f"Database setup for {table_name} complete.")
    except Exception as e:
        logging.error(f"An error occurred during database setup for {table_name}: {e}")
        raise

def convert_data_types(df, table_name):
    """
    Converts DataFrame columns to specific types based on the table's configuration.
    """
    if table_name not in TYPE_CONVERSIONS:
        return df

    config = TYPE_CONVERSIONS.get(table_name, {})
    df_copy = df.copy()

    if 'date_cols' in config:
        for col in config.get('date_cols', []):
            if col in df_copy.columns:
                df_copy[col] = pd.to_datetime(df_copy[col], errors='coerce')

    if 'int_cols' in config:
        for col in config.get('int_cols', []):
            if col in df_copy.columns:
                df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce').astype('Int64')
            
    return df_copy


def load_data(table_name, zip_file_path, csv_file_name, column_mapping, engine, dtype_mapping=None, has_header=True, drop_nulls=None):
    """
    A generic function to extract a CSV and load it into a PostgreSQL table.
    """
    logging.info("-" * 50)
    logging.info(f"Starting data load for table: '{table_name}'")
    
    logging.info("Fetching existing application numbers from tm_main...")
    try:
        with engine.connect() as connection:
            main_ids_df = pd.read_sql("SELECT application_number FROM tm_main", connection)
            valid_app_numbers = set(main_ids_df['application_number'])
            logging.info(f"Found {len(valid_app_numbers)} valid application numbers to link against.")
    except Exception as e:
        logging.error(f"Could not fetch application numbers from tm_main. This must be loaded first. Aborting. Error: {e}")
        return

    try:
        with zipfile.ZipFile(zip_file_path, 'r') as z:
            with z.open(csv_file_name) as f:
                header_option = 0 if has_header else None
                df_iterator = pd.read_csv(
                    f, delimiter='|', header=header_option, chunksize=CHUNK_SIZE, 
                    low_memory=False, dtype=str, on_bad_lines='skip', quoting=3
                )

                logging.info("Processing and loading data in chunks...")
                for i, chunk_df in enumerate(df_iterator):
                    logging.info(f"  -> Processing chunk {i + 1}...")

                    chunk_df.rename(columns=column_mapping, inplace=True)
                    processed_chunk = convert_data_types(chunk_df.copy(), table_name)
                    
                    required_cols = ['application_number'] + (drop_nulls or [])
                    processed_chunk.dropna(subset=required_cols, inplace=True)

                    original_rows = len(processed_chunk)
                    processed_chunk = processed_chunk[processed_chunk['application_number'].isin(valid_app_numbers)]
                    if original_rows > len(processed_chunk):
                        logging.info(f"     Removed {original_rows - len(processed_chunk)} rows with no matching application_number in tm_main.")

                    if processed_chunk.empty:
                        logging.info(f"     Chunk {i + 1} is empty after filtering. Skipping.")
                        continue
                    
                    processed_chunk.drop_duplicates(inplace=True)

                    db_columns = [col for col in processed_chunk.columns if col in column_mapping.values()]
                    final_chunk = processed_chunk[db_columns]

                    final_chunk.to_sql(
                        name=table_name,
                        con=engine,
                        if_exists='append',
                        index=False,
                        method='multi',
                        dtype=dtype_mapping
                    )
        logging.info(f"Data loading for '{table_name}' complete! 🎉")
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading '{table_name}': {e}")
        raise


if __name__ == "__main__":
    db_engine = sqlalchemy.create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # =================================================================
    #           Step 1: Define and Create the Table Schema
    # =================================================================
    create_tm_cancellation_case_sql = """
    CREATE TABLE IF NOT EXISTS public.tm_cancellation_case
    (
        application_number text COLLATE pg_catalog."default" NOT NULL,
        section_44_45_case_number integer NOT NULL,
        legal_proceeding_type_description_in_english text COLLATE pg_catalog."default",
        legal_proceeding_type_description_in_french text COLLATE pg_catalog."default",
        section_44_45_filing_date date,
        wipo_section_44_45_status_category_code smallint,
        section_44_45_status_code smallint,
        section_44_45_status_date date,
        entity_name_of_the_legal_proceeding_defendant text COLLATE pg_catalog."default",
        defendant_language_code text COLLATE pg_catalog."default",
        defendant_address_line_1 text COLLATE pg_catalog."default",
        defendant_address_line_2 text COLLATE pg_catalog."default",
        defendant_address_line_3 text COLLATE pg_catalog."default",
        defendant_country_code text COLLATE pg_catalog."default",
        contact_name_of_defendant text COLLATE pg_catalog."default",
        contact_language_code_of_defendant text COLLATE pg_catalog."default",
        contact_address_line_1_of_defendant text COLLATE pg_catalog."default",
        contact_address_line_2_of_defendant text COLLATE pg_catalog."default",
        contact_address_line_3_of_defendant text COLLATE pg_catalog."default",
        contact_province_name_of_defendant text COLLATE pg_catalog."default",
        contact_country_code_of_defendant text COLLATE pg_catalog."default",
        contact_postal_code_of_defendant text COLLATE pg_catalog."default",
        agent_name_of_defendant text COLLATE pg_catalog."default",
        agent_language_code_of_defendant text COLLATE pg_catalog."default",
        agent_address_line_1_of_defendant text COLLATE pg_catalog."default",
        agent_address_line_2_of_defendant text COLLATE pg_catalog."default",
        agent_address_line_3_of_defendant text COLLATE pg_catalog."default",
        agent_province_name_of_defendant text COLLATE pg_catalog."default",
        agent_country_code_of_defendant text COLLATE pg_catalog."default",
        agent_postal_code_of_defendant text COLLATE pg_catalog."default",
        plaintiff_name text COLLATE pg_catalog."default",
        plaintiff_legal_name text COLLATE pg_catalog."default",
        plaintiff_language_code text COLLATE pg_catalog."default",
        plaintiff_address_line_1 text COLLATE pg_catalog."default",
        plaintiff_address_line_2 text COLLATE pg_catalog."default",
        plaintiff_address_line_3 text COLLATE pg_catalog."default",
        plaintiff_country_code text COLLATE pg_catalog."default",
        contact_name_of_plaintiff text COLLATE pg_catalog."default",
        contact_language_code_of_plaintiff text COLLATE pg_catalog."default",
        contact_address_line_1_of_plaintiff text COLLATE pg_catalog."default",
        contact_address_line_2_of_plaintiff text COLLATE pg_catalog."default",
        contact_address_line_3_of_plaintiff text COLLATE pg_catalog."default",
        contact_province_name_of_plaintiff text COLLATE pg_catalog."default",
        contact_country_code_of_plaintiff text COLLATE pg_catalog."default",
        contact_postal_code_of_plaintiff text COLLATE pg_catalog."default",
        agent_number_of_plaintiff integer,
        agent_name_of_plaintiff text COLLATE pg_catalog."default",
        agent_language_code_of_plaintiff text COLLATE pg_catalog."default",
        agent_address_line_1_of_plaintiff text COLLATE pg_catalog."default",
        agent_address_line_2_of_plaintiff text COLLATE pg_catalog."default",
        agent_address_line_3_of_plaintiff text COLLATE pg_catalog."default",
        agent_province_name_of_plaintiff text COLLATE pg_catalog."default",
        agent_country_code_of_plaintiff text COLLATE pg_catalog."default",
        agent_postal_code_of_plaintiff text COLLATE pg_catalog."default",
        CONSTRAINT tm_cancellation_case_pkey PRIMARY KEY (application_number, section_44_45_case_number),
        CONSTRAINT fk_tm_main FOREIGN KEY (application_number)
            REFERENCES public.tm_main (application_number) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE CASCADE
    )
    """
    setup_database(db_engine, 'tm_cancellation_case', create_tm_cancellation_case_sql)

    # =================================================================
    #              Step 2: Load Data into the New Table
    # =================================================================
    tm_cancellation_case_mapping = {
        0: 'application_number',
        1: 'section_44_45_case_number',
        2: 'legal_proceeding_type_description_in_english',
        3: 'legal_proceeding_type_description_in_french',
        4: 'section_44_45_filing_date',
        5: 'wipo_section_44_45_status_category_code',
        6: 'section_44_45_status_code',
        7: 'section_44_45_status_date',
        8: 'entity_name_of_the_legal_proceeding_defendant',
        9: 'defendant_language_code',
        10: 'defendant_address_line_1',
        11: 'defendant_address_line_2',
        12: 'defendant_address_line_3',
        13: 'defendant_country_code',
        14: 'contact_name_of_defendant',
        15: 'contact_language_code_of_defendant',
        16: 'contact_address_line_1_of_defendant',
        17: 'contact_address_line_2_of_defendant',
        18: 'contact_address_line_3_of_defendant',
        19: 'contact_province_name_of_defendant',
        20: 'contact_country_code_of_defendant',
        21: 'contact_postal_code_of_defendant',
        22: 'agent_name_of_defendant',
        23: 'agent_language_code_of_defendant',
        24: 'agent_address_line_1_of_defendant',
        25: 'agent_address_line_2_of_defendant',
        26: 'agent_address_line_3_of_defendant',
        27: 'agent_province_name_of_defendant',
        28: 'agent_country_code_of_defendant',
        29: 'agent_postal_code_of_defendant',
        30: 'plaintiff_name',
        31: 'plaintiff_legal_name',
        32: 'plaintiff_language_code',
        33: 'plaintiff_address_line_1',
        34: 'plaintiff_address_line_2',
        35: 'plaintiff_address_line_3',
        36: 'plaintiff_country_code',
        37: 'contact_name_of_plaintiff',
        38: 'contact_language_code_of_plaintiff',
        39: 'contact_address_line_1_of_plaintiff',
        40: 'contact_address_line_2_of_plaintiff',
        41: 'contact_address_line_3_of_plaintiff',
        42: 'contact_province_name_of_plaintiff',
        43: 'contact_country_code_of_plaintiff',
        44: 'contact_postal_code_of_plaintiff',
        45: 'agent_number_of_plaintiff',
        46: 'agent_name_of_plaintiff',
        47: 'agent_language_code_of_plaintiff',
        48: 'agent_address_line_1_of_plaintiff',
        49: 'agent_address_line_2_of_plaintiff',
        50: 'agent_address_line_3_of_plaintiff',
        51: 'agent_province_name_of_plaintiff',
        52: 'agent_country_code_of_plaintiff',
        53: 'agent_postal_code_of_plaintiff'
    }

    tm_cancellation_case_dtype_mapping = {
        'section_44_45_filing_date': Date,
        'section_44_45_status_date': Date,
        'wipo_section_44_45_status_category_code': Integer,
        'section_44_45_status_code': Integer,
        'agent_number_of_plaintiff': Integer
    }
    
    load_data(
        table_name='tm_cancellation_case',
        zip_file_path="TM_cancellation_case_2025-01-28.zip",
        csv_file_name="TM_cancellation_case_2025-01-28.csv",
        column_mapping=tm_cancellation_case_mapping,
        engine=db_engine,
        dtype_mapping=tm_cancellation_case_dtype_mapping,
        has_header=False, # This file has no header
        drop_nulls=['section_44_45_case_number']
    )

    print("\nAll data loading tasks are finished.")