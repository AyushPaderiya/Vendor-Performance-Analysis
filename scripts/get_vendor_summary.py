import pandas as pd
import sqlite3
import logging
import time
from ingestion_db import ingest_db 

# Setup logging
logging.basicConfig(
    filename="logs/get_vendor_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

def create_vendor_summary(conn):
    """
    Creates a vendor-wise summary by merging purchase, sales, and freight data.
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
            GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume
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
    
        df = pd.read_sql_query(query, conn)
    
        end = time.time()
        total_time = (end - start) / 60
        logging.info(f"Vendor summary created. Time taken: {total_time:.2f} minutes")
    
        return df
    except Exception as e:
        logging.error(f"Error creating vendor summary: {e}")
        return pd.DataFrame()  # Return empty DataFrame to avoid crashing


def clean_data(df):
    """
    Cleans and enriches the vendor summary data.
    """
    try:
        # Type conversion
        df['Volume'] = df['Volume'].astype('float')
    
        # Fill missing values
        df.fillna(0, inplace=True)
    
        # Trim spaces
        df['VendorName'] = df['VendorName'].str.strip()
        df['Description'] = df['Description'].str.strip()
    
        # New calculated columns
        df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
        df['ProfitMargin'] = (df['GrossProfit'] / df['TotalSalesDollars'].replace(0, 1)) * 100
        df['StockTurnover'] = df['TotalSalesQuantity'] / df['TotalPurchaseQuantity'].replace(0, 1)
        df['Sales_To_Purchase_Ratio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars'].replace(0, 1)
    
        return df
    except Exception as e:
        logging.error(f"Error cleaning data: {e}")
        return df  # Return partially cleaned data if error occurs


if __name__ == '__main__':
    conn = sqlite3.connect('inventory.db')

    logging.info('Creating Vendor Summary Table...')
    summary_df = create_vendor_summary(conn)
    if summary_df.empty:
        logging.warning("Summary DataFrame is empty. Skipping cleaning and ingestion.")
    else:
        logging.info(f"Vendor summary preview:\n{summary_df.head()}")

        logging.info('Cleaning Data...')
        clean_df = clean_data(summary_df)
        logging.info(f"Cleaned data preview:\n{clean_df.head()}")

        logging.info('Ingesting Data...')
        ingest_db(clean_df, 'vendor_sales_summary', conn)
        logging.info('Ingestion Completed.')
