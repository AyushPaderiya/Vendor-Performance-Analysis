import pandas as pd
import os
import logging
import time
from sqlalchemy import create_engine

pd.set_option("display.max_columns", None)

logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

engine = create_engine('sqlite:///inventory.db')


def ingest_db(df: pd.DataFrame, table_name: str, engine) -> None:
    """
    Ingests a DataFrame into a specified database table.

    Parameters:
    - df (pd.DataFrame): DataFrame to ingest
    - table_name (str): Name of the table to create/replace
    - engine: SQLAlchemy engine to connect to the database
    """
    try:
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
        logging.info(f"Successfully ingested table '{table_name}'")
    except Exception as e:
        logging.error(f"Error ingesting table '{table_name}': {e}")

def load_raw_data(data_path: str = 'data') -> None:
    """
    Loads all CSV files from the specified folder, ingests them into the database,
    and logs the time taken for the entire ingestion process.

    Parameters:
    - data_path (str): Folder path where CSV files are stored (default: 'data')
    """
    try:
        if not os.path.exists(data_path):
            logging.error(f"Data directory '{data_path}' does not exist.")
            print(f"Directory '{data_path}' not found.")
            return

        start = time.time()
        csv_files = [f for f in os.listdir(data_path) if f.endswith('.csv')]

        if not csv_files:
            logging.warning(f"No CSV files found in '{data_path}'.")
            print(f"No CSV files found in '{data_path}'.")
            return

        for file in csv_files:
            file_path = os.path.join(data_path, file)
            try:
                df = pd.read_csv(file_path)
                table_name = os.path.splitext(file)[0]
                logging.info(f"Ingesting {file} into table '{table_name}'")
                ingest_db(df, table_name, engine)
            except Exception as e:
                logging.error(f"Failed to read or ingest '{file}': {e}")
                print(f"Failed to process file '{file}': {e}")

        end = time.time()
        total_time = (end - start) / 60
        logging.info("------------- Ingestion Complete -------------")
        logging.info(f"Total Time Taken: {total_time:.2f} minutes")

    except Exception as e:
        logging.error(f"Unexpected error during data loading: {e}")


if __name__ == '__main__':
    load_raw_data()
