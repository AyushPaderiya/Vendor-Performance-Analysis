"""
Vendor summary generation module for Vendor Performance Analysis.
Creates aggregated vendor-wise summary by merging purchase, sales, and freight data.

Features:
- Configuration-driven settings
- Improved missing value handling (column-specific)
- Standardized SQLAlchemy connections
- Calculated metrics with proper edge case handling
"""
import pandas as pd
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
    log_file = get_project_root() / 'logs' / 'get_vendor_summary.log'
    
    # Ensure log directory exists
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        filename=str(log_file),
        level=getattr(logging, log_config.get('level', 'INFO')),
        format=log_config.get('format', '%(asctime)s - %(levelname)s - %(message)s'),
        filemode='a'
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


def create_vendor_summary(engine: Engine) -> pd.DataFrame:
    """
    Creates a vendor-wise summary by merging purchase, sales, and freight data.
    
    Uses SQL CTEs for efficient aggregation before joining.
    
    Parameters:
    - engine: SQLAlchemy engine connected to the database
    
    Returns:
    - DataFrame with vendor summary data
    """
    try:
        start = time.time()
        
        query = """
        WITH FreightSummary AS (
            SELECT 
                VendorNumber, 
                SUM(Freight) AS FreightCost
            FROM vendor_invoice
            GROUP BY VendorNumber
        ),
        
        PurchaseSummary AS (
            SELECT 
                p.VendorNumber,
                p.VendorName,
                p.Brand,
                p.Description,
                p.PurchasePrice,
                pp.Volume,
                pp.Price AS ActualPrice,
                SUM(p.Quantity) AS TotalPurchaseQuantity,
                SUM(p.Dollars) AS TotalPurchaseDollars
            FROM purchases p
            JOIN purchase_prices pp USING(Brand)
            WHERE p.PurchasePrice > 0
            GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, 
                     p.PurchasePrice, pp.Price, pp.Volume
        ),
        
        SalesSummary AS (
            SELECT 
                VendorNo,
                Brand,
                SUM(SalesQuantity) AS TotalSalesQuantity,
                SUM(SalesDollars) AS TotalSalesDollars,
                SUM(SalesPrice) AS TotalSalesPrice,
                SUM(ExciseTax) AS TotalExciseTax
            FROM sales
            GROUP BY VendorNo, Brand
        )
        
        SELECT 
            ps.*, 
            ss.TotalSalesQuantity,
            ss.TotalSalesDollars,
            ss.TotalSalesPrice,
            ss.TotalExciseTax,
            fs.FreightCost
        FROM PurchaseSummary ps
        LEFT JOIN SalesSummary ss
            ON ps.VendorNumber = ss.VendorNo AND ps.Brand = ss.Brand
        LEFT JOIN FreightSummary fs
            ON ps.VendorNumber = fs.VendorNumber
        ORDER BY ps.TotalPurchaseDollars DESC
        """
        
        with engine.connect() as conn:
            df = pd.read_sql_query(text(query), conn)
        
        end = time.time()
        total_time = (end - start) / 60
        logging.info(f"Vendor summary created: {len(df):,} rows in {total_time:.2f} minutes")
        
        return df
        
    except Exception as e:
        logging.error(f"Error creating vendor summary: {e}")
        raise


def handle_missing_values(df: pd.DataFrame, config: Any) -> pd.DataFrame:
    """
    Handle missing values with column-specific strategies.
    
    This replaces the blanket fillna(0) approach with more thoughtful handling.
    
    Parameters:
    - df: DataFrame with potential missing values
    - config: Configuration object
    
    Returns:
    - DataFrame with missing values handled appropriately
    """
    missing_config = config.missing_values
    column_overrides = missing_config.get('column_overrides', {})
    
    # Document what we're doing
    null_counts_before = df.isnull().sum()
    total_nulls = null_counts_before.sum()
    
    if total_nulls > 0:
        logging.info(f"Handling {total_nulls} missing values across {(null_counts_before > 0).sum()} columns")
    
    # Apply column-specific strategies
    for col in df.columns:
        if df[col].isnull().sum() == 0:
            continue
            
        # Check for column-specific override
        if col in column_overrides:
            strategy = column_overrides[col]
        elif pd.api.types.is_numeric_dtype(df[col]):
            strategy = missing_config.get('numeric_strategy', 'zero')
        else:
            strategy = missing_config.get('text_strategy', 'unknown')
        
        # Apply strategy
        if strategy == 'zero':
            df[col] = df[col].fillna(0)
            logging.debug(f"Filled nulls in '{col}' with 0")
        elif strategy == 'mean':
            df[col] = df[col].fillna(df[col].mean())
            logging.debug(f"Filled nulls in '{col}' with mean")
        elif strategy == 'median':
            df[col] = df[col].fillna(df[col].median())
            logging.debug(f"Filled nulls in '{col}' with median")
        elif strategy == 'unknown':
            df[col] = df[col].fillna('UNKNOWN')
            logging.debug(f"Filled nulls in '{col}' with 'UNKNOWN'")
        elif strategy == 'drop':
            # Flag but don't drop - let caller decide
            logging.warning(f"Column '{col}' has nulls marked for dropping")
        # 'flag' strategy - leave nulls for downstream flagging
    
    return df


