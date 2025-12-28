# 📊 Vendor Performance Analysis

> **End-to-end data analytics solution for retail vendor performance evaluation and inventory optimization**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-SQLite-lightgrey.svg)](https://www.sqlite.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-yellow.svg)](https://powerbi.microsoft.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Table of Contents
- [Overview](#-overview)
- [Business Context](#-business-context)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Installation & Setup](#-installation--setup)
- [Key Insights](#-key-insights)
- [Dashboard Preview](#-dashboard-preview)
- [Project Learnings](#-project-learnings)
- [Future Enhancements](#-future-enhancements)
- [Contact](#-contact)

## 🎯 Overview

This project delivers a comprehensive vendor performance evaluation system for retail operations, combining **data engineering**, **statistical analysis**, and **business intelligence**. The solution processes raw transactional data through an automated ETL pipeline, performs advanced analytics using Python and SQL, and presents actionable insights through an interactive Power BI dashboard.

### Key Features
- Automated data ingestion and transformation pipeline
- SQL-based analytical queries with CTEs and window functions
- Statistical hypothesis testing for margin analysis
- Interactive Power BI dashboard with drill-down capabilities
- Comprehensive PDF report for stakeholders
- Unit-tested metric calculations for data reliability

## 💼 Business Context

### Problem Statement
Retail organizations often struggle with:
- Identifying which vendors deliver the best value and margins
- Managing inventory costs tied up in slow-moving stock
- Optimizing bulk purchasing strategies
- Making data-driven procurement decisions

### Solution Delivered
This analytics solution provides:
- **Vendor Scorecards**: Performance metrics including profit margins, sales velocity, and inventory turnover
- **Cost Optimization Analysis**: Quantified bulk purchasing benefits and unit cost variations
- **Inventory Health Monitoring**: Identification of dead stock and capital locked in unsold inventory
- **Statistical Validation**: Hypothesis testing to validate margin differences across vendor segments
- **Actionable Recommendations**: Data-backed strategies for procurement optimization

## 🛠 Tech Stack

### Data Engineering & Analysis
- **Python 3.8+**: Core programming language
- **Pandas**: Data manipulation and transformation
- **SQLite/SQLAlchemy**: Relational database and ORM
- **SQL**: Complex queries with CTEs, joins, and aggregations
- **NumPy**: Numerical computations

### Statistical Analysis & Visualization
- **SciPy**: Statistical hypothesis testing (t-tests, ANOVA)
- **Seaborn & Matplotlib**: Exploratory data visualization
- **Jupyter Notebooks**: Interactive analysis environment

### Business Intelligence
- **Power BI**: Interactive dashboard development
- **DAX**: Calculated measures and KPIs

### Development Tools
- **YAML**: Configuration management
- **Pytest**: Unit testing framework
- **Git**: Version control

## 🏗 Project Architecture

```
vendor-performance-analysis/
│
├── config/
│   ├── config.yaml              # Database paths, column mappings, thresholds
│   └── config_loader.py         # YAML configuration parser
│
├── data/                        # Raw CSV files (6 normalized tables)
│   ├── sales_fact.csv
│   ├── purchase_fact.csv
│   ├── vendor_dim.csv
│   ├── product_dim.csv
│   ├── inventory_snapshot.csv
│   └── dates_dim.csv
│
├── docs/
│   ├── data_dictionary.md       # Schema definitions and relationships
│   └── dashboard_narrative.md   # Dashboard insights and storytelling
│
├── scripts/
│   ├── ingestion_db.py          # ETL: CSV → SQLite with validation
│   └── get_vendor_summary.py    # Aggregation engine for vendor metrics
│
├── notebooks/
│   ├── 01_Exploratory_Data_Analysis.ipynb     # Univariate/bivariate EDA
│   └── 02_Vendor_Performance_Analysis.ipynb   # Statistical testing & insights
│
├── dashboard/
│   └── Vendor_Performance_Dashboard.pbix      # Interactive Power BI report
│
├── reports/
│   └── Vendor_Performance_Report.pdf          # Executive summary
│
├── tests/
│   ├── test_metrics.py                        # Unit tests for KPI calculations
│   └── test_data_validation.py                # Data integrity checks
│
├── logs/                        # Execution logs and error tracking
├── .gitignore
├── requirements.txt
└── README.md
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Power BI Desktop (for viewing dashboard)
- 2GB free disk space for data

### Step-by-Step Instructions

**1. Clone the repository**
```bash
git clone https://github.com/AyushPaderiya/Vendor-Performance-Analysis.git
cd Vendor-Performance-Analysis
```

**2. Create and activate virtual environment** *(recommended)*
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Download the dataset**

The dataset is hosted externally due to size constraints:
- **Download Link**: [Google Drive - Vendor Data (ZIP)](https://drive.google.com/file/d/11gvpbVVY735zTfNOqRPdjpsLiRvQGHVS/view?usp=sharing)
- Extract all contents into the `data/` folder
- Verify 6 CSV files are present

**5. Run the ETL pipeline**
```bash
python scripts/ingestion_db.py          # Creates SQLite database
python scripts/get_vendor_summary.py     # Generates vendor summary table
```

**6. Explore the analysis**
```bash
jupyter notebook notebooks/01_Exploratory_Data_Analysis.ipynb
```

**7. Open the dashboard**
- Launch Power BI Desktop
- Open `dashboard/Vendor Performance Dashboard.pbix`
- Refresh data connections if prompted

**8. Review the business report**
- Open `reports/Vendor Performance Report.pdf`

## 📊 Key Insights

### Vendor Performance Metrics

| Metric | Finding | Business Impact |
|--------|---------|----------------|
| **Vendor Concentration** | Top 10 vendors = 65% of purchases | High dependency risk |
| **Bulk Discount** | 72% lower unit costs on large orders | Significant savings opportunity |
| **Dead Inventory** | $2.7M in slow-moving stock | Capital inefficiency |
| **Margin Variance** | 8-15% difference across vendors (p < 0.05) | Opportunity for optimization |

### Statistical Analysis
- **Hypothesis Test**: Profit margins differ significantly across vendor tiers (ANOVA, α=0.05)
- **Correlation Analysis**: Strong negative correlation (-0.68) between purchase volume and unit cost
- **Inventory Turnover**: 40% of SKUs turn less than 2x annually

## 📈 Dashboard Preview

The Power BI dashboard includes:
- **Executive Summary**: High-level KPIs and trends
- **Vendor Scorecard**: Detailed performance by vendor
- **Inventory Analysis**: Stock levels, turnover rates, dead stock identification
- **Purchase Patterns**: Volume discounts, seasonal trends
- **Margin Analysis**: Profitability breakdown by vendor and category

*Interactive filters enable drill-down by time period, vendor, product category, and brand.*

## 🎓 Project Learnings

### Technical Skills Demonstrated
- **Data Engineering**: Built ETL pipeline with error handling and logging
- **SQL Proficiency**: Complex joins, CTEs, window functions, and aggregations
- **Statistical Analysis**: Hypothesis testing, confidence intervals, correlation analysis
- **BI Development**: Created interactive dashboards with DAX measures
- **Software Engineering**: Modular code design, configuration management, unit testing

### Business Skills Applied
- Translated business questions into analytical frameworks
- Derived actionable recommendations from statistical findings
- Communicated technical insights to non-technical stakeholders
- Balanced analytical rigor with practical business constraints

## 🔮 Future Enhancements

### Phase 1: Scalability
- [ ] Migrate to PostgreSQL/MySQL for production deployment
- [ ] Implement Apache Airflow for scheduled pipeline execution
- [ ] Add data quality monitoring and alerting

### Phase 2: Advanced Analytics
- [ ] Demand forecasting using time series models (ARIMA/Prophet)
- [ ] Vendor risk scoring with machine learning
- [ ] Price elasticity analysis for dynamic pricing

### Phase 3: Deployment
- [ ] Deploy dashboard to Power BI Service with row-level security
- [ ] Create REST API for programmatic access
- [ ] Build Streamlit/Dash web application for broader accessibility

## 📧 Contact

**Ayush Paderiya**  
Data Analyst | Aspiring ML Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/ayush-paderiya-94b2a3131)
[![Email](https://img.shields.io/badge/Email-paderiyaayush%40gmail.com-red)](mailto:paderiyaayush@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/AyushPaderiya)

---

### 📝 License
This project is available under the MIT License. Feel free to use it for learning and portfolio purposes.

### ⭐ Acknowledgments
If you find this project helpful, please consider giving it a star!

---

*This project showcases end-to-end data analytics capabilities from data engineering to business intelligence, demonstrating proficiency in Python, SQL, statistical analysis, and visualization tools.*
