# 📊 Business KPI Dashboard: Customer Churn & Retention

[![Track: Data Analytics](https://img.shields.io/badge/Track-Data_Analytics-blue.svg)](https://edvyro.in)
[![Role: Senior BI Developer](https://img.shields.io/badge/Role-Senior_BI_Developer-darkblue.svg)]()
[![Architecture: Modular Components](https://img.shields.io/badge/Architecture-Modular_Components-brightgreen.svg)]()
[![Status: Production Ready](https://img.shields.io/badge/Status-Complete-brightgreen.svg)]()

> **Decision Question:** *Which customer groups should a fictional subscription team contact first to reduce avoidable churn?*

---

## 📁 Modular Project Architecture

```text
KPI/
├── index.html                             # Clean semantic HTML container
├── assets/
│   ├── css/
│   │   ├── variables.css                  # Design tokens, colorblind-safe palettes, typography
│   │   ├── layout.css                     # Header banner, responsive grid system, footer
│   │   ├── components.css                 # Slicer bar, KPI cards, chart boxes, action roster
│   │   └── style.css                      # Master CSS bundle
│   └── js/
│       ├── data.js                        # Subscriber dataset repository
│       ├── state.js                       # Reactive state manager for active slicers
│       ├── components/
│       │   ├── headerBanner.js            # Header banner & decision question badge component
│       │   ├── filterBar.js               # Interactive slicers (Contract, Tenure, Payment)
│       │   ├── kpiCards.js                # Top 5 KPI executive summary cards component
│       │   ├── charts.js                  # 4 dynamic Chart.js visualizations component
│       │   └── actionTable.js             # Prioritized customer outreach table component
│       └── app.js                         # Application bootstrap & lifecycle orchestrator
├── data/
│   └── customer_churn_cleaned.csv         # Validated production dataset
├── src/
│   ├── __init__.py
│   ├── config.py                          # Excel palette tokens, fonts, openpyxl styles
│   ├── data_loader.py                     # Cohort feature engineering (tenure buckets, tiers)
│   ├── excel_styler.py                    # Reusable openpyxl formatting & width helpers
│   ├── excel_builder.py                   # Worksheet generator for dashboard and data sheets
│   └── main.py                            # Python builder orchestrator
├── run_builder.py                         # Root launcher for Python Excel builder
├── customer_churn_kpi_dashboard.xlsx      # Pre-built executive Excel dashboard workbook
├── BUSINESS_KPI_DASHBOARD_GUIDE.md        # Comprehensive implementation guide (DAX, Tableau, Excel)
├── requirements.txt                       # Python dependencies
└── README.md                              # Project documentation
```

---

## 🚀 Quick Launch

### 1. Interactive Web Dashboard
Open `index.html` in your browser.  
Features:
- **Modular Component Architecture:** Independent UI components for slicers, cards, charts, and tables.
- **Reactive State Management:** Changes to Contract, Tenure, or Payment Method filters re-calculate KPI cards, update charts, and re-filter the outreach table in real-time.

### 2. Pre-Built Executive Excel Dashboard
Open `customer_churn_kpi_dashboard.xlsx` in Microsoft Excel.  
Features:
- **Sheet 1 (`Executive_KPI_Dashboard`):** KPI cards with live Excel formulas (`COUNTIF`, `SUMIF`), contract breakdown tables, tenure revenue risk cohorts, and formatted priority customer roster.
- **Sheet 2 (`Customer_Data`):** Complete validated customer records with engineered cohort helper fields.

### 3. Rebuild Excel Workbook with Modular Python
```bash
python run_builder.py
```
Or:
```bash
python -m src.main
```
