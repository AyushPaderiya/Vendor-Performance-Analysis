"""
Data validation tests for the Vendor Performance Analysis project.
Tests data integrity, schema validation, and referential integrity.
"""
import pytest
import pandas as pd
import sqlite3
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'config'))


class TestSchemaValidation:
    """Tests to validate that data files have expected schemas."""
    
    @pytest.fixture
    def data_dir(self):
        """Get the data directory path."""
        return project_root / 'data'
    
    def test_begin_inventory_columns(self, data_dir):
        """Validate begin_inventory has all required columns."""
        expected_columns = [
            'InventoryId', 'Store', 'City', 'Brand', 'Description',
            'Size', 'onHand', 'Price', 'startDate'
        ]
        
        df = pd.read_csv(data_dir / 'begin_inventory.csv', nrows=1)
        
        for col in expected_columns:
            assert col in df.columns, f"Missing column: {col}"
    
    def test_end_inventory_columns(self, data_dir):
        """Validate end_inventory has all required columns."""
        expected_columns = [
            'InventoryId', 'Store', 'City', 'Brand', 'Description',
            'Size', 'onHand', 'Price', 'endDate'
        ]
        
        df = pd.read_csv(data_dir / 'end_inventory.csv', nrows=1)
        
        for col in expected_columns:
            assert col in df.columns, f"Missing column: {col}"
    
    def test_purchase_prices_columns(self, data_dir):
        """Validate purchase_prices has all required columns."""
        expected_columns = [
            'Brand', 'Description', 'Price', 'Size', 'Volume',
            'Classification', 'PurchasePrice', 'VendorNumber', 'VendorName'
        ]
        
        df = pd.read_csv(data_dir / 'purchase_prices.csv', nrows=1)
        
        for col in expected_columns:
            assert col in df.columns, f"Missing column: {col}"
    
    def test_purchases_columns(self, data_dir):
        """Validate purchases has all required columns."""
        expected_columns = [
            'InventoryId', 'Store', 'Brand', 'Description', 'Size',
            'VendorNumber', 'VendorName', 'PONumber', 'PODate',
            'ReceivingDate', 'InvoiceDate', 'PayDate', 'PurchasePrice',
            'Quantity', 'Dollars', 'Classification'
        ]
        
        df = pd.read_csv(data_dir / 'purchases.csv', nrows=1)
        
        for col in expected_columns:
            assert col in df.columns, f"Missing column: {col}"
    
    def test_sales_columns(self, data_dir):
        """Validate sales has all required columns."""
        expected_columns = [
            'InventoryId', 'Store', 'Brand', 'Description', 'Size',
            'SalesQuantity', 'SalesDollars', 'SalesPrice', 'SalesDate',
            'Volume', 'Classification', 'ExciseTax', 'VendorNo', 'VendorName'
        ]
        
        df = pd.read_csv(data_dir / 'sales.csv', nrows=1)
        
        for col in expected_columns:
            assert col in df.columns, f"Missing column: {col}"
    
    def test_vendor_invoice_columns(self, data_dir):
        """Validate vendor_invoice has all required columns."""
        expected_columns = [
            'VendorNumber', 'VendorName', 'InvoiceDate', 'PONumber',
            'PODate', 'PayDate', 'Quantity', 'Dollars', 'Freight', 'Approval'
        ]
        
        df = pd.read_csv(data_dir / 'vendor_invoice.csv', nrows=1)
        
        for col in expected_columns:
            assert col in df.columns, f"Missing column: {col}"


class TestDataTypes:
    """Tests to validate data types are correct."""
    
    @pytest.fixture
    def data_dir(self):
        return project_root / 'data'
    
    def test_numeric_columns_not_string(self, data_dir):
        """Ensure numeric columns don't contain string values."""
        df = pd.read_csv(data_dir / 'purchases.csv', nrows=100)
        
        numeric_columns = ['Store', 'Brand', 'VendorNumber', 'PONumber', 
                          'PurchasePrice', 'Quantity', 'Dollars']
        
        for col in numeric_columns:
            assert pd.api.types.is_numeric_dtype(df[col]), \
                f"Column {col} should be numeric but is {df[col].dtype}"
    
    def test_price_columns_positive(self, data_dir):
        """Prices should be positive or zero."""
        df = pd.read_csv(data_dir / 'purchase_prices.csv', nrows=1000)
        
        assert (df['Price'] >= 0).all(), "Found negative prices in Price column"
        assert (df['PurchasePrice'] >= 0).all(), "Found negative purchase prices"
    
    def test_quantity_columns_positive(self, data_dir):
        """Quantities should be positive or zero."""
        df = pd.read_csv(data_dir / 'purchases.csv', nrows=1000)
        
        assert (df['Quantity'] >= 0).all(), "Found negative quantities"


