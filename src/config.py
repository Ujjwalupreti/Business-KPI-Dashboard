"""
Configuration, design tokens, and style constants for Excel KPI Dashboard.
"""
import os
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# Paths
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SRC_DIR)

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "customer_churn_cleaned.csv")
ROOT_DATA_PATH = os.path.join(PROJECT_ROOT, "customer_churn_cleaned.csv")
EXCEL_OUTPUT_PATH = os.path.join(PROJECT_ROOT, "customer_churn_kpi_dashboard.xlsx")

# Color Palette (Hex)
DARK_NAVY = "1B365D"
ACCENT_BLUE = "2B6CB0"
ALERT_RED = "D9381E"
SUCCESS_GREEN = "2E7D32"
LIGHT_GRAY_FILL = "F4F6F9"
BORDER_GRAY = "D1D5DB"
WHITE = "FFFFFF"

# Fonts
FONT_TITLE = Font(name="Segoe UI", size=16, bold=True, color=WHITE)
FONT_SUBTITLE = Font(name="Segoe UI", size=10, italic=True, color="E2E8F0")
FONT_CARD_NUM = Font(name="Segoe UI", size=18, bold=True, color=DARK_NAVY)
FONT_CARD_NUM_ALERT = Font(name="Segoe UI", size=18, bold=True, color=ALERT_RED)
FONT_CARD_NUM_GREEN = Font(name="Segoe UI", size=18, bold=True, color=SUCCESS_GREEN)
FONT_CARD_LABEL = Font(name="Segoe UI", size=9, bold=True, color="4A5568")
FONT_SEC_HDR = Font(name="Segoe UI", size=11, bold=True, color=DARK_NAVY)
FONT_BOLD = Font(name="Segoe UI", size=10, bold=True)
FONT_REGULAR = Font(name="Segoe UI", size=9)
FONT_CALLOUT = Font(name="Segoe UI", size=9, italic=True, color="2D3748")

# Fills
FILL_HEADER = PatternFill(start_color=DARK_NAVY, end_color=DARK_NAVY, fill_type="solid")
FILL_CARD_HEADER = PatternFill(start_color="EDF2F7", end_color="EDF2F7", fill_type="solid")
FILL_ALERT_LIGHT = PatternFill(start_color="FED7D7", end_color="FED7D7", fill_type="solid")
FILL_GREEN_LIGHT = PatternFill(start_color="C6F6D5", end_color="C6F6D5", fill_type="solid")
FILL_TBL_HEADER = PatternFill(start_color=ACCENT_BLUE, end_color=ACCENT_BLUE, fill_type="solid")

# Borders
THIN_SIDE = Side(border_style="thin", color=BORDER_GRAY)
CARD_BORDER = Border(top=THIN_SIDE, left=THIN_SIDE, right=THIN_SIDE, bottom=THIN_SIDE)
