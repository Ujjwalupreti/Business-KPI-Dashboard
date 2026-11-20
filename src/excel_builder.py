"""
Worksheet builder for Executive KPI Dashboard and Customer Data sheets.
"""
from openpyxl.styles import Alignment, Font, PatternFill
from .config import (
    FONT_TITLE, FONT_SUBTITLE, FONT_CARD_LABEL, FONT_CARD_NUM,
    FONT_CARD_NUM_ALERT, FONT_CARD_NUM_GREEN, FONT_SEC_HDR,
    FONT_BOLD, FONT_REGULAR, FONT_CALLOUT, FILL_HEADER,
    FILL_CARD_HEADER, FILL_ALERT_LIGHT, FILL_GREEN_LIGHT,
    FILL_TBL_HEADER, CARD_BORDER, DARK_NAVY, WHITE, ALERT_RED, SUCCESS_GREEN
)
from .excel_styler import auto_fit_columns, apply_card_borders

def build_dashboard_sheet(ws, df):
    """Builds the Executive KPI Dashboard single-page view."""
    ws.views.sheetView[0].showGridLines = True

    # 1. Header Banner
    ws.merge_cells("B1:K1")
    ws["B1"] = "📊 SUBSCRIPTION CHURN & RETENTION KPI EXECUTIVE DASHBOARD"
    ws["B1"].font = FONT_TITLE
    ws["B1"].fill = FILL_HEADER
    ws["B1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)

    ws.merge_cells("B2:K2")
    ws["B2"] = "Decision Question: Which customer groups should the subscription team contact first to reduce avoidable churn? | Currency: INR (₹)"
    ws["B2"].font = FONT_SUBTITLE
    ws["B2"].fill = FILL_HEADER
    ws["B2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)

    ws.row_dimensions[1].height = 28
    ws.row_dimensions[2].height = 18
    ws.row_dimensions[3].height = 8

    # 2. Top KPI Cards Banner (Rows 4 to 6)
    cards = [
        {"cs": "B", "ce": "C", "label": "TOTAL CUSTOMERS", "val": 15, "fmt": "#,##0", "font": FONT_CARD_NUM, "fill": FILL_CARD_HEADER},
        {"cs": "D", "ce": "E", "label": "CHURN RATE (%)", "val": '=COUNTIF(Customer_Data!L2:L16,"Yes")/COUNTA(Customer_Data!A2:A16)', "fmt": "0.0%", "font": FONT_CARD_NUM_ALERT, "fill": FILL_ALERT_LIGHT},
        {"cs": "F", "ce": "G", "label": "RETENTION RATE (%)", "val": '=COUNTIF(Customer_Data!L2:L16,"No")/COUNTA(Customer_Data!A2:A16)', "fmt": "0.0%", "font": FONT_CARD_NUM_GREEN, "fill": FILL_GREEN_LIGHT},
        {"cs": "H", "ce": "I", "label": "MONTHLY REVENUE AT RISK", "val": '=SUMIF(Customer_Data!L2:L16,"Yes",Customer_Data!F2:F16)', "fmt": "₹#,##0.00", "font": FONT_CARD_NUM_ALERT, "fill": FILL_ALERT_LIGHT},
        {"cs": "J", "ce": "K", "label": "AVG TENURE (CHURN vs RET)", "val": "7.0m vs 29.1m", "fmt": None, "font": FONT_CARD_NUM, "fill": FILL_CARD_HEADER}
    ]

    for card in cards:
        cs, ce = card["cs"], card["ce"]
        ws.merge_cells(f"{cs}4:{ce}4")
        lbl_cell = ws[f"{cs}4"]
        lbl_cell.value = card["label"]
        lbl_cell.font = FONT_CARD_LABEL
        lbl_cell.fill = card["fill"]
        lbl_cell.alignment = Alignment(horizontal="center", vertical="center")

        ws.merge_cells(f"{cs}5:{ce}6")
        val_cell = ws[f"{cs}5"]
        val_cell.value = card["val"]
        val_cell.font = card["font"]
        if card["fmt"]:
            val_cell.number_format = card["fmt"]
        val_cell.alignment = Alignment(horizontal="center", vertical="center")

        apply_card_borders(ws, 4, 6, cs, ce)

    ws.row_dimensions[4].height = 16
    ws.row_dimensions[5].height = 18
    ws.row_dimensions[6].height = 18
    ws.row_dimensions[7].height = 10

    # 3. Breakdown Tables (Rows 8 to 16)
    # Table A: Churn by Contract Type (Cols B to E)
    ws.merge_cells("B8:E8")
    ws["B8"] = "📈 CHURN RATE & REVENUE BY CONTRACT TYPE"
    ws["B8"].font = FONT_SEC_HDR
    ws["B8"].alignment = Alignment(horizontal="left", vertical="center")

    headers_ct = ["Contract Type", "Total Cust", "Churned", "Churn Rate (%)"]
    for idx, h in enumerate(headers_ct):
        c = chr(ord("B") + idx)
        ws[f"{c}9"] = h
        ws[f"{c}9"].font = Font(name="Segoe UI", size=9, bold=True, color=WHITE)
        ws[f"{c}9"].fill = FILL_TBL_HEADER
        ws[f"{c}9"].alignment = Alignment(horizontal="center", vertical="center")

    ct_data = [
        ("Monthly", 7, 7, 1.00),
        ("Annual", 4, 0, 0.00),
        ("Two-Year", 4, 0, 0.00),
        ("Overall Total", 15, 7, 0.467)
    ]

    for r_idx, (ct, tc, ch, cr) in enumerate(ct_data, start=10):
        ws[f"B{r_idx}"] = ct
        ws[f"C{r_idx}"] = tc
        ws[f"D{r_idx}"] = ch
        ws[f"E{r_idx}"] = cr
        ws[f"E{r_idx}"].number_format = "0.0%"
        is_total = (ct == "Overall Total")
        row_font = FONT_BOLD if is_total else FONT_REGULAR

        for c in ["B", "C", "D", "E"]:
            ws[f"{c}{r_idx}"].font = row_font
            ws[f"{c}{r_idx}"].alignment = Alignment(horizontal="center" if c != "B" else "left", vertical="center")
            ws[f"{c}{r_idx}"].border = CARD_BORDER
            if is_total:
                ws[f"{c}{r_idx}"].fill = FILL_CARD_HEADER

    ws.merge_cells("B15:E16")
    ws["B15"] = "💡 Descriptive Finding: 100% of churned accounts (7/7) were on Monthly contracts. Monthly contracts lower exit barriers but do not inherently cause dissatisfaction."
    ws["B15"].font = FONT_CALLOUT
    ws["B15"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

    # Table B: Revenue at Risk by Tenure Bucket (Cols G to K)
    ws.merge_cells("G8:K8")
    ws["G8"] = "⏱️ REVENUE AT RISK BY TENURE BUCKET"
    ws["G8"].font = FONT_SEC_HDR
    ws["G8"].alignment = Alignment(horizontal="left", vertical="center")

    headers_tb = ["Tenure Bucket", "Total Cust", "Churned Cust", "Churn Rate", "Revenue at Risk (₹)"]
    for idx, h in enumerate(headers_tb):
        c = chr(ord("G") + idx)
        ws[f"{c}9"] = h
        ws[f"{c}9"].font = Font(name="Segoe UI", size=9, bold=True, color=WHITE)
        ws[f"{c}9"].fill = FILL_TBL_HEADER
        ws[f"{c}9"].alignment = Alignment(horizontal="center", vertical="center")

    tb_data = [
        ("0–6m (Early Onboarding)", 4, 4, 1.00, 199.96),
        ("7–12m (Early Lifecycle)", 2, 2, 1.00, 129.98),
        ("13–24m (Mature)", 5, 1, 0.20, 79.99),
        ("25m+ (Long-Term Loyals)", 4, 0, 0.00, 0.00),
        ("Total Portfolio", 15, 7, 0.467, 409.93)
    ]

    for r_idx, (tb, tc, ch, cr, rar) in enumerate(tb_data, start=10):
        ws[f"G{r_idx}"] = tb
        ws[f"H{r_idx}"] = tc
        ws[f"I{r_idx}"] = ch
        ws[f"J{r_idx}"] = cr
        ws[f"J{r_idx}"].number_format = "0.0%"
        ws[f"K{r_idx}"] = rar
        ws[f"K{r_idx}"].number_format = "₹#,##0.00"
        is_total = ("Total" in tb)
        row_font = FONT_BOLD if is_total else FONT_REGULAR

        for c in ["G", "H", "I", "J", "K"]:
            ws[f"{c}{r_idx}"].font = row_font
            ws[f"{c}{r_idx}"].alignment = Alignment(horizontal="center" if c not in ["G", "K"] else ("left" if c=="G" else "right"), vertical="center")
            ws[f"{c}{r_idx}"].border = CARD_BORDER
            if is_total:
                ws[f"{c}{r_idx}"].fill = FILL_CARD_HEADER

    ws.merge_cells("G15:K16")
    ws["G15"] = "💡 Descriptive Finding: 80.5% of total revenue at risk (₹329.94) is concentrated in subscribers with <=12 months tenure. Subscribers surviving past 24 months show 0% churn."
    ws["G15"].font = FONT_CALLOUT
    ws["G15"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

    ws.row_dimensions[17].height = 10

    # 4. Actionable Priority Customer Roster (Rows 18 to 35)
    ws.merge_cells("B18:K18")
    ws["B18"] = "🎯 ACTIONABLE SUBSCRIBER OUTREACH ROSTER (PRIORITIZED FOR SUBSCRIPTION TEAM)"
    ws["B18"].font = FONT_SEC_HDR
    ws["B18"].alignment = Alignment(horizontal="left", vertical="center")

    headers_roster = ["Customer ID", "Gender", "Age", "Tenure (Mos)", "Tier", "Monthly Fee (₹)", "Contract", "Tickets (90d)", "Churn Status", "Priority Outreach Tier"]
    for idx, h in enumerate(headers_roster):
        c = chr(ord("B") + idx)
        ws[f"{c}19"] = h
        ws[f"{c}19"].font = Font(name="Segoe UI", size=9, bold=True, color=WHITE)
        ws[f"{c}19"].fill = PatternFill(start_color=DARK_NAVY, end_color=DARK_NAVY, fill_type="solid")
        ws[f"{c}19"].alignment = Alignment(horizontal="center", vertical="center")

    df_sorted = df.sort_values(by=["is_churned", "support_tickets"], ascending=[False, False])
    for r_idx, (_, row) in enumerate(df_sorted.iterrows(), start=20):
        ws[f"B{r_idx}"] = row["customer_id"]
        ws[f"C{r_idx}"] = row["gender"]
        ws[f"D{r_idx}"] = row["age"]
        ws[f"E{r_idx}"] = row["tenure_months"]
        ws[f"F{r_idx}"] = row["subscription_type"]
        ws[f"G{r_idx}"] = row["monthly_charge"]
        ws[f"G{r_idx}"].number_format = "₹#,##0.00"
        ws[f"H{r_idx}"] = row["contract_type_standardized"]
        ws[f"I{r_idx}"] = row["support_tickets"]
        ws[f"J{r_idx}"] = row["churned"]
        ws[f"K{r_idx}"] = row["priority_tier"]

        is_ch = (row["churned"] == "Yes")
        tier_fill = FILL_ALERT_LIGHT if is_ch else FILL_GREEN_LIGHT

        for c in ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]:
            cell = ws[f"{c}{r_idx}"]
            cell.font = FONT_REGULAR
            cell.alignment = Alignment(horizontal="center" if c not in ["F", "H", "K"] else ("left" if c=="K" else "center"), vertical="center")
            cell.border = CARD_BORDER
            if c == "J":
                cell.font = Font(name="Segoe UI", size=9, bold=True, color=ALERT_RED if is_ch else SUCCESS_GREEN)
                cell.fill = tier_fill
            elif c == "K":
                cell.font = Font(name="Segoe UI", size=8, bold=True)
                cell.fill = tier_fill

    # Set column widths
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 15
    ws.column_dimensions["C"].width = 12
    ws.column_dimensions["D"].width = 12
    ws.column_dimensions["E"].width = 16
    ws.column_dimensions["F"].width = 14
    ws.column_dimensions["G"].width = 16
    ws.column_dimensions["H"].width = 14
    ws.column_dimensions["I"].width = 14
    ws.column_dimensions["J"].width = 14
    ws.column_dimensions["K"].width = 32

def build_data_sheet(ws, df):
    """Populates the raw customer records with helper columns."""
    ws.views.sheetView[0].showGridLines = True
    cols = list(df.columns)

    for c_idx, col_name in enumerate(cols, start=1):
        cell = ws.cell(row=1, column=c_idx, value=col_name)
        cell.font = Font(name="Segoe UI", size=10, bold=True, color=WHITE)
        cell.fill = FILL_TBL_HEADER
        cell.alignment = Alignment(horizontal="center", vertical="center")

    for r_idx, row in df.iterrows():
        for c_idx, col_name in enumerate(cols, start=1):
            cell = ws.cell(row=r_idx + 2, column=c_idx, value=row[col_name])
            cell.font = FONT_REGULAR
            cell.border = CARD_BORDER
            if "charge" in col_name or "revenue" in col_name:
                cell.number_format = "₹#,##0.00"

    auto_fit_columns(ws)

