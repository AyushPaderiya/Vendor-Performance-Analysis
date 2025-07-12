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
├── data.zip                         # Raw CSV files
├── scripts/
│   ├── ingestion_db.py          # Load CSVs into SQLite
│   └── get_vendor_summary.py    # SQL/Python summary table builder
├── notebooks/
│   ├── Exploratory Data Analysis.ipynb
│   └── Vendor Performance Analysis.ipynb
├── dashboard/
│   └── vendor_performance.pbix  # Power BI file
├── reports/
│   └── Vendor Performance Report.pdf
├── logs/
│   └── ingestion_db.log
└── requirements.txt              # Python dependencies
```

## 🧪 How to Run

1. **Clone** the repository

   ```bash
   git clone https://github.com/AyushPaderiya/Vendor-Performance-Analysis.git
   cd Vendor-Performance-Analysis
   ```
2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```
3. **Run data ingestion and transformation**

   ```bash
   python scripts/ingestion_db.py
   python scripts/get_vendor_summary.py
   ```
4. **Explore analysis**
   Open and run the Jupyter notebooks in `/notebooks/`
5. **View dashboard**
   Open `dashboard/vendor_performance.pbix` in Power BI
6. **Review report**
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
