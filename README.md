# Enterprise Healthcare Ingestion & Analytics Pipeline

A production-grade Python data engineering pipeline designed to ingest, validate, sanitize, and analyze clinical admission records. Built with strict data quality assertions, HIPAA-aligned pseudonymization, automated testing via `pytest`, continuous integration via GitHub Actions, and high-performance Apache Parquet serialization.

---

## Architecture Overview

```text
healthcare_analytics/
│
├── .github/workflows/
│   └── ci.yml               # Automated CI: linting (Ruff) + test suite on push/PR
│
├── data/
│   ├── raw/                 # Raw source CSVs (git-ignored)
│   └── processed/           # Validated, compressed Parquet tables
│
├── src/
│   ├── __init__.py
│   ├── anonymizer.py        # Salted SHA-256 patient pseudonymization
│   ├── schemas.py           # Domain validation & corruption quarantine filter
│   └── pipeline.py          # Orchestration: ingestion, metric engineering, Parquet output
│
├── tests/
│   ├── test_anonymizer.py   # Determinism, salting, & edge case unit tests
│   ├── test_validation.py   # Schema integrity & boundary assertion tests
│   └── test_pipeline.py     # End-to-end integration test
│
├── healthcare_eda.ipynb     # Interactive operational EDA & payer variance audit
├── requirements.txt         # Pinned production & development dependencies
└── .gitignore               # Caches, virtual environments, and raw data exclusion
```

---

## Key Pipeline Features

1. **PHI Pseudonymization (`src/anonymizer.py`)**
   - Applies salted SHA-256 hashing to raw patient identifiers.
   - Enforces normalization (whitespace trimming, case flattening) to preserve deterministic joins across multi-visit admissions while keeping raw PHI out of downstream analytics.

2. **Data Quarantine & Clinical Validation (`src/schemas.py`)**
   - Automatically drops corrupted records while preserving pipeline throughput.
   - Filters out:
     - Inverted temporal sequences (`Discharge Date < Date of Admission`).
     - Negative billing values (`Billing Amount < 0`).
     - Impossible biological ages (`Age < 0` or `Age > 125`).
     - Missing mandatory schema features.
   - **Result:** Safely quarantined 108 corrupted entries from 55,500 raw records without crashing pipeline execution.

3. **Feature Engineering & Serialization (`src/pipeline.py`)**
   - Calculates operational metrics:
     - `Length_of_Stay_Days`: Net inpatient stay duration.
     - `Daily_Billing_Rate`: Incurred cost normalized by stay duration (0-day admissions handled via zero-division fallback).
   - Serializes clean records into Apache Parquet format for fast, compressed columnar querying.

4. **CI/CD Automation (`.github/workflows/ci.yml`)**
   - Configured for automated Ubuntu runners.
   - Runs `ruff` for code hygiene and executes all 9 `pytest` test suites across PRs and main merges.

---

## Quickstart

### 1. Environment Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd healthcare_analytics

# Install dependencies
pip install -r requirements.txt

Run Test Suite
Bash
pytest tests/ -v


Execute Pipeline
Bash
python -m src.pipeline