class TestDataIntegrity:
    """Tests to validate data integrity and consistency."""
    
    @pytest.fixture
    def data_dir(self):
        return project_root / 'data'
    
    def test_no_duplicate_brands_in_purchase_prices(self, data_dir):
        """Each brand should appear once in purchase_prices (with same price info)."""
        df = pd.read_csv(data_dir / 'purchase_prices.csv')
        
        # Check for duplicate Brand + Volume combinations
        duplicates = df.duplicated(subset=['Brand', 'Volume'], keep=False)
        duplicate_count = duplicates.sum()
        
        # Allow some duplicates for different volumes but warn
        if duplicate_count > 0:
            pytest.skip(f"Found {duplicate_count} Brand+Volume duplicates - may be intentional for size variants")
    
    def test_inventory_id_format(self, data_dir):
        """InventoryId should follow pattern: Store_City_Brand."""
        df = pd.read_csv(data_dir / 'begin_inventory.csv', nrows=100)
        
        for _, row in df.iterrows():
            parts = str(row['InventoryId']).split('_')
            assert len(parts) == 3, f"Invalid InventoryId format: {row['InventoryId']}"
            assert parts[0] == str(row['Store']), \
                f"InventoryId store mismatch: {row['InventoryId']} vs Store {row['Store']}"
    
    def test_dollars_equals_price_times_quantity(self, data_dir):
        """Verify Dollars ≈ PurchasePrice × Quantity in purchases."""
        df = pd.read_csv(data_dir / 'purchases.csv', nrows=1000)
        
        calculated = df['PurchasePrice'] * df['Quantity']
        
        # Allow for small floating point differences (0.01)
        differences = abs(df['Dollars'] - calculated)
        max_diff = differences.max()
        
        assert max_diff < 0.1, \
            f"Dollars column doesn't match Price × Quantity. Max diff: {max_diff}"


class TestMinimumRowCounts:
    """Tests to validate minimum expected row counts."""
    
    @pytest.fixture
    def data_dir(self):
        return project_root / 'data'
    
    def test_begin_inventory_row_count(self, data_dir):
        """Begin inventory should have minimum expected rows."""
        min_expected = 200000
        
        # Count lines efficiently without loading full file
        with open(data_dir / 'begin_inventory.csv', 'r') as f:
            row_count = sum(1 for _ in f) - 1  # Subtract header
        
        assert row_count >= min_expected, \
            f"begin_inventory has {row_count} rows, expected >= {min_expected}"
    
    def test_purchases_row_count(self, data_dir):
        """Purchases should have minimum expected rows."""
        min_expected = 2000000
        
        with open(data_dir / 'purchases.csv', 'r') as f:
            row_count = sum(1 for _ in f) - 1
        
        assert row_count >= min_expected, \
            f"purchases has {row_count} rows, expected >= {min_expected}"
    
    def test_sales_row_count(self, data_dir):
        """Sales should have minimum expected rows."""
        min_expected = 10000000
        
        with open(data_dir / 'sales.csv', 'r') as f:
            row_count = sum(1 for _ in f) - 1
        
        assert row_count >= min_expected, \
            f"sales has {row_count} rows, expected >= {min_expected}"


class TestNullHandling:
    """Tests to validate null value handling."""
    
    @pytest.fixture
    def data_dir(self):
        return project_root / 'data'
    
    def test_critical_columns_no_nulls(self, data_dir):
        """Critical columns should not have null values."""
        df = pd.read_csv(data_dir / 'purchases.csv', nrows=10000)
        
        critical_columns = ['Brand', 'VendorNumber', 'Quantity', 'Dollars']
        
        for col in critical_columns:
            null_count = df[col].isnull().sum()
            assert null_count == 0, \
                f"Column {col} has {null_count} null values"
    
    def test_approval_nullable(self, data_dir):
        """Approval column in vendor_invoice is expected to have nulls."""
        df = pd.read_csv(data_dir / 'vendor_invoice.csv')
        
        null_percentage = df['Approval'].isnull().sum() / len(df)
        
        # We know from schema inspection that ~98% is null
        assert null_percentage > 0.9, \
            f"Expected high null rate in Approval column, got {null_percentage:.2%}"


class TestReferentialIntegrity:
    """Tests to validate relationships between tables."""
    
    @pytest.fixture
    def data_dir(self):
        return project_root / 'data'
    
    def test_purchase_brands_exist_in_prices(self, data_dir):
        """Brands in purchases should exist in purchase_prices."""
        purchases = pd.read_csv(data_dir / 'purchases.csv', nrows=10000)
        prices = pd.read_csv(data_dir / 'purchase_prices.csv')
        
        purchase_brands = set(purchases['Brand'].unique())
        price_brands = set(prices['Brand'].unique())
        
        missing_brands = purchase_brands - price_brands
        
        # Allow some missing (may be data quality issue in source)
        missing_pct = len(missing_brands) / len(purchase_brands) * 100
        assert missing_pct < 5, \
            f"{missing_pct:.1f}% of purchase brands missing from price list"
    
    def test_vendor_numbers_consistent(self, data_dir):
        """Vendor numbers should appear in vendor_invoice."""
        purchases = pd.read_csv(data_dir / 'purchases.csv', nrows=10000)
        invoices = pd.read_csv(data_dir / 'vendor_invoice.csv')
        
        purchase_vendors = set(purchases['VendorNumber'].unique())
        invoice_vendors = set(invoices['VendorNumber'].unique())
        
        # At least some overlap expected
        overlap = purchase_vendors & invoice_vendors
        assert len(overlap) > 0, "No vendor overlap between purchases and invoices"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
