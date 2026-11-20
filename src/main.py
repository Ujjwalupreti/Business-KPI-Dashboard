"""
Main orchestrator script to build the Excel Business KPI Dashboard.
"""
import openpyxl
from .config import EXCEL_OUTPUT_PATH
from .data_loader import load_and_prepare_data
from .excel_builder import build_dashboard_sheet, build_data_sheet

def generate_dashboard():
    print("=" * 80)
    print("BUILDING MODULAR EXCEL KPI DASHBOARD")
    print("=" * 80)

    # 1. Load & prepare data
    df = load_and_prepare_data()
    print(f"Data loaded successfully: {len(df)} records with engineered cohorts.")

    # 2. Initialize workbook
    wb = openpyxl.Workbook()

    # 3. Build Sheet 1: Executive KPI Dashboard
    ws_dash = wb.active
    ws_dash.title = "Executive_KPI_Dashboard"
    build_dashboard_sheet(ws_dash, df)
    print("Sheet 1 ('Executive_KPI_Dashboard') created with KPI cards and action roster.")

    # 4. Build Sheet 2: Customer Data
    ws_data = wb.create_sheet(title="Customer_Data")
    build_data_sheet(ws_data, df)
    print("Sheet 2 ('Customer_Data') populated with validated records and helper fields.")

    # 5. Save workbook
    wb.save(EXCEL_OUTPUT_PATH)
    print(f"\n[Success] Workbook successfully saved to:\n  {EXCEL_OUTPUT_PATH}")
    print("=" * 80)

if __name__ == "__main__":
    generate_dashboard()

