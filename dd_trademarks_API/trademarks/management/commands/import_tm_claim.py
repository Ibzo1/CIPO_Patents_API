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
    'tm_claim': {
        'date_cols': ['structure_claim_date'],
        'int_cols': [
            'claim_type',
            'claim_number',
            'claim_code',
            'claim_year_number',
            'claim_month_number',
            'claim_day_number'
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


def load_data(table_name, zip_file_path, csv_file_name, column_mapping, engine, dtype_mapping=None, drop_nulls=None):
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
                df_iterator = pd.read_csv(
                    f, delimiter='|', chunksize=CHUNK_SIZE, low_memory=False, 
                    dtype=str, on_bad_lines='skip', quoting=3
                )

                logging.info("Processing and loading data in chunks...")
                for i, chunk_df in enumerate(df_iterator):
                    logging.info(f"  -> Processing chunk {i + 1}...")

                    chunk_df.rename(columns=column_mapping, inplace=True)
                    processed_chunk = convert_data_types(chunk_df.copy(), table_name)

                    # Drop rows where any part of the composite primary key is null
                    required_cols = ['application_number'] + (drop_nulls or [])
                    processed_chunk.dropna(subset=required_cols, inplace=True)

                    original_rows = len(processed_chunk)
                    processed_chunk = processed_chunk[processed_chunk['application_number'].isin(valid_app_numbers)]
                    if original_rows > len(processed_chunk):
                        logging.info(f"     Removed {original_rows - len(processed_chunk)} rows with no matching application_number in tm_main.")

                    if processed_chunk.empty:
                        logging.info(f"     Chunk {i + 1} is empty after filtering. Skipping.")
                        continue
                    
                    # Remove any true duplicates before trying to insert
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
    create_tm_claim_sql = """
    CREATE TABLE IF NOT EXISTS public.tm_claim
    (
        application_number text COLLATE pg_catalog."default" NOT NULL,
        claim_type smallint NOT NULL,
        claim_number integer NOT NULL,
        claim_text text COLLATE pg_catalog."default",
        claim_code smallint,
        structure_claim_date date,
        claim_year_number smallint,
        claim_month_number smallint,
        claim_day_number smallint,
        claim_country_code text COLLATE pg_catalog."default",
        foreign_registration_number text COLLATE pg_catalog."default",
        goods_services_reference_identifier text COLLATE pg_catalog."default",
        CONSTRAINT tm_claim_pkey PRIMARY KEY (application_number, claim_type, claim_number),
        CONSTRAINT fk_tm_main FOREIGN KEY (application_number)
            REFERENCES public.tm_main (application_number) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE CASCADE
    )
    """
    setup_database(db_engine, 'tm_claim', create_tm_claim_sql)

    # =================================================================
    #              Step 2: Load Data into the New Table
    # =================================================================
    tm_claim_mapping = {
        'Application Number - Numéro de la demande ': 'application_number',
        'Claim Text - Texte de revendication': 'claim_text',
        'Claim Type - Type de revendication': 'claim_type',
        'Claim Number - Numéro de revendication': 'claim_number',
        'Claim Code - Code de revendication': 'claim_code',
        'Structure Claim Date - Date de revendication structurée': 'structure_claim_date',
        'Claim Year Number - Année de la revendication': 'claim_year_number',
        'Claim Month Number - Mois de la revendication': 'claim_month_number',
        'Claim Day Number - Jour de la revendication': 'claim_day_number',
        'Claim Country Code - Code du pays de la revendication': 'claim_country_code',
        'Foreign Registration Number - Numéro d’enregistrement de la revendication étrangère': 'foreign_registration_number',
        'Goods Services Reference Identifier - Nom de référence des produits et services': 'goods_services_reference_identifier'
    }

    tm_claim_dtype_mapping = {
        'claim_type': Integer,
        'claim_number': Integer,
        'claim_code': Integer,
        'claim_year_number': Integer,
        'claim_month_number': Integer,
        'claim_day_number': Integer,
        'structure_claim_date': Date
    }

    load_data(
        table_name='tm_claim',
        zip_file_path="TM_claim_2025-01-28.zip",
        csv_file_name="TM_claim_2025-01-28.csv",
        column_mapping=tm_claim_mapping,
        engine=db_engine,
        dtype_mapping=tm_claim_dtype_mapping,
        # Drop rows where any part of the composite primary key is null
        drop_nulls=['claim_type', 'claim_number']
    )

    print("\nAll data loading tasks are finished.")