"""
Create a professional, styled Excel Business KPI Dashboard using openpyxl.
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import pandas as pd
import os

KPI_DIR = r"c:\Users\Hp\Downloads\EDAI\KPI"
csv_path = os.path.join(KPI_DIR, "customer_churn_cleaned.csv")
excel_path = os.path.join(KPI_DIR, "customer_churn_kpi_dashboard.xlsx")

df = pd.read_csv(csv_path)

# Helper bucket functions
def get_tenure_bucket(m):
    if m <= 6:
        return "0–6m"
    elif m <= 12:
        return "7–12m"
    elif m <= 24:
        return "13–24m"
    else:
        return "25m+"

def get_priority_tier(row):
    if row["contract_type_standardized"] == "Monthly" and row["support_tickets"] >= 3:
        return "Tier 1: Emergency Outreach (100% Churn)"
    elif row["tenure_months"] <= 6 and row["support_tickets"] >= 2:
        return "Tier 2: Proactive Onboarding"
    else:
        return "Tier 3: Low Risk / Retained"

df["tenure_bucket"] = df["tenure_months"].apply(get_tenure_bucket)
df["priority_tier"] = df.apply(get_priority_tier, axis=1)
df["revenue_at_risk"] = df.apply(lambda r: r["monthly_charge"] if r["churned"] == "Yes" else 0.0, axis=1)

wb = openpyxl.Workbook()

# Setup Sheet 1: Dashboard
ws_dash = wb.active
ws_dash.title = "Executive_KPI_Dashboard"
ws_dash.views.sheetView[0].showGridLines = True

# Setup Sheet 2: Cleaned Data
ws_data = wb.create_sheet(title="Customer_Data")
ws_data.views.sheetView[0].showGridLines = True

# Palettes & Styles
DARK_NAVY = "1B365D"
ACCENT_BLUE = "2B6CB0"
ALERT_RED = "D9381E"
SUCCESS_GREEN = "2E7D32"
LIGHT_GRAY_FILL = "F4F6F9"
BORDER_GRAY = "D1D5DB"
WHITE = "FFFFFF"

font_title = Font(name="Segoe UI", size=16, bold=True, color=WHITE)
font_subtitle = Font(name="Segoe UI", size=10, italic=True, color="E2E8F0")
font_card_num = Font(name="Segoe UI", size=18, bold=True, color=DARK_NAVY)
font_card_num_alert = Font(name="Segoe UI", size=18, bold=True, color=ALERT_RED)
font_card_num_green = Font(name="Segoe UI", size=18, bold=True, color=SUCCESS_GREEN)
font_card_label = Font(name="Segoe UI", size=9, bold=True, color="4A5568")
font_sec_hdr = Font(name="Segoe UI", size=11, bold=True, color=DARK_NAVY)
font_bold = Font(name="Segoe UI", size=10, bold=True)
font_regular = Font(name="Segoe UI", size=9)
font_callout = Font(name="Segoe UI", size=9, italic=True, color="2D3748")

fill_header = PatternFill(start_color=DARK_NAVY, end_color=DARK_NAVY, fill_type="solid")
fill_card_header = PatternFill(start_color="EDF2F7", end_color="EDF2F7", fill_type="solid")
fill_alert_light = PatternFill(start_color="FED7D7", end_color="FED7D7", fill_type="solid")
fill_green_light = PatternFill(start_color="C6F6D5", end_color="C6F6D5", fill_type="solid")
fill_tbl_header = PatternFill(start_color="2B6CB0", end_color="2B6CB0", fill_type="solid")
fill_zebra = PatternFill(start_color="F7FAFC", end_color="F7FAFC", fill_type="solid")

thin_border_side = Side(border_style="thin", color=BORDER_GRAY)
card_border = Border(top=thin_border_side, left=thin_border_side, right=thin_border_side, bottom=thin_border_side)
thick_top_border = Border(top=Side(border_style="medium", color=DARK_NAVY))

# Write Dashboard Header Banner (Rows 1-2)
ws_dash.merge_cells("B1:K1")
ws_dash["B1"] = "📊 SUBSCRIPTION CHURN & RETENTION KPI EXECUTIVE DASHBOARD"
ws_dash["B1"].font = font_title
ws_dash["B1"].fill = fill_header
ws_dash["B1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)

ws_dash.merge_cells("B2:K2")
ws_dash["B2"] = "Decision Question: Which customer groups should the subscription team contact first to reduce avoidable churn? | Currency: INR (₹)"
ws_dash["B2"].font = font_subtitle
ws_dash["B2"].fill = fill_header
ws_dash["B2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)

ws_dash.row_dimensions[1].height = 28
ws_dash.row_dimensions[2].height = 18

# Row 3: Blank spacer
ws_dash.row_dimensions[3].height = 8

# KPI Cards (Rows 4-6)
cards = [
    {"col_start": "B", "col_end": "C", "label": "TOTAL CUSTOMERS", "val": 15, "fmt": "#,##0", "font": font_card_num, "fill": fill_card_header},
    {"col_start": "D", "col_end": "E", "label": "CHURN RATE (%)", "val": "=COUNTIF(Customer_Data!L2:L16,\"Yes\")/COUNTA(Customer_Data!A2:A16)", "fmt": "0.0%", "font": font_card_num_alert, "fill": fill_alert_light},
    {"col_start": "F", "col_end": "G", "label": "RETENTION RATE (%)", "val": "=COUNTIF(Customer_Data!L2:L16,\"No\")/COUNTA(Customer_Data!A2:A16)", "fmt": "0.0%", "font": font_card_num_green, "fill": fill_green_light},
    {"col_start": "H", "col_end": "I", "label": "MONTHLY REVENUE AT RISK", "val": "=SUMIF(Customer_Data!L2:L16,\"Yes\",Customer_Data!F2:F16)", "fmt": "₹#,##0.00", "font": font_card_num_alert, "fill": fill_alert_light},
    {"col_start": "J", "col_end": "K", "label": "AVG TENURE (CHURN vs RET)", "val": "7.0m vs 29.1m", "fmt": None, "font": font_card_num, "fill": fill_card_header}
]

for card in cards:
    cs, ce = card["col_start"], card["col_end"]
    # Header label
    ws_dash.merge_cells(f"{cs}4:{ce}4")
    cell_lbl = ws_dash[f"{cs}4"]
    cell_lbl.value = card["label"]
    cell_lbl.font = font_card_label
    cell_lbl.fill = card["fill"]
    cell_lbl.alignment = Alignment(horizontal="center", vertical="center")
    
    # Value
    ws_dash.merge_cells(f"{cs}5:{ce}6")
    cell_val = ws_dash[f"{cs}5"]
    cell_val.value = card["val"]
    cell_val.font = card["font"]
    if card["fmt"]:
        cell_val.number_format = card["fmt"]
    cell_val.alignment = Alignment(horizontal="center", vertical="center")
    
    # Border
    for r in range(4, 7):
        for col_char in [cs, ce]:
            ws_dash[f"{col_char}{r}"].border = card_border

ws_dash.row_dimensions[4].height = 16
ws_dash.row_dimensions[5].height = 18
ws_dash.row_dimensions[6].height = 18
ws_dash.row_dimensions[7].height = 10

# Section 1: Breakdown Tables & Visual Summaries (Rows 8 to 18)
# Table A: Churn Rate by Contract Type (Cols B to E)
ws_dash.merge_cells("B8:E8")
ws_dash["B8"] = "📈 CHURN RATE & REVENUE BY CONTRACT TYPE"
ws_dash["B8"].font = font_sec_hdr
ws_dash["B8"].alignment = Alignment(horizontal="left", vertical="center")

headers_ct = ["Contract Type", "Total Cust", "Churned", "Churn Rate (%)"]
for idx, h in enumerate(headers_ct):
    c = chr(ord("B") + idx)
    ws_dash[f"{c}9"] = h
    ws_dash[f"{c}9"].font = Font(name="Segoe UI", size=9, bold=True, color=WHITE)
    ws_dash[f"{c}9"].fill = fill_tbl_header
    ws_dash[f"{c}9"].alignment = Alignment(horizontal="center", vertical="center")

ct_data = [
    ("Monthly", 7, 7, 1.00),
    ("Annual", 4, 0, 0.00),
    ("Two-Year", 4, 0, 0.00),
    ("Overall Total", 15, 7, 0.467)
]

for r_idx, (ct, tc, ch, cr) in enumerate(ct_data, start=10):
    ws_dash[f"B{r_idx}"] = ct
    ws_dash[f"C{r_idx}"] = tc
    ws_dash[f"D{r_idx}"] = ch
    ws_dash[f"E{r_idx}"] = cr
    ws_dash[f"E{r_idx}"].number_format = "0.0%"
    
    is_total = (ct == "Overall Total")
    row_font = font_bold if is_total else font_regular
    for c in ["B", "C", "D", "E"]:
        ws_dash[f"{c}{r_idx}"].font = row_font
        ws_dash[f"{c}{r_idx}"].alignment = Alignment(horizontal="center" if c != "B" else "left", vertical="center")
        ws_dash[f"{c}{r_idx}"].border = card_border
        if is_total:
            ws_dash[f"{c}{r_idx}"].fill = fill_card_header

# Callout below Table A
ws_dash.merge_cells("B15:E16")
ws_dash["B15"] = "💡 Descriptive Finding: 100% of churned accounts (7/7) were on Monthly contracts. Monthly contracts lower exit barriers but do not inherently cause dissatisfaction."
ws_dash["B15"].font = font_callout
ws_dash["B15"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

# Table B: Revenue at Risk by Tenure Bucket (Cols G to K)
ws_dash.merge_cells("G8:K8")
ws_dash["G8"] = "⏱️ REVENUE AT RISK BY TENURE BUCKET"
ws_dash["G8"].font = font_sec_hdr
ws_dash["G8"].alignment = Alignment(horizontal="left", vertical="center")

headers_tb = ["Tenure Bucket", "Total Cust", "Churned Cust", "Churn Rate", "Revenue at Risk (₹)"]
for idx, h in enumerate(headers_tb):
    c = chr(ord("G") + idx)
    ws_dash[f"{c}9"] = h
    ws_dash[f"{c}9"].font = Font(name="Segoe UI", size=9, bold=True, color=WHITE)
    ws_dash[f"{c}9"].fill = fill_tbl_header
    ws_dash[f"{c}9"].alignment = Alignment(horizontal="center", vertical="center")

tb_data = [
    ("0–6m (Early Onboarding)", 4, 4, 1.00, 199.96),
    ("7–12m (Early Lifecycle)", 2, 2, 1.00, 129.98),
    ("13–24m (Mature)", 5, 1, 0.20, 79.99),
    ("25m+ (Long-Term Loyals)", 4, 0, 0.00, 0.00),
    ("Total Portfolio", 15, 7, 0.467, 409.93)
]

for r_idx, (tb, tc, ch, cr, rar) in enumerate(tb_data, start=10):
    ws_dash[f"G{r_idx}"] = tb
    ws_dash[f"H{r_idx}"] = tc
    ws_dash[f"I{r_idx}"] = ch
    ws_dash[f"J{r_idx}"] = cr
    ws_dash[f"J{r_idx}"].number_format = "0.0%"
    ws_dash[f"K{r_idx}"] = rar
    ws_dash[f"K{r_idx}"].number_format = "₹#,##0.00"
    
    is_total = ("Total" in tb)
    row_font = font_bold if is_total else font_regular
    for c in ["G", "H", "I", "J", "K"]:
        ws_dash[f"{c}{r_idx}"].font = row_font
        ws_dash[f"{c}{r_idx}"].alignment = Alignment(horizontal="center" if c not in ["G", "K"] else ("left" if c=="G" else "right"), vertical="center")
        ws_dash[f"{c}{r_idx}"].border = card_border
        if is_total:
            ws_dash[f"{c}{r_idx}"].fill = fill_card_header

# Callout below Table B
ws_dash.merge_cells("G15:K16")
ws_dash["G15"] = "💡 Descriptive Finding: 80.5% of total revenue at risk (₹329.94) is concentrated in subscribers with <=12 months tenure. Subscribers surviving past 24 months show 0% churn."
ws_dash["G15"].font = font_callout
ws_dash["G15"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

# Row 17: Spacer
ws_dash.row_dimensions[17].height = 10

# Section 2: Priority Outreach Action Table (Rows 18 to 28)
ws_dash.merge_cells("B18:K18")
ws_dash["B18"] = "🎯 ACTIONABLE SUBSCRIBER OUTREACH ROSTER (PRIORITIZED FOR SUBSCRIPTION TEAM)"
ws_dash["B18"].font = font_sec_hdr
ws_dash["B18"].alignment = Alignment(horizontal="left", vertical="center")

headers_roster = ["Customer ID", "Gender", "Age", "Tenure (Mos)", "Tier", "Monthly Fee (₹)", "Contract", "Tickets (90d)", "Churn Status", "Priority Outreach Tier"]
for idx, h in enumerate(headers_roster):
    c = chr(ord("B") + idx)
    ws_dash[f"{c}19"] = h
    ws_dash[f"{c}19"].font = Font(name="Segoe UI", size=9, bold=True, color=WHITE)
    ws_dash[f"{c}19"].fill = PatternFill(start_color=DARK_NAVY, end_color=DARK_NAVY, fill_type="solid")
    ws_dash[f"{c}19"].alignment = Alignment(horizontal="center", vertical="center")

# Sort df by priority and churned
df_sorted = df.sort_values(by=["is_churned", "support_tickets"], ascending=[False, False])

for r_idx, (_, row) in enumerate(df_sorted.iterrows(), start=20):
    ws_dash[f"B{r_idx}"] = row["customer_id"]
    ws_dash[f"C{r_idx}"] = row["gender"]
    ws_dash[f"D{r_idx}"] = row["age"]
    ws_dash[f"E{r_idx}"] = row["tenure_months"]
    ws_dash[f"F{r_idx}"] = row["subscription_type"]
    ws_dash[f"G{r_idx}"] = row["monthly_charge"]
    ws_dash[f"G{r_idx}"].number_format = "₹#,##0.00"
    ws_dash[f"H{r_idx}"] = row["contract_type_standardized"]
    ws_dash[f"I{r_idx}"] = row["support_tickets"]
    ws_dash[f"J{r_idx}"] = row["churned"]
    ws_dash[f"K{r_idx}"] = row["priority_tier"]
    
    # Conditional formatting color
    is_ch = (row["churned"] == "Yes")
    tier_fill = fill_alert_light if is_ch else fill_green_light
    
    for c in ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]:
        cell = ws_dash[f"{c}{r_idx}"]
        cell.font = font_regular
        cell.alignment = Alignment(horizontal="center" if c not in ["F", "H", "K"] else ("left" if c=="K" else "center"), vertical="center")
        cell.border = card_border
        if c == "J":
            cell.font = Font(name="Segoe UI", size=9, bold=True, color=ALERT_RED if is_ch else SUCCESS_GREEN)
            cell.fill = tier_fill
        elif c == "K":
            cell.font = Font(name="Segoe UI", size=8, bold=True)
            cell.fill = tier_fill

# Write Cleaned Data into Sheet 2
data_headers = list(df.columns)
for col_idx, col_name in enumerate(data_headers, start=1):
    cell = ws_data.cell(row=1, column=col_idx, value=col_name)
    cell.font = Font(name="Segoe UI", size=10, bold=True, color=WHITE)
    cell.fill = fill_tbl_header
    cell.alignment = Alignment(horizontal="center", vertical="center")

for row_idx, row in df.iterrows():
    for col_idx, col_name in enumerate(data_headers, start=1):
        cell = ws_data.cell(row=row_idx+2, column=col_idx, value=row[col_name])
        cell.font = font_regular
        cell.border = card_border
        if "charge" in col_name or "revenue" in col_name:
            cell.number_format = "₹#,##0.00"

# Adjust column widths
for sheet in [ws_dash, ws_data]:
    for col in sheet.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        sheet.column_dimensions[col_letter].width = max(max_len + 3, 11)

ws_dash.column_dimensions["A"].width = 3
ws_dash.column_dimensions["B"].width = 15
ws_dash.column_dimensions["C"].width = 12
ws_dash.column_dimensions["D"].width = 12
ws_dash.column_dimensions["E"].width = 16
ws_dash.column_dimensions["F"].width = 14
ws_dash.column_dimensions["G"].width = 16
ws_dash.column_dimensions["H"].width = 14
ws_dash.column_dimensions["I"].width = 14
ws_dash.column_dimensions["J"].width = 14
ws_dash.column_dimensions["K"].width = 32

wb.save(excel_path)
print(f"Excel Dashboard successfully created at: {excel_path}")

