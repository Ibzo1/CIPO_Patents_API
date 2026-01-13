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
    'tm_cancellation_case_action': {
        'date_cols': ['proceeding_effective_date', 'section_44_45_filing_date', 'section_44_45_status_date'],
        'int_cols': [
            'section_44_45_case_number',
            'wipo_section_44_45_status_category_code',
            'section_44_45_status_code',
            'section_44_45_stage_code',
            'section_44_45_actions_code'
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


def load_data(table_name, zip_file_path, csv_file_name, column_mapping, engine, dtype_mapping=None, parent_table_info=None):
    """
    A generic function to extract a CSV and load it into a PostgreSQL table.
    """
    logging.info("-" * 50)
    logging.info(f"Starting data load for table: '{table_name}'")
    
    valid_parent_keys_df = None
    if parent_table_info:
        parent_table = parent_table_info['name']
        parent_key_cols = parent_table_info['key_cols']
        logging.info(f"Fetching existing keys from parent table '{parent_table}'...")
        try:
            with engine.connect() as connection:
                query = f"SELECT {', '.join(parent_key_cols)} FROM {parent_table}"
                valid_parent_keys_df = pd.read_sql(query, connection)
                # Convert integer columns in the parent key df for accurate matching
                for col in parent_key_cols:
                    if pd.api.types.is_numeric_dtype(valid_parent_keys_df[col]):
                         valid_parent_keys_df[col] = valid_parent_keys_df[col].astype('Int64')
                logging.info(f"Found {len(valid_parent_keys_df)} valid parent key combinations to link against.")
        except Exception as e:
            logging.error(f"Could not fetch keys from {parent_table}. Aborting. Error: {e}")
            return

    try:
        with zipfile.ZipFile(zip_file_path, 'r') as z:
            with z.open(csv_file_name) as f:
                df_iterator = pd.read_csv(
                    f, delimiter='|', chunksize=CHUNK_SIZE, low_memory=False, 
                    dtype=str, on_bad_lines='skip', quoting=3
                )

                logging.info("Processing and loading data in chunks...")
                for i, chunk_df in enumerate(df_iterator):
                    logging.info(f"  -> Processing chunk {i + 1}...")

                    chunk_df.rename(columns=column_mapping, inplace=True)
                    processed_chunk = convert_data_types(chunk_df.copy(), table_name)
                    processed_chunk.dropna(subset=['application_number', 'section_44_45_case_number'], inplace=True)

                    if parent_table_info:
                        original_rows = len(processed_chunk)
                        # Use pandas merge to efficiently filter for valid parent keys
                        processed_chunk = processed_chunk.merge(valid_parent_keys_df, on=parent_key_cols, how='inner')
                        if original_rows > len(processed_chunk):
                            logging.info(f"     Removed {original_rows - len(processed_chunk)} rows with no matching key in parent table '{parent_table}'.")

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
        logging.info(f"Data loading for '{table_name}' complete! �")
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
    create_tm_cancellation_case_action_sql = """
    CREATE TABLE IF NOT EXISTS public.tm_cancellation_case_action
    (
        cancellation_case_action_id SERIAL PRIMARY KEY,
        application_number text COLLATE pg_catalog."default" NOT NULL,
        section_44_45_case_number integer NOT NULL,
        additional_comment text COLLATE pg_catalog."default",
        proceeding_effective_date date,
        legal_proceeding_type_description_in_english text COLLATE pg_catalog."default",
        legal_proceeding_type_description_in_french text COLLATE pg_catalog."default",
        section_44_45_filing_date date,
        wipo_section_44_45_status_category_code smallint,
        section_44_45_status_code smallint,
        section_44_45_status_date date,
        section_44_45_stage_code integer,
        section_44_45_case_status text COLLATE pg_catalog."default",
        section_44_45_actions_code integer,
        CONSTRAINT fk_tm_cancellation_case FOREIGN KEY (application_number, section_44_45_case_number)
            REFERENCES public.tm_cancellation_case (application_number, section_44_45_case_number) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE CASCADE
    )
    """
    setup_database(db_engine, 'tm_cancellation_case_action', create_tm_cancellation_case_action_sql)

    # =================================================================
    #              Step 2: Load Data into the New Table
    # =================================================================
    tm_cancellation_case_action_mapping = {
        'Application Number - Numéro de la demande ': 'application_number',
        'Additional Comment - Information supplémentaire': 'additional_comment',
        'Proceeding Effective Date - Date d’entrée en vigueur de l’action ': 'proceeding_effective_date',
        'Section 44/45 Case Number - Numéro du cas de l’article 44/45': 'section_44_45_case_number',
        'Legal Proceeding Type Description in English - Description du type de procédure juridique en anglais': 'legal_proceeding_type_description_in_english',
        'Legal Proceeding Type Description in French - Description du type de procédure juridique en français': 'legal_proceeding_type_description_in_french',
        'Section 44/45 Filing Date - Date de soumission de l’article 44/45': 'section_44_45_filing_date',
        'WIPO Section 44/45 Status Category Code - Catégorie du statut de l’article 44/45 selon l’OMPI': 'wipo_section_44_45_status_category_code',
        'Section 44/45 Status Code - Code du statut de l’article 44/45': 'section_44_45_status_code',
        'Section 44/45 Status Date - Date du statut de l’article 44/45': 'section_44_45_status_date',
        'Section 44/45 Stage Code - Code de l’étape de l’article 44/45': 'section_44_45_stage_code',
        'Section 44/45 case status - Statut du cas sous l’article 44/45 ': 'section_44_45_case_status',
        "Section 44/45 actions code - Code d’action de l'article  44/45": 'section_44_45_actions_code'
    }

    tm_cancellation_case_action_dtype_mapping = {
        'proceeding_effective_date': Date,
        'section_44_45_filing_date': Date,
        'section_44_45_status_date': Date,
        'section_44_45_case_number': Integer,
        'wipo_section_44_45_status_category_code': Integer,
        'section_44_45_status_code': Integer,
        'section_44_45_stage_code': Integer,
        'section_44_45_actions_code': Integer
    }
    
    parent_info = {
        'name': 'tm_cancellation_case',
        'key_cols': ['application_number', 'section_44_45_case_number']
    }

    load_data(
        table_name='tm_cancellation_case_action',
        zip_file_path="TM_cancellation_case_action_2025-01-28.zip",
        csv_file_name="TM_cancellation_case_action_2025-01-28.csv",
        column_mapping=tm_cancellation_case_action_mapping,
        engine=db_engine,
        dtype_mapping=tm_cancellation_case_action_dtype_mapping,
        parent_table_info=parent_info
    )

    print("\nAll data loading tasks are finished.")