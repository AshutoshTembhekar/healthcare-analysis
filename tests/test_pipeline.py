import pytest
import pandas as pd
from src.pipeline import run_pipeline

def test_pipeline_execution(tmp_path):
    # Create a small, compliant raw mock CSV
    mock_data = pd.DataFrame([{
        "Name": "John Doe",
        "Age": 45,
        "Gender": "Male",
        "Blood Type": "B+",
        "Medical Condition": "Asthma",
        "Date of Admission": "2024-02-01",
        "Doctor": "Dr. House",
        "Hospital": "Mercy Clinic",
        "Insurance Provider": "Cigna",
        "Billing Amount": 5000.00,
        "Room Number": 101,
        "Admission Type": "Elective",
        "Discharge Date": "2024-02-05",
        "Medication": "Albuterol",
        "Test Results": "Normal"
    }])
    
    raw_csv = tmp_path / "mock_raw.csv"
    output_parquet = tmp_path / "mock_clean.parquet"
    mock_data.to_csv(raw_csv, index=False)

    # Run the pipeline
    df_out = run_pipeline(str(raw_csv), str(output_parquet))

    # Assertions on pipeline output
    assert "Name" not in df_out.columns
    assert "Patient_ID" in df_out.columns
    assert df_out["Patient_ID"].iloc[0].startswith("PT-")
    assert df_out["Length_of_Stay_Days"].iloc[0] == 4
    assert df_out["Daily_Billing_Rate"].iloc[0] == 1250.00
    assert output_parquet.exists()