# Enterprise Healthcare Ingestion & Analytics Pipeline

A production-grade Python data engineering pipeline designed to ingest, validate, sanitize, and analyze clinical admission records. Built with strict data quality assertions, HIPAA-aligned pseudonymization, automated testing via `pytest`, continuous integration via GitHub Actions, and high-performance Apache Parquet serialization.

---

## Architecture Overview

| Path / Module | Layer | Description |
| :--- | :--- | :--- |
| `.github/workflows/ci.yml` | CI/CD | Automated linting (`ruff`) and `pytest` execution on push/PR |
| `data/raw/` | Storage (Raw) | Source clinical CSV datasets (untracked in Git) |
| `data/processed/` | Storage (Clean) | Validated, compressed Apache Parquet analytical tables |
| `src/anonymizer.py` | Security / PHI | Salted SHA-256 deterministic patient pseudonymization |
| `src/schemas.py` | Validation | Domain boundary enforcement and corrupt record quarantine |
| `src/pipeline.py` | Orchestration | End-to-end ingestion, feature engineering, and serialization |
| `tests/test_anonymizer.py` | Unit Test | Hash determinism, salting, and whitespace normalization tests |
| `tests/test_validation.py` | Unit Test | Temporal inversion, negative billing, and age boundary assertions |
| `tests/test_pipeline.py` | Integration Test | Full pipeline execution and Parquet output verification |
| `healthcare_eda.ipynb` | Analytics | Interactive LOS capacity analysis and payer financial audit |
| `requirements.txt` | Environment | Pinned production and testing package dependencies |

---

## Mathematical Formulation & Engineering Logic

### 1. Cryptographic PHI Pseudonymization
To maintain HIPAA-aligned de-identification while preserving longitudinal patient tracking across multiple hospital admissions, raw patient identifiers $P_{\mathrm{raw}}$ are normalized (case-folded and whitespace-trimmed) and passed through a salted SHA-256 cryptographic hash function with a secret application salt $S$:

$$\mathrm{ID}_{\mathrm{patient}} = \mathrm{PT-} \parallel \mathrm{SHA256}\left(\mathrm{lower}\left(\mathrm{trim}(P_{\mathrm{raw}})\right) \parallel S\right)_{[0:12]}$$

### 2. Clinical Domain Validation & Quarantine Set
Let $D$ represent the raw dataset of $N = 55,500$ clinical records. A record $r_i \in D$ is admitted to the validated analytical set $D_{\mathrm{clean}}$ if and only if it satisfies all four clinical and financial invariants:

$$D_{\mathrm{clean}} = \lbrace r_i \in D \mid (T_{\mathrm{discharge}, i} \ge T_{\mathrm{admission}, i}) \land (B_i \ge 0) \land (0 \le A_i \le 125) \land (\Phi_i \neq \emptyset) \rbrace$$

Where:
* $T_{\mathrm{admission}, i}$ and $T_{\mathrm{discharge}, i}$ denote the admission and discharge timestamps.
* $B_i$ is the total billed amount.
* $A_i$ is the biological patient age at admission.
* $\Phi_i$ represents the vector of mandatory clinical schema fields.
* **Quarantine Yield:** $\vert{}D \setminus D_{\mathrm{clean}}\vert{} = 108$ corrupt records isolated and dropped, leaving $\vert{}D_{\mathrm{clean}}\vert{} = 55,392$ verified records.

### 3. Operational Metric Engineering
For each validated record $r_i \in D_{\mathrm{clean}}$, net inpatient **Length of Stay ($\mathrm{LOS}_i$)** in days is computed as:

$$\mathrm{LOS}_i = (T_{\mathrm{discharge}, i} - T_{\mathrm{admission}, i})_{\mathrm{days}}$$

To normalize financial auditing across same-day discharges ($\mathrm{LOS}_i = 0$) and multi-week stays without zero-division faults, the **Daily Billing Rate ($R_{\mathrm{daily}, i}$)** is formulated with a unit-day floor:

$$R_{\mathrm{daily}, i} = \frac{B_i}{\max(\mathrm{LOS}_i, 1)}$$

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
   - Calculates operational metrics (`Length_of_Stay_Days` and `Daily_Billing_Rate`).
   - Serializes clean records into Apache Parquet format for fast, compressed columnar querying.

4. **CI/CD Automation (`.github/workflows/ci.yml`)**
   - Configured for automated Ubuntu runners.
   - Runs `ruff` for code hygiene and executes all 9 `pytest` test suites across PRs and main merges.

---

## Quickstart

### 1. Environment Setup
```bash
git clone [https://github.com/AshutoshTembhekar/healthcare-analysis.git](https://github.com/AshutoshTembhekar/healthcare-analysis.git)
cd healthcare-analysis
pip install -r requirements.txt
```

### 2. Run Test Suite
```bash
pytest tests/ -v
```

### 3. Execute Pipeline
```bash
python -m src.pipeline
```

### 4. Interactive Analysis
Launch `healthcare_eda.ipynb` inside Jupyter or VS Code to explore capacity dynamics, insurer rate variances, and operational summaries.

---

## Author

**Ashutosh Tembhekar**  
*Data Analytics & Data Engineering*  
GitHub: https://github.com/AshutoshTembhekar