def calculate_metrics(df: pd.DataFrame, config: Any) -> pd.DataFrame:
    """
    Calculate derived metrics with proper edge case handling.
    
    Metrics calculated:
    - GrossProfit: TotalSalesDollars - TotalPurchaseDollars
    - ProfitMargin: (GrossProfit / TotalSalesDollars) * 100
    - StockTurnover: TotalSalesQuantity / TotalPurchaseQuantity
    - Sales_To_Purchase_Ratio: TotalSalesDollars / TotalPurchaseDollars
    
    Parameters:
    - df: DataFrame with sales and purchase totals
    - config: Configuration object
    
    Returns:
    - DataFrame with calculated metrics
    """
    metrics_config = config.metrics
    
    # GrossProfit: simple subtraction, no edge cases
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    
    # ProfitMargin: handle division by zero
    profit_margin_config = metrics_config.get('profit_margin', {})
    zero_replacement = profit_margin_config.get('zero_replacement', 1)
    decimal_places = profit_margin_config.get('decimal_places', 2)
    
    df['ProfitMargin'] = (
        df['GrossProfit'] / df['TotalSalesDollars'].replace(0, zero_replacement)
    ) * 100
    df['ProfitMargin'] = df['ProfitMargin'].round(decimal_places)
    
    # StockTurnover: handle division by zero
    turnover_config = metrics_config.get('stock_turnover', {})
    zero_replacement = turnover_config.get('zero_replacement', 1)
    decimal_places = turnover_config.get('decimal_places', 4)
    
    df['StockTurnover'] = (
        df['TotalSalesQuantity'] / df['TotalPurchaseQuantity'].replace(0, zero_replacement)
    )
    df['StockTurnover'] = df['StockTurnover'].round(decimal_places)
    
    # Sales_To_Purchase_Ratio: handle division by zero
    ratio_config = metrics_config.get('sales_to_purchase_ratio', {})
    zero_replacement = ratio_config.get('zero_replacement', 1)
    decimal_places = ratio_config.get('decimal_places', 4)
    
    df['Sales_To_Purchase_Ratio'] = (
        df['TotalSalesDollars'] / df['TotalPurchaseDollars'].replace(0, zero_replacement)
    )
    df['Sales_To_Purchase_Ratio'] = df['Sales_To_Purchase_Ratio'].round(decimal_places)
    
    logging.info("Calculated metrics: GrossProfit, ProfitMargin, StockTurnover, Sales_To_Purchase_Ratio")
    
    return df


def clean_data(df: pd.DataFrame, config: Optional[Any] = None) -> pd.DataFrame:
    """
    Cleans and enriches the vendor summary data.
    
    Steps:
    1. Type conversion
    2. Handle missing values (column-specific)
    3. Trim text whitespace
    4. Calculate derived metrics
    
    Parameters:
    - df: Raw vendor summary DataFrame
    - config: Optional configuration object (loaded if not provided)
    
    Returns:
    - Cleaned and enriched DataFrame
    """
    if config is None:
        config = get_config()
    
    try:
        start = time.time()
        
        # Type conversion
        df['Volume'] = df['Volume'].astype('float')
        
        # Handle missing values with column-specific strategies
        df = handle_missing_values(df, config)
        
        # Trim whitespace from text columns
        text_columns = ['VendorName', 'Description']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        # Calculate derived metrics
        df = calculate_metrics(df, config)
        
        end = time.time()
        total_time = (end - start) / 60
        logging.info(f"Data cleaned in {total_time:.4f} minutes")
        
        return df
        
    except Exception as e:
        logging.error(f"Error cleaning data: {e}")
        raise


def run_summary_pipeline(output_table: Optional[str] = None) -> pd.DataFrame:
    """
    Run the complete vendor summary pipeline.
    
    Parameters:
    - output_table: Optional override for output table name
    
    Returns:
    - Final vendor summary DataFrame
    """
    config = get_config()
    setup_logging(config)
    
    if output_table is None:
        output_table = config.output.get('summary_table', 'vendor_sales_summary')
    
    logging.info("=" * 60)
    logging.info("Starting Vendor Summary Pipeline")
    logging.info("=" * 60)
    
    engine = create_db_engine(config)
    
    # Step 1: Create summary from raw data
    logging.info("Step 1: Creating vendor summary from database...")
    summary_df = create_vendor_summary(engine)
    
    if summary_df.empty:
        logging.warning("Summary DataFrame is empty. Check if raw data was ingested.")
        return summary_df
    
    logging.info(f"Created summary with {len(summary_df):,} rows")
    
    # Step 2: Clean and enrich data
    logging.info("Step 2: Cleaning and calculating metrics...")
    clean_df = clean_data(summary_df, config)
    
    # Step 3: Save to database
    logging.info(f"Step 3: Saving to table '{output_table}'...")
    clean_df.to_sql(name=output_table, con=engine, if_exists='replace', index=False)
    
    logging.info("=" * 60)
    logging.info("Pipeline Complete")
    logging.info(f"Output table: {output_table} ({len(clean_df):,} rows)")
    logging.info("=" * 60)
    
    print(f"\n✅ Summary complete: {len(clean_df):,} rows saved to '{output_table}'")
    
    return clean_df


if __name__ == '__main__':
    run_summary_pipeline()
