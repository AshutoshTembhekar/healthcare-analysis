import pandas as pd
import numpy as np

REQUIRED_COLUMNS = [
    "Name", "Age", "Gender", "Blood Type", "Medical Condition",
    "Date of Admission", "Doctor", "Hospital", "Insurance Provider",
    "Billing Amount", "Room Number", "Admission Type", "Discharge Date",
    "Medication", "Test Results"
]

def validate_healthcare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validates structural integrity, enforces types, filters corrupted records,
    and returns a clean, audit-compliant DataFrame.
    """
    missing_cols = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Schema violation: Missing required columns: {missing_cols}")

    df = df.copy()

    # Temporal conversions
    df["Date of Admission"] = pd.to_datetime(df["Date of Admission"], errors="coerce")
    df["Discharge Date"] = pd.to_datetime(df["Discharge Date"], errors="coerce")

    # Filter out null timestamps
    valid_dates = df["Date of Admission"].notna() & df["Discharge Date"].notna()
    # Business rule: Discharge date cannot precede admission date
    valid_temporal = df["Discharge Date"] >= df["Date of Admission"]
    # Domain rules: Non-negative billing, valid biological age
    valid_billing = df["Billing Amount"] >= 0
    valid_age = (df["Age"] >= 0) & (df["Age"] <= 125)

    clean_mask = valid_dates & valid_temporal & valid_billing & valid_age
    dropped_count = len(df) - clean_mask.sum()

    if dropped_count > 0:
        print(f"[DATA QUALITY ALERT] Filtered out {dropped_count} anomalous/corrupted records.")

    return df[clean_mask].reset_index(drop=True)