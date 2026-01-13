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
    'tm_cipo_classifications': {
        'int_cols': ['nice_classification_code']
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
                # Use CASCADE to handle dependencies from other tables
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

    if 'int_cols' in config:
        for col in config.get('int_cols', []):
            if col in df_copy.columns:
                df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce').astype('Int64')
            
    return df_copy


def load_data(table_name, zip_file_path, csv_file_name, column_mapping, engine, dtype_mapping=None):
    """
    A generic function to extract a CSV from a ZIP and load it into a PostgreSQL table.
    """
    logging.info("-" * 50)
    logging.info(f"Starting data load for table: '{table_name}'")
    
    # This table depends on tm_main, so we fetch the valid application numbers first.
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
                df_iterator = pd.read_csv(
                    f, delimiter='|', chunksize=CHUNK_SIZE, low_memory=False, 
                    dtype=str, on_bad_lines='skip', quoting=3
                )
                
                logging.info("Processing and loading data in chunks...")
                for i, chunk_df in enumerate(df_iterator):
                    logging.info(f"  -> Processing chunk {i + 1}...")

                    chunk_df.rename(columns=column_mapping, inplace=True)
                    chunk_df.dropna(subset=['application_number', 'nice_classification_code'], inplace=True)
                    
                    # Filter out rows that don't have a corresponding entry in tm_main
                    original_rows = len(chunk_df)
                    chunk_df = chunk_df[chunk_df['application_number'].isin(valid_app_numbers)]
                    if original_rows > len(chunk_df):
                        logging.info(f"     Removed {original_rows - len(chunk_df)} rows with no matching application_number in tm_main.")

                    if chunk_df.empty:
                        logging.info(f"     Chunk {i + 1} is empty after filtering. Skipping.")
                        continue

                    db_columns = [col for col in chunk_df.columns if col in column_mapping.values()]
                    final_chunk = chunk_df[db_columns]
                    
                    processed_chunk = convert_data_types(final_chunk, table_name)
                    
                    processed_chunk.to_sql(
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
    create_tm_cipo_classifications_sql = """
    CREATE TABLE IF NOT EXISTS public.tm_cipo_classifications
    (
        application_number text COLLATE pg_catalog."default" NOT NULL,
        classification_kind_code text COLLATE pg_catalog."default",
        nice_classification_code smallint NOT NULL,
        CONSTRAINT tm_cipo_classifications_pkey PRIMARY KEY (application_number, nice_classification_code),
        CONSTRAINT fk_tm_main FOREIGN KEY (application_number)
            REFERENCES public.tm_main (application_number) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE CASCADE
    )
    """
    setup_database(db_engine, 'tm_cipo_classifications', create_tm_cipo_classifications_sql)
    
    # =================================================================
    #              Step 2: Load Data into the New Table
    # =================================================================
    tm_cipo_classification_mapping = {
        'Application Number - Numéro de la demande ': 'application_number',
        'Classification Kind Code - Code du type de classification': 'classification_kind_code',
        'Nice Classification Code - Code de Classification de Nice': 'nice_classification_code'
    }
    
    tm_cipo_dtype_mapping = {
        'nice_classification_code': Integer
    }
    
    load_data(
        table_name='tm_cipo_classifications',
        zip_file_path="TM_cipo_classification_2025-01-28.zip",
        csv_file_name="TM_cipo_classification_2025-01-28.csv",
        column_mapping=tm_cipo_classification_mapping,
        engine=db_engine,
        dtype_mapping=tm_cipo_dtype_mapping
    )

    print("\nAll data loading tasks are finished.")