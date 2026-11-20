"""
Excel styling utility helpers for openpyxl worksheets.
"""
from openpyxl.utils import get_column_letter
from .config import CARD_BORDER

def auto_fit_columns(worksheet, min_width: int = 11, padding: int = 3):
    """Dynamically adjusts column widths based on maximum content length."""
    for col in worksheet.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        worksheet.column_dimensions[col_letter].width = max(max_len + padding, min_width)

def apply_card_borders(worksheet, row_start: int, row_end: int, col_start: str, col_end: str):
    """Applies clean thin border box around a cell range."""
    col_idx_start = ord(col_start.upper())
    col_idx_end = ord(col_end.upper())
    for r in range(row_start, row_end + 1):
        for c_idx in range(col_idx_start, col_idx_end + 1):
            col_char = chr(c_idx)
            worksheet[f"{col_char}{r}"].border = CARD_BORDER

