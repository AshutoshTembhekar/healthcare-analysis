import os
import pandas as pd
from src.schemas import validate_healthcare_dataframe
from src.anonymizer import hash_patient_id

def run_pipeline(raw_csv_path: str, output_parquet_path: str) -> pd.DataFrame:
    """
    Executes raw data loading, schema validation, PII pseudonymization,
    operational metric calculation, and optimized Parquet serialization.
    """
    if not os.path.exists(raw_csv_path):
        raise FileNotFoundError(f"Raw data file not found at: {raw_csv_path}")

    print(f"Loading raw dataset from {raw_csv_path}...")
    raw_df = pd.read_csv(raw_csv_path)

    print("Executing strict schema and clinical domain assertions...")
    clean_df = validate_healthcare_dataframe(raw_df)

    print("Hashing patient identifiers (PHI sanitization)...")
    clean_df["Patient_ID"] = clean_df["Name"].apply(hash_patient_id)
    clean_df = clean_df.drop(columns=["Name"])

    print("Engineering operational healthcare metrics...")
    clean_df["Length_of_Stay_Days"] = (clean_df["Discharge Date"] - clean_df["Date of Admission"]).dt.days
    clean_df["Daily_Billing_Rate"] = (clean_df["Billing Amount"] / clean_df["Length_of_Stay_Days"].replace(0, 1)).round(2)

    os.makedirs(os.path.dirname(output_parquet_path), exist_ok=True)
    clean_df.to_parquet(output_parquet_path, index=False)
    print(f"Sanitized dataset successfully serialized to {output_parquet_path}")

    return clean_df

if __name__ == "__main__":
    raw_path = "data/raw/healthcare_dataset.csv"
    processed_path = "data/processed/healthcare_clean.parquet"
    run_pipeline(raw_path, processed_path)