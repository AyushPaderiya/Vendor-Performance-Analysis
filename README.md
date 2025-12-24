# 📊 Vendor Performance Analysis

A comprehensive end-to-end data analytics project that evaluates vendor and inventory performance in a retail setting using Python, SQL, and Power BI.

## 🚀 Overview

This project ingests raw sales and purchase data, computes key performance metrics, performs exploratory and statistical analysis, and presents actionable insights through a Power BI dashboard and PDF report.

## 🎯 Objectives & Business Questions

* Identify top-performing and underperforming vendors and brands
* Analyze inventory turnover and cost locked in unsold stock
* Determine bulk-purchasing benefits for cost efficiency
* Statistically test differences in profit margins across vendor segments
* Provide clear, data-driven recommendations for procurement and pricing strategies

## 🧰 Tech Stack & Tools

* **Extraction & Transformation**: Python, Pandas, and SQLite/SQLAlchemy
* **Analysis**: SQL (joins, CTEs, aggregation), Pandas, Seaborn, Matplotlib, SciPy
* **Visualization**: Power BI Dashboard
* **Reporting**: PDF summary for business stakeholders
* **Environment**: Jupyter Notebooks for EDA and deep dives

## 📂 Repository Structure

```
/
├── config/
│   ├── config.yaml              # Centralized configuration
│   └── config_loader.py         # Configuration loader utility
├── data/                        # Raw CSV files (6 tables)
├── docs/
│   ├── data_dictionary.md       # Complete schema documentation
│   └── dashboard_narrative.md   # Dashboard storytelling guide
├── scripts/
│   ├── ingestion_db.py          # Load CSVs into SQLite
│   └── get_vendor_summary.py    # SQL/Python summary table builder
├── notebooks/
│   ├── 01_Exploratory_Data_Analysis.ipynb
│   └── 02_Vendor_Performance_Analysis.ipynb
├── dashboard/
│   └── Vendor Performance Dashboard.pbix
├── reports/
│   └── Vendor Performance Report.pdf
├── tests/
│   ├── test_metrics.py          # Unit tests for calculations
│   └── test_data_validation.py  # Data integrity tests
├── logs/
├── .gitignore
└── requirements.txt
```

## 🧪 How to Run

1. **Clone** the repository

   ```bash
   git clone https://github.com/AyushPaderiya/Vendor-Performance-Analysis.git
   cd Vendor-Performance-Analysis
   ```

2. **Data Setup**
   
   The dataset is too large for GitHub and is hosted externally.
   * [Download Data Here](https://drive.google.com/file/d/11gvpbVVY735zTfNOqRPdjpsLiRvQGHVS/view?usp=sharing)
   * Extract the ZIP contents directly into the `data/` folder in the project root.

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```
4. **Run data ingestion and transformation**

   ```bash
   python scripts/ingestion_db.py
   python scripts/get_vendor_summary.py
   ```
5. **Explore analysis**
   Open and run the Jupyter notebooks in `/notebooks/`
6. **View dashboard**
   Open `dashboard/vendor_performance.pbix` in Power BI
7. **Review report**
   Refer to `reports/Vendor Performance Report.pdf` for key findings and recommendations

## 📈 Key Insights

* **Vendor Concentration Risk**: Top 10 vendors account for about 65% of total purchases
* **Bulk Purchase Savings**: Large orders yield \~72% lower unit costs
* **Unsold Inventory**: Approximately \$2.7M tied up in slow-moving stock
* **Margin Differences**: Statistical analysis reveals significant margin variance across vendor tiers

## ✅ Recommendations

* Rebalance vendor portfolio to reduce over-dependence
* Negotiate bulk purchasing for cost efficiencies
* Price or promo optimization for low-volume, high-margin brands
* Clear excess inventory to free up capital
* Automate reporting pipeline for continuous insights

## 🛠️ Customization & Extensions

Feel free to adapt for other industries or data sets—e.g.:

* **Scale out** with larger SQL databases (PostgreSQL, MySQL)
* **Migrate dashboard** to PowerBI Service or Tableau
* **Add predictive analytics**—demand forecasting, vendor risk modeling

## 🙋‍♂️ Author

**Ayush Paderiya**

* LinkedIn: \[[Ayush Paderiya](https://www.linkedin.com/in/ayush-paderiya-94b2a3131)]
* Email: [paderiyaayush@gmail.com](paderiyaayush@gmail.com)
