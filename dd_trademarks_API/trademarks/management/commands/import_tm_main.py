import os
import pandas as pd
import sqlalchemy
from sqlalchemy.types import Integer, Boolean, Date, Text, BigInteger
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
    'tm_main': {
        'bool_cols': [
            'expungement_indicator', 
            'distinctiveness_indicator',
            'evidence_of_use_indicator',
            'foreign_application_indicator',
            'foreign_registration_indicator',
            'used_in_canada_indicator',
            'proposed_use_in_canada_indicator'
        ],
        'date_cols': [
            'publication_date', 'expiry_date', 'current_status_date',
            'divisional_application_date', 'allowed_date', 'renewal_date',
            'filing_date', 'registration_date', 'receiving_office_date',
            'termination_date', 'opposition_start_date', 'opposition_end_date',
            'authorization_of_use_date', 'application_abandoned_date'
        ],
        'int_cols': [
            'legislation_code',
            'wipo_status_code',
            'mark_type_code',
            'total_nice_classifications_number',
            'authorization_code',
            'cipo_status_code',
            'trademark_class_code',
            'geographical_indication_kind_category_code',
            'geographical_indication_translation_sequence_number'
        ]
    },
}

def setup_database(engine):
    """
    Drops and recreates the tm_main table to ensure a clean slate.
    """
    logging.info("Setting up the database schema for tm_main...")
    
    # SQL statement to create the tm_main table
    # This is taken directly from your pgAdmin output
    create_tm_main_sql = """
    CREATE TABLE IF NOT EXISTS public.tm_main
    (
        application_number text COLLATE pg_catalog."default" NOT NULL,
        filing_date date,
        publication_date date,
        registration_date date,
        registration_office_country_code text COLLATE pg_catalog."default",
        receiving_office_country_code text COLLATE pg_catalog."default",
        receiving_office_date date,
        assigning_office_country_code text COLLATE pg_catalog."default",
        registration_number character varying(255) COLLATE pg_catalog."default",
        legislation_code integer,
        filing_place text COLLATE pg_catalog."default",
        application_reference_number text COLLATE pg_catalog."default",
        application_language_code text COLLATE pg_catalog."default",
        expiry_date date,
        termination_date date,
        wipo_status_code integer,
        current_status_date date,
        association_category_id text COLLATE pg_catalog."default",
        associated_application_number bigint,
        mark_category text COLLATE pg_catalog."default",
        divisional_application_country_code text COLLATE pg_catalog."default",
        divisional_application_number bigint,
        divisional_application_date date,
        international_registration_number character varying(255) COLLATE pg_catalog."default",
        mark_type_code integer,
        mark_verbal_element_text text COLLATE pg_catalog."default",
        mark_significant_verbal_element_text text COLLATE pg_catalog."default",
        mark_translation_text text COLLATE pg_catalog."default",
        expungement_indicator boolean,
        distinctiveness_indicator boolean,
        distinctiveness_description text COLLATE pg_catalog."default",
        evidence_of_use_indicator boolean,
        evidence_of_use_description text COLLATE pg_catalog."default",
        restriction_of_use_description text COLLATE pg_catalog."default",
        cipo_standard_message_description text COLLATE pg_catalog."default",
        opposition_start_date date,
        opposition_end_date date,
        total_nice_classifications_number integer,
        foreign_application_indicator boolean,
        foreign_registration_indicator boolean,
        used_in_canada_indicator boolean,
        proposed_use_in_canada_indicator boolean,
        classification_term_office_country_code text COLLATE pg_catalog."default",
        classification_term_source_category text COLLATE pg_catalog."default",
        classification_term_english_description text COLLATE pg_catalog."default",
        publication_id text COLLATE pg_catalog."default",
        publication_status text COLLATE pg_catalog."default",
        authorization_of_use_date date,
        authorization_code integer,
        authorization_description text COLLATE pg_catalog."default",
        register_code text COLLATE pg_catalog."default",
        application_abandoned_date date,
        allowed_date date,
        renewal_date date,
        trademark_class_code integer,
        geographical_indication_kind_category_code integer,
        geographical_indication_translation_sequence_number integer,
        geographical_indication_translation_text text COLLATE pg_catalog."default",
        doubtful_case_application_number character varying(255) COLLATE pg_catalog."default",
        doubtful_case_registration_number character varying(255) COLLATE pg_catalog."default",
        cipo_status_code integer,
        CONSTRAINT tm_main_pkey PRIMARY KEY (application_number)
    )
    """
    
    try:
        with engine.connect() as connection:
            # Use a transaction to ensure both operations succeed or fail together
            with connection.begin() as transaction:
                logging.info("Dropping existing tm_main table (and dependent tables)...")
                # Drop table with CASCADE to also drop dependent tables
                connection.execute(sqlalchemy.text("DROP TABLE IF EXISTS public.tm_main CASCADE;"))
                
                logging.info("Creating new tm_main table...")
                connection.execute(sqlalchemy.text(create_tm_main_sql))
        logging.info("Database setup for tm_main complete.")
    except Exception as e:
        logging.error(f"An error occurred during database setup: {e}")
        raise

