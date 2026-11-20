"""
Data loading and cohort feature engineering module.
"""
import os
import pandas as pd
from .config import DATA_PATH, ROOT_DATA_PATH

def get_tenure_bucket(months: int) -> str:
    """Categorizes continuous tenure into standardized cohorts."""
    if months <= 6:
        return "0–6m"
    elif months <= 12:
        return "7–12m"
    elif months <= 24:
        return "13–24m"
    else:
        return "25m+"

def get_priority_tier(row: pd.Series) -> str:
    """Assigns triage priority tiers based on contract commitment and friction signals."""
    if row["contract_type_standardized"] == "Monthly" and row["support_tickets"] >= 3:
        return "Tier 1: Emergency Outreach (100% Churn)"
    elif row["tenure_months"] <= 6 and row["support_tickets"] >= 2:
        return "Tier 2: Proactive Onboarding"
    else:
        return "Tier 3: Low Risk / Retained"

def load_and_prepare_data() -> pd.DataFrame:
    """Loads cleaned dataset and applies analytical helper fields."""
    target_path = DATA_PATH if os.path.exists(DATA_PATH) else ROOT_DATA_PATH
    if not os.path.exists(target_path):
        raise FileNotFoundError(f"Data file not found at: {target_path}")

    df = pd.read_csv(target_path)
    df["tenure_bucket"] = df["tenure_months"].apply(get_tenure_bucket)
    df["priority_tier"] = df.apply(get_priority_tier, axis=1)
    df["revenue_at_risk"] = df.apply(
        lambda r: r["monthly_charge"] if r["churned"] == "Yes" else 0.0, axis=1
    )
    return df

