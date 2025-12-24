"""
Data ingestion module for Vendor Performance Analysis.
Loads CSV files from the data directory into a SQLite database.

Features:
- Configuration-driven paths and settings
- Data validation after ingestion
- Support for both full refresh and incremental loads
- Comprehensive logging
"""
import pandas as pd
import os
import logging
import time
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

# Add project root to path for config import
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'config'))

from config_loader import get_config, get_database_url, get_project_root


def setup_logging(config: Any) -> None:
    """Configure logging based on configuration settings."""
    log_config = config.logging_config
    log_file = get_project_root() / log_config.get('file', 'logs/pipeline.log')
    
    # Ensure log directory exists
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        filename=str(log_file),
        level=getattr(logging, log_config.get('level', 'INFO')),
        format=log_config.get('format', '%(asctime)s - %(levelname)s - %(message)s'),
        filemode='a' if log_config.get('append', True) else 'w'
    )
    
    # Also log to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logging.getLogger().addHandler(console_handler)


def create_db_engine(config: Any) -> Engine:
    """Create SQLAlchemy engine from configuration."""
    db_url = get_database_url()
    timeout = config.database.get('timeout', 30)
    echo = config.database.get('echo', False)
    
    engine = create_engine(
        db_url,
        connect_args={'timeout': timeout},
        echo=echo
    )
    return engine


def validate_dataframe(df: pd.DataFrame, table_name: str, config: Any) -> bool:
    """
    Validate a DataFrame before/after ingestion.
    
    Parameters:
    - df: DataFrame to validate
    - table_name: Name of the table (for config lookup)
    - config: Configuration object
    
    Returns:
    - True if validation passes, False otherwise
    """
    quality_config = config.data_quality
    etl_config = config.etl
    
    # Check minimum row count
    min_counts = etl_config.get('min_row_counts', {})
    if table_name in min_counts:
        expected_min = min_counts[table_name]
        actual = len(df)
        if actual < expected_min:
            logging.warning(
                f"Table '{table_name}' has {actual} rows, expected >= {expected_min}"
            )
            # Don't fail, just warn
    
    # Check for nulls in required columns
    required_cols = quality_config.get('required_columns', [])
    for col in required_cols:
        if col in df.columns:
            null_count = df[col].isnull().sum()
            if null_count > 0:
                logging.warning(
                    f"Column '{col}' in table '{table_name}' has {null_count} null values"
                )
    
    # Log row count
    logging.info(f"Validated table '{table_name}': {len(df):,} rows, {len(df.columns)} columns")
    
    return True


def ingest_df(df: pd.DataFrame, table_name: str, engine: Engine, 
              load_mode: str = 'replace') -> None:
    """
    Ingest a DataFrame into a specified database table.
    
    Parameters:
    - df: DataFrame to ingest
    - table_name: Name of the table to create/replace/append
    - engine: SQLAlchemy engine
    - load_mode: 'replace' for full refresh, 'append' for incremental
    """
    try:
        if_exists = load_mode if load_mode in ['replace', 'append'] else 'replace'
        df.to_sql(name=table_name, con=engine, if_exists=if_exists, index=False)
        logging.info(f"Successfully ingested table '{table_name}' ({len(df):,} rows)")
    except Exception as e:
        logging.error(f"Error ingesting table '{table_name}': {e}")
        raise


def get_table_row_count(engine: Engine, table_name: str) -> int:
    """Get the current row count of a table."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            return result.scalar()
    except Exception:
        return 0


def load_raw_data(data_path: Optional[str] = None, 
                  load_mode: Optional[str] = None) -> Dict[str, int]:
    """
    Load all CSV files from the specified folder into the database.
    
    Parameters:
    - data_path: Optional override for data directory
    - load_mode: Optional override for load mode ('replace' or 'append')
    
    Returns:
    - Dictionary of table names to row counts
    """
    config = get_config()
    setup_logging(config)
    
    # Use config values if not overridden
    if data_path is None:
        data_path = str(get_project_root() / config.raw_data_dir)
    if load_mode is None:
        load_mode = config.load_mode
    
    logging.info("=" * 60)
    logging.info("Starting Data Ingestion Pipeline")
    logging.info(f"Data directory: {data_path}")
    logging.info(f"Load mode: {load_mode}")
    logging.info("=" * 60)
    
    results = {}
    
    try:
        if not os.path.exists(data_path):
            logging.error(f"Data directory '{data_path}' does not exist.")
            print(f"Directory '{data_path}' not found.")
            return results
        
        start = time.time()
        csv_files = [f for f in os.listdir(data_path) if f.endswith('.csv')]
        
        if not csv_files:
            logging.warning(f"No CSV files found in '{data_path}'.")
            print(f"No CSV files found in '{data_path}'.")
            return results
        
        logging.info(f"Found {len(csv_files)} CSV files to process")
        
        engine = create_db_engine(config)
        
        for file in csv_files:
            file_path = os.path.join(data_path, file)
            file_start = time.time()
            
            try:
                logging.info(f"Loading '{file}'...")
                
                # Read CSV with optimized settings for large files
                df = pd.read_csv(file_path, low_memory=False)
                table_name = os.path.splitext(file)[0]
                
                # Validate before ingestion
                if config.etl.get('validate_after_load', True):
                    validate_dataframe(df, table_name, config)
                
                # Ingest to database
                ingest_df(df, table_name, engine, load_mode)
                results[table_name] = len(df)
                
                file_time = (time.time() - file_start) / 60
                logging.info(f"Completed '{table_name}' in {file_time:.2f} minutes")
                
            except Exception as e:
                logging.error(f"Failed to process '{file}': {e}")
                print(f"Failed to process file '{file}': {e}")
        
        end = time.time()
        total_time = (end - start) / 60
        total_rows = sum(results.values())
        
        logging.info("=" * 60)
        logging.info("Ingestion Complete")
        logging.info(f"Total tables: {len(results)}")
        logging.info(f"Total rows: {total_rows:,}")
        logging.info(f"Total time: {total_time:.2f} minutes")
        logging.info("=" * 60)
        
        print(f"\n✅ Ingestion complete: {len(results)} tables, {total_rows:,} rows in {total_time:.2f} min")
        
    except Exception as e:
        logging.error(f"Unexpected error during data loading: {e}")
        raise
    
    return results


if __name__ == '__main__':
    load_raw_data()
