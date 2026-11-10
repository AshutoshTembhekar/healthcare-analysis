import pytest
import pandas as pd
from src.schemas import validate_healthcare_dataframe

@pytest.fixture
def valid_record():
    return pd.DataFrame([{
        "Name": "Leslie Terry",
        "Age": 62,
        "Gender": "Male",
        "Blood Type": "A+",
        "Medical Condition": "Cancer",
        "Date of Admission": "2024-01-10",
        "Doctor": "Dr. Smith",
        "Hospital": "General Hospital",
        "Insurance Provider": "Aetna",
        "Billing Amount": 12450.50,
        "Room Number": 204,
        "Admission Type": "Urgent",
        "Discharge Date": "2024-01-18",
        "Medication": "Lipitor",
        "Test Results": "Normal"
    }])

def test_valid_data_passes(valid_record):
    df_clean = validate_healthcare_dataframe(valid_record)
    assert len(df_clean) == 1

def test_missing_required_column_fails(valid_record):
    bad_df = valid_record.drop(columns=["Billing Amount"])
    with pytest.raises(ValueError, match="Schema violation"):
        validate_healthcare_dataframe(bad_df)

def test_negative_billing_filtered(valid_record):
    bad_df = valid_record.copy()
    bad_df["Billing Amount"] = -500.00
    df_clean = validate_healthcare_dataframe(bad_df)
    assert len(df_clean) == 0

def test_discharge_before_admission_filtered(valid_record):
    bad_df = valid_record.copy()
    bad_df["Date of Admission"] = "2024-01-20"
    bad_df["Discharge Date"] = "2024-01-10"
    df_clean = validate_healthcare_dataframe(bad_df)
    assert len(df_clean) == 0

def test_impossible_age_filtered(valid_record):
    bad_df = valid_record.copy()
    bad_df["Age"] = 150
    df_clean = validate_healthcare_dataframe(bad_df)
    assert len(df_clean) == 0