def convert_data_types(df, table_name):
    """
    Converts DataFrame columns to specific types based on the table's configuration.
    """
    if table_name not in TYPE_CONVERSIONS:
        return df

    config = TYPE_CONVERSIONS.get(table_name, {})
    df_copy = df.copy()

    if 'bool_cols' in config:
        for col in config.get('bool_cols', []):
            if col in df_copy.columns:
                map_dict = {'1': True, 't': True, 'true': True, 'y': True, 'yes': True,
                            '0': False, 'f': False, 'false': False, 'n': False, 'no': False}
                df_copy[col] = df_copy[col].astype(str).str.strip().str.lower().map(map_dict).astype('boolean')

    if 'date_cols' in config:
        for col in config.get('date_cols', []):
            if col in df_copy.columns:
                df_copy[col] = pd.to_datetime(df_copy[col], errors='coerce')

    if 'int_cols' in config:
        for col in config.get('int_cols', []):
            if col in df_copy.columns:
                df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce').astype('Int64')
            
    return df_copy


def load_data(table_name, zip_file_path, csv_file_name, column_mapping, engine, dtype_mapping=None):
    """
    A generic function to extract a CSV and load it into a PostgreSQL table.
    """
    logging.info("-" * 50)
    logging.info(f"Starting data load for table: '{table_name}'")
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
                    chunk_df.dropna(subset=['application_number'], inplace=True)

                    if chunk_df.empty:
                        logging.info(f"     Chunk {i + 1} is empty after dropping nulls. Skipping.")
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

    # Step 1: Set up the database schema
    setup_database(db_engine)

    # Step 2: Load the data into the newly created table
    tm_main_column_mapping = {
        'Application Number - Numéro de la demande ': 'application_number',
        'Filing Date - Date de dépôt': 'filing_date',
        'Publication Date - Date de publication': 'publication_date',
        'Registration Date - Date d’enregistrement': 'registration_date',
        'Registration Office Country Code - Code du pays de l’office de l’enregistrement': 'registration_office_country_code',
        'Receiving Office Country Code - Code du pays de l’office récepteur': 'receiving_office_country_code',
        'Receiving Office Date - Date de réception par l’office': 'receiving_office_date',
        "Assigning Office Country Code - Code du pays de l'office de cession": 'assigning_office_country_code',
        'Registration Number - Numéro d’enregistrement': 'registration_number',
        'Legislation Description Code - Code de description de la législation (Code de Loi applicable)': 'legislation_code',
        'Filing Place - Pays de Dépôt': 'filing_place',
        'Application Reference Number - Numéro de référence de la demande': 'application_reference_number',
        'Application Language Code - Code de langue de la demande': 'application_language_code',
        "Expiry Date - Date d'expiration": 'expiry_date',
        'Termination Date - Date d’inactivation': 'termination_date',
        'WIPO Status Code - Code du statut de l’OMPI': 'wipo_status_code',
        'Current Status Date - Date de statut actuel ': 'current_status_date',
        'Association Category ID - Indicateur de cession partielle': 'association_category_id',
        'Associated Application Number - Numéro de la demande associée': 'associated_application_number',
        'Mark Category - Catégorie de la marque ': 'mark_category',
        'Divisional Application Country Code - Code du pays de la demande divisionnaire': 'divisional_application_country_code',
        'Divisional Application Number - numéro de la demande divisionnaire (Numéro ST.13 de la demande originale)': 'divisional_application_number',
        'Divisional Application Date - Date de la demande divisionnaire': 'divisional_application_date',
        'Internationall Registration Number - Numéro d’enregistrement international': 'international_registration_number',
        'MarkType Code - Code du type de marque ': 'mark_type_code',
        'Mark Verbal Element Description - Description de l’élément Verbal de la marque (Texte de l’élément Verbal de la marque)': 'mark_verbal_element_text',
        'Mark Significant Description - Description  détaillée de la marque (Texte de l’élément verbal signifiant de la marque)': 'mark_significant_verbal_element_text',
        'Mark Translation Description - Description de la traduction de la marque (Traduction de la marque)': 'mark_translation_text',
        'Expungement Indicator - Indicateur de radiation': 'expungement_indicator',
        'Distinctiveness Indicator - Indicateur de caractère distinctif acquis': 'distinctiveness_indicator',
        'Distinctiveness Description - Descriotion du caractère distinctif acquis': 'distinctiveness_description',
        'Evidence Of Use Indicator - Indicateur de preuve d’utilisation': 'evidence_of_use_indicator',
        'Evidence Of Use Description - Description de preuve d’utilisation': 'evidence_of_use_description',
        'Restriction Of Use Description - Description de la restriction d’utilisation': 'restriction_of_use_description',
        'CIPO Standard Message Description - Description de la mise en garde sur les données de marque de commerce': 'cipo_standard_message_description',
        'Opposition Start Date - Date de début d’opposition ': 'opposition_start_date',
        'Opposition End Date - Date de fin d’opposition ': 'opposition_end_date',
        'Total Nice Classifications Number - Nombre total de classification de Nice ': 'total_nice_classifications_number',
        'Foreign Application Indicator - Indicateur de demande étrangère': 'foreign_application_indicator',
        "Foreign Registration Indicator - Indicateur d'enregistrement étranger": 'foreign_registration_indicator',
        'Used In Canada Indicator - Indicateur d’utilisation au Canada': 'used_in_canada_indicator',
        "Proposed Use In Canada Indicator - Indicateur d'utilisation projetée au Canada": 'proposed_use_in_canada_indicator',
        "Classification Term Office Country Code - Code du pays de l'office du terme de classification": 'classification_term_office_country_code',
        'Classification Term Source Name - Catégorie de la source du terme de classification': 'classification_term_source_category',
        'Classification Term English Description - Description en anglais du terme de classification': 'classification_term_english_description',
        'Publication ID - Numéro et volume de la publication ': 'publication_id',
        'Publication Status - Statut de publication': 'publication_status',
        "Authorization Of Use Date - Date d’autorisation d'utilisation": 'authorization_of_use_date',
        "Authorization Code - Code d'autorisation": 'authorization_code',
        "Authorization Description - Description d'autorisation": 'authorization_description',
        'Register Code - Catégorie du registre': 'register_code',
        'Application Abandoned Date - Date d’abandon de la demande': 'application_abandoned_date',
        'CIPO Status Code - Code de statut de la marque': 'cipo_status_code',
        'Allowed Date - Date admise': 'allowed_date',
        'Renewal Date - Date de renouvellement': 'renewal_date',
        'Trademark Class Code - Code de la classe de marque ': 'trademark_class_code',
        'Geographical Indication Kind Category Code - Code du type d’indication géographique': 'geographical_indication_kind_category_code',
        'Geographical Indication Translation Sequence Number - Numéro d’ordre de traduction de l’indication géographique': 'geographical_indication_translation_sequence_number',
        'Geographical IndicationTranslationText - Texte de la traduction de l’indication géographique': 'geographical_indication_translation_text',
        'Doubtful Case Application Number - Numéro de demande du cas douteux': 'doubtful_case_application_number',
        'Doubtful Case Registration Number - Numéro d’enregistrement du cas douteux': 'doubtful_case_registration_number'
    }

    tm_main_dtype_mapping = {
        col: Integer for col in TYPE_CONVERSIONS['tm_main']['int_cols']
    }
    tm_main_dtype_mapping.update({
        col: Boolean for col in TYPE_CONVERSIONS['tm_main']['bool_cols']
    })
    tm_main_dtype_mapping.update({
        col: Date for col in TYPE_CONVERSIONS['tm_main']['date_cols']
    })
    
    load_data(
        table_name='tm_main',
        zip_file_path="TM_application_main_2025-01-28.zip",
        csv_file_name="TM_application_main_2025-01-28.csv",
        column_mapping=tm_main_column_mapping,
        engine=db_engine,
        dtype_mapping=tm_main_dtype_mapping
    )

    print("\nAll data loading tasks are finished.")