#### Author : Shesadree Priyadarshani
#### Date: 15th Feb 2026

# ICU Mortality Prediction Using First 72 Hours of MIMIC-IV Data

This project develops a data-driven approach to predict ICU mortality using clinical data collected within the first 72 hours of ICU admission from the MIMIC-IV database.

The workflow includes database design, feature engineering, exploratory analysis, machine learning modeling, and an interactive clinical decision support dashboard — all documented for full reproducibility.

> **Prediction Note:** The model predicts the probability of **in-ICU mortality** using early clinical indicators. It does not predict death within 72 hours — it estimates overall ICU mortality risk based on data from the first 72-hour window.

---

# Repository Structure

```
CAP5771_LILI1501/
│
├── diary/
│   ├── problem_formulation.txt
│   ├── data_acquisition.txt
│   ├── data_acquisition_II_database.txt
│   ├── data_exploration.txt
│   ├── reflection_and_next_steps.txt
│   ├── figures/
|       └── describe.png
|       └── info.png
|
├── database_schema.png
│
├── data_dictionary.pdf
│
├── Milestone1.ipynb
│
├── 4.Data_Modeling.ipynb         ← Baseline and improved modeling
├── 5.Data_Visualization.ipynb    ← EDA visualizations
├── 8_Voila_Dashboard.ipynb       ← Interactive clinical dashboard (Voilà)
│
├── icu_mortality_model.pkl       ← Trained ensemble model (Git LFS, 361MB)
├── icu_mortality_threshold.pkl   ← Decision threshold (0.1428)
│
├── Hospital.png                  ← Dashboard hero image
├── mimic dataset/
│   └── icu_final_df.csv          ← Processed feature dataset
│
├── voila_config.py               ← Voilà server configuration
│
├── db_instruction.md (see access instructions how to create)
│
├── requirements.txt
│
└── README.md
```

---

# 1. Problem Formulation

## Objective

Develop a predictive model to estimate the probability of ICU mortality using patient data from the first 72 hours of ICU admission.

## Problem Type

Binary classification.

## Inputs

Features derived within 72 hours of ICU admission:

- Demographics (age, gender, race, ICU type)
- Vital signs (heart rate, MAP, respiratory rate, SpO2, SBP, DBP)
- Laboratory markers (lactate, creatinine, bilirubin, BUN, WBC, platelets, sodium, potassium)
- Urine output (total over 72 hours)

## Output

- `hospital_expire_flag`
  - 0 → Survived
  - 1 → Died during hospital stay

## Time Horizon

All features are restricted to measurements within the first 72 hours of ICU admission to prevent data leakage.

---

# 2. Data Acquisition & Documentation

## Data Source

- Dataset: MIMIC-IV (Medical Information Mart for Intensive Care)
- Hosted on PhysioNet
- Credentialed access required

## Acquisition Process

1. Download CSV files from PhysioNet.
2. Create a local SQLite database (`mimic_iv.db`).
3. Load raw tables:
   - patients
   - admissions
   - icustays
   - chartevents
   - labevents
   - outputevents
4. Create filtered views for the first 72 hours:
   - chartevents_72h
   - labevents_72h
   - outputevents_72h
5. Aggregate features using SQL `GROUP BY stay_id`.
6. Merge into final modeling table: `icu_features`.

All steps are reproducible through SQL queries and Python scripts.

---

# 3. Data Acquisition II – Database Storage

- Database type: SQLite
- One row in final table represents one ICU stay.
- Relational keys used for joins:
  - `subject_id`
  - `hadm_id`
  - `stay_id`
  - `itemid`
- These identifiers are used for linking and aggregation but are not predictive features.

Database schema visualization is included in:

```
database_schema.png
```

---

# 4. Data Exploration

Exploratory analysis included:

- Mortality distribution (class imbalance identified ~12–15%)
- Age distribution (majority 55–75 years)
- Length of stay (right-skewed)
- Vital signs vs mortality (hemodynamic instability in non-survivors)
- Laboratory markers vs mortality (organ dysfunction patterns)
- Missingness analysis (higher in selected lab tests)
- Correlation matrix (high correlation among min/mean/max variants)

Key findings:

- Non-survivors showed elevated lactate, creatinine, bilirubin.
- Blood pressure was lower in non-survivors.
- Several derived features were highly correlated and reduced.

---

# 5. Reflection and Next Steps

## Identified Issues

- Class imbalance
- Missing laboratory data
- Multicollinearity among summary statistics
- Skewed distributions (LOS, lab markers)
- Potential outliers

## Next Steps

- Remove redundant features
- Apply missing value imputation
- Log-transform skewed variables
- Address class imbalance
- Build baseline logistic regression model
- Compare with tree-based models
- Evaluate using AUROC and precision-recall
- Analyze feature importance

---

# 6. Database Schema

The database schema ER diagram as follows :

![db schema Describe](database_schema.png)

It illustrates:

- Core relational tables
- Aggregation tables
- Final modeling table
- Foreign key relationships

---

# 7. Data Dictionary

The complete data dictionary is provided as:

![data dictionary](data_dictionary.pdf)

It describes:

- Variable definitions
- Units of measurement
- Aggregation logic
- Source tables
- Role (identifier vs feature)

---

# 8. Code Implementation

The main implementation file:

```
Milestone1.ipynb
```
![Milestione1](Milestone1.ipynb)

Includes:

- Problem formulation
- Data acquisition
- Database construction
- Feature engineering
- Data exploration

All processing is reproducible and programmatically executed.

---

# 9. Machine Learning Model

## Model Architecture

The final model is a **soft-voting ensemble** combining three classifiers:

| Component | Weight | Class Handling |
|---|---|---|
| HistGradientBoosting (HGB) | 2 | class_weight='balanced' |
| Random Forest (RF) | 1 | Explicit ratio search w ∈ [5,7,10,15,20] |
| XGBoost | 2 | scale_pos_weight = neg/pos |

## Training Strategy

| Setting | Value |
|---|---|
| Resampling | SMOTE (k=5) inside imblearn.Pipeline |
| CV strategy | StratifiedKFold (5 fold) |
| CV scorer | Recall with precision floor ≥ 0.40 |
| Calibration | Platt sigmoid (CalibratedClassifierCV) |
| Decision threshold | 0.1428 |
| ROC-AUC | 0.922 |
| Dataset size | 47,291 ICU patients (~12% mortality) |

## Threshold Selection

- Recall ≥ 0.80 constraint enforced first
- Precision floor ≥ 0.40 to avoid rubber-stamp predictions
- F1 maximised within those constraints

## Risk Tiers

| Risk Level | Probability Range | Recommendation |
|---|---|---|
| Low Risk | < 0.1428 | Continue standard monitoring |
| Moderate Risk | 0.1428 – 0.2928 | Increased monitoring |
| High Risk | 0.2928 – 0.4928 | Intervention recommended |
| Critical Risk | > 0.4928 | Urgent intervention |

---

# 10. Clinical Dashboard

## Overview

An interactive clinical decision support dashboard built with **Voilà** and **ipywidgets**, deployed from `8_Voila_Dashboard.ipynb`.

## Dashboard Sections

### Home
- Hero landing page with project overview and Start Patient Assessment button
- Feature cards explaining each section (Population Overview, Data Explorer, Patient Assessment)

### Overview Tab
- Population statistics (total patients, mortality rate, median age, LOS)
- Outcome distribution pie chart
- Age distribution by outcome
- Mortality rate by care unit
- Key lab medians by outcome
- Length of stay boxplot

### Patient Assessment
- Input form for demographics, vitals (mean/min/max), labs, and fluid output
- Supports blank fields or `NA` for unavailable values — model imputes automatically
- Units reference tables for vitals and labs
- Real-time mortality risk prediction with risk gauge
- Vitals and labs status bar chart (Blue=Normal, Orange=Warning, Red=Critical, Grey=NA)
- Clinical alerts (critical and warning value flags)
- Clinical action items with recommended interventions

### Data Explorer Tab
- Interactive feature distribution explorer (histogram, box, violin)
- Correlation heatmap (Vitals / Labs / All features)
- Missing data map

## Running the Dashboard

```bash
conda activate data_catalyst

# Trust the notebook (required once)
jupyter trust 8_Voila_Dashboard.ipynb

# Launch dashboard
voila 8_Voila_Dashboard.ipynb --port=8502 --no-browser --config=voila_config.py --ExecutePreprocessor.timeout=300
```

Then open the forwarded port URL in your browser (e.g. via VS Code tunnel at `https://<tunnel>-8502.use2.devtunnels.ms`).

### voila_config.py

```python
c.ServerApp.disable_check_xsrf = True
c.ServerApp.allow_origin = '*'
c.ServerApp.tornado_settings = {'xsrf_cookies': False}
```

---

# 11. Reproducing the Project

## Step 1 – Clone Repository

```bash
git clone https://github.com/lili1501/CAP5771_lili1501.git
cd CAP5771_LILI1501
```

## Step 2 – Pull Model Files (Git LFS)

The model file (`icu_mortality_model.pkl`) is 361MB and stored via Git LFS.

```bash
git lfs install
git lfs pull
```

If Git LFS is unavailable, place `icu_mortality_model.pkl` manually in the project root directory. The dashboard will fall back to demo mode if the file is not found.

## Step 3 – Create Environment

Using conda:

```bash
conda create -n icu_env python=3.10
conda activate icu_env
```

## Step 4 – Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 12. Database File or Access Instructions

## Generate Database

1. Obtain credentialed access to MIMIC-IV via PhysioNet.
2. Download required CSV files.
3. Run the notebook or scripts to:
   - Load tables
   - Create filtered views
   - Generate aggregated feature tables
4. The database will be created locally as (see instruction in db_instruction):

```
mimic_iv.db
```

[db_instruction.md](db_instruction.md)

---

# 13. Dependencies

Listed in `requirements.txt`:

- pandas
- numpy
- matplotlib
- seaborn
- tqdm
- jupyter
- scikit-learn
- imbalanced-learn
- xgboost
- plotly
- ipywidgets
- voila
- joblib

SQLite is included in the Python standard library.

---

# Summary

This repository demonstrates:

- Structured relational database design
- Time-window feature engineering
- Clinical exploratory data analysis
- Reproducible ML modeling pipeline with ensemble methods and SMOTE
- Interactive clinical decision support dashboard (Voilà)
- Complete documentation

All components are organized for clarity, reproducibility, and academic evaluation.

---

> **Disclaimer:** This dashboard is intended for clinical decision support only. All predictions should be interpreted in the context of the full clinical picture by a qualified healthcare professional. This tool is not a substitute for clinical judgment.