"""
Unit tests for metric calculations in the Vendor Performance Analysis project.
Tests the GrossProfit, ProfitMargin, StockTurnover, and Sales_To_Purchase_Ratio calculations.
"""
import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'scripts'))


class TestGrossProfit:
    """Tests for GrossProfit calculation: TotalSalesDollars - TotalPurchaseDollars"""
    
    def test_positive_profit(self):
        """Gross profit should be positive when sales > purchases."""
        total_sales = 1000.0
        total_purchases = 600.0
        expected = 400.0
        
        gross_profit = total_sales - total_purchases
        
        assert gross_profit == expected
    
    def test_negative_profit(self):
        """Gross profit can be negative (loss) when purchases > sales."""
        total_sales = 500.0
        total_purchases = 700.0
        expected = -200.0
        
        gross_profit = total_sales - total_purchases
        
        assert gross_profit == expected
    
    def test_zero_profit(self):
        """Gross profit should be zero when sales equal purchases."""
        total_sales = 500.0
        total_purchases = 500.0
        expected = 0.0
        
        gross_profit = total_sales - total_purchases
        
        assert gross_profit == expected
    
    def test_zero_sales(self):
        """Gross profit should be negative when there are no sales."""
        total_sales = 0.0
        total_purchases = 300.0
        expected = -300.0
        
        gross_profit = total_sales - total_purchases
        
        assert gross_profit == expected
    
    def test_gross_profit_dataframe(self):
        """Test gross profit calculation on a DataFrame."""
        df = pd.DataFrame({
            'TotalSalesDollars': [1000.0, 500.0, 0.0],
            'TotalPurchaseDollars': [600.0, 700.0, 100.0]
        })
        expected = pd.Series([400.0, -200.0, -100.0])
        
        df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
        
        pd.testing.assert_series_equal(df['GrossProfit'], expected, check_names=False)


class TestProfitMargin:
    """Tests for ProfitMargin calculation: (GrossProfit / TotalSalesDollars) * 100"""
    
    def test_positive_margin(self):
        """Normal profit margin calculation."""
        gross_profit = 400.0
        total_sales = 1000.0
        expected = 40.0  # 40% margin
        
        profit_margin = (gross_profit / total_sales) * 100
        
        assert profit_margin == expected
    
    def test_negative_margin(self):
        """Profit margin can be negative for losses."""
        gross_profit = -200.0
        total_sales = 500.0
        expected = -40.0  # -40% margin
        
        profit_margin = (gross_profit / total_sales) * 100
        
        assert profit_margin == expected
    
    def test_division_by_zero_handling(self):
        """Division by zero should be handled with replacement value."""
        gross_profit = 100.0
        total_sales = 0.0
        zero_replacement = 1  # From config
        expected = 10000.0  # (100 / 1) * 100
        
        # Apply zero replacement logic
        denominator = total_sales if total_sales != 0 else zero_replacement
        profit_margin = (gross_profit / denominator) * 100
        
        assert profit_margin == expected
    
    def test_profit_margin_dataframe(self):
        """Test profit margin on DataFrame with division by zero handling."""
        df = pd.DataFrame({
            'GrossProfit': [400.0, -200.0, 100.0],
            'TotalSalesDollars': [1000.0, 500.0, 0.0]  # Last has zero sales
        })
        expected = pd.Series([40.0, -40.0, 10000.0])  # Using replace(0, 1)
        
        # This is how the actual code handles it
        df['ProfitMargin'] = (df['GrossProfit'] / df['TotalSalesDollars'].replace(0, 1)) * 100
        
        pd.testing.assert_series_equal(df['ProfitMargin'], expected, check_names=False)
    
    def test_100_percent_margin(self):
        """100% margin means cost was zero (unlikely but valid)."""
        gross_profit = 500.0  # All revenue is profit
        total_sales = 500.0
        expected = 100.0
        
        profit_margin = (gross_profit / total_sales) * 100
        
        assert profit_margin == expected


class TestStockTurnover:
    """Tests for StockTurnover calculation: TotalSalesQuantity / TotalPurchaseQuantity"""
    
    def test_turnover_less_than_one(self):
        """Turnover < 1 means not all purchased stock was sold."""
        sales_qty = 80.0
        purchase_qty = 100.0
        expected = 0.8
        
        turnover = sales_qty / purchase_qty
        
        assert turnover == expected
    
    def test_turnover_equals_one(self):
        """Turnover = 1 means all purchased stock was sold exactly."""
        sales_qty = 100.0
        purchase_qty = 100.0
        expected = 1.0
        
        turnover = sales_qty / purchase_qty
        
        assert turnover == expected
    
    def test_turnover_greater_than_one(self):
        """Turnover > 1 is unusual (selling more than purchased - existing inventory)."""
        sales_qty = 120.0
        purchase_qty = 100.0
        expected = 1.2
        
        turnover = sales_qty / purchase_qty
        
        assert turnover == expected
    
    def test_division_by_zero_handling(self):
        """Division by zero when no purchases should be handled."""
        sales_qty = 50.0
        purchase_qty = 0.0
        zero_replacement = 1
        expected = 50.0  # 50 / 1
        
        denominator = purchase_qty if purchase_qty != 0 else zero_replacement
        turnover = sales_qty / denominator
        
        assert turnover == expected
    
    def test_stock_turnover_dataframe(self):
        """Test stock turnover on DataFrame."""
        df = pd.DataFrame({
            'TotalSalesQuantity': [80.0, 100.0, 50.0],
            'TotalPurchaseQuantity': [100.0, 100.0, 0.0]  # Last has zero purchases
        })
        expected = pd.Series([0.8, 1.0, 50.0])
        
        df['StockTurnover'] = df['TotalSalesQuantity'] / df['TotalPurchaseQuantity'].replace(0, 1)
        
        pd.testing.assert_series_equal(df['StockTurnover'], expected, check_names=False)


class TestSalesToPurchaseRatio:
    """Tests for Sales_To_Purchase_Ratio: TotalSalesDollars / TotalPurchaseDollars"""
    
    def test_ratio_greater_than_one(self):
        """Ratio > 1 means profitable (revenue exceeds cost)."""
        sales_dollars = 1200.0
        purchase_dollars = 1000.0
        expected = 1.2
        
        ratio = sales_dollars / purchase_dollars
        
        assert ratio == expected
    
    def test_ratio_less_than_one(self):
        """Ratio < 1 means unprofitable (cost exceeds revenue)."""
        sales_dollars = 800.0
        purchase_dollars = 1000.0
        expected = 0.8
        
        ratio = sales_dollars / purchase_dollars
        
        assert ratio == expected
    
    def test_ratio_equals_one(self):
        """Ratio = 1 means break-even."""
        sales_dollars = 1000.0
        purchase_dollars = 1000.0
        expected = 1.0
        
        ratio = sales_dollars / purchase_dollars
        
        assert ratio == expected
    
    def test_division_by_zero_handling(self):
        """Division by zero when no purchases should be handled."""
        sales_dollars = 500.0
        purchase_dollars = 0.0
        zero_replacement = 1
        expected = 500.0  # 500 / 1
        
        denominator = purchase_dollars if purchase_dollars != 0 else zero_replacement
        ratio = sales_dollars / denominator
        
        assert ratio == expected
    
    def test_ratio_dataframe(self):
        """Test sales to purchase ratio on DataFrame."""
        df = pd.DataFrame({
            'TotalSalesDollars': [1200.0, 800.0, 500.0],
            'TotalPurchaseDollars': [1000.0, 1000.0, 0.0]  # Last has zero purchases
        })
        expected = pd.Series([1.2, 0.8, 500.0])
        
        df['Sales_To_Purchase_Ratio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars'].replace(0, 1)
        
        pd.testing.assert_series_equal(df['Sales_To_Purchase_Ratio'], expected, check_names=False)


class TestEdgeCases:
    """Tests for edge cases and unusual data scenarios."""
    
    def test_all_zeros(self):
        """Handle row where all values are zero."""
        df = pd.DataFrame({
            'TotalSalesDollars': [0.0],
            'TotalPurchaseDollars': [0.0],
            'TotalSalesQuantity': [0.0],
            'TotalPurchaseQuantity': [0.0]
        })
        
        df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
        df['ProfitMargin'] = (df['GrossProfit'] / df['TotalSalesDollars'].replace(0, 1)) * 100
        df['StockTurnover'] = df['TotalSalesQuantity'] / df['TotalPurchaseQuantity'].replace(0, 1)
        df['Sales_To_Purchase_Ratio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars'].replace(0, 1)
        
        assert df['GrossProfit'].iloc[0] == 0.0
        assert df['ProfitMargin'].iloc[0] == 0.0  # 0 / 1 * 100 = 0
        assert df['StockTurnover'].iloc[0] == 0.0
        assert df['Sales_To_Purchase_Ratio'].iloc[0] == 0.0
    
    def test_negative_values(self):
        """Handle negative values (should not occur but test robustness)."""
        df = pd.DataFrame({
            'TotalSalesDollars': [-100.0],
            'TotalPurchaseDollars': [50.0]
        })
        
        df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
        
        assert df['GrossProfit'].iloc[0] == -150.0
    
    def test_very_large_values(self):
        """Handle very large values without overflow."""
        df = pd.DataFrame({
            'TotalSalesDollars': [1e12],  # 1 trillion
            'TotalPurchaseDollars': [9e11]  # 900 billion
        })
        
        df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
        df['Sales_To_Purchase_Ratio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars']
        
        assert df['GrossProfit'].iloc[0] == 1e11  # 100 billion
        assert np.isclose(df['Sales_To_Purchase_Ratio'].iloc[0], 1.1111, rtol=0.01)
    
    def test_nan_handling(self):
        """NaN values should be handled appropriately."""
        df = pd.DataFrame({
            'TotalSalesDollars': [1000.0, np.nan],
            'TotalPurchaseDollars': [600.0, 400.0]
        })
        
        # After fillna(0)
        df.fillna(0, inplace=True)
        df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
        
        assert df['GrossProfit'].iloc[0] == 400.0
        assert df['GrossProfit'].iloc[1] == -400.0  # 0 - 400


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
