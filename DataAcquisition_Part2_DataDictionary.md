** 1. List variables you plan to use **
Under MIMIC IV there are 5 modules and I intend to use the required data file for this project.

Data Source:
MIMIC-IV Clinical Database
Official Documentation: https://mimic.mit.edu/docs/iv/

---

## 1. Patient Identifiers

### Table: patients

| Column | Type | Description |
|------|------|-------------|
| subject_id | INTEGER | Unique identifier for each patient |
| gender | TEXT | Patient’s biological sex |
| anchor_age | INTEGER | Age of the patient at the anchor year |
| anchor_year | INTEGER | Reference year for age shifting |
| anchor_year_group | TEXT | Range of anchor years |

---

## 2. Hospital Admission Information

### Table: admissions

| Column | Type | Description |
|------|------|-------------|
| hadm_id | INTEGER | Unique identifier for a hospital admission |
| subject_id | INTEGER | Links admission to a patient |
| admittime | TIMESTAMP | Date and time of hospital admission |
| dischtime | TIMESTAMP | Date and time of hospital discharge |
| admission_type | TEXT | Emergency, elective, or urgent admission |
| admission_location | TEXT | Location prior to admission |
| discharge_location | TEXT | Location after discharge |
| insurance | TEXT | Insurance type |
| ethnicity | TEXT | Self-reported ethnicity |
| hospital_expire_flag | INTEGER | Indicates in-hospital mortality |

---

## 3. ICU Stay Information

### Table: icustays

| Column | Type | Description |
|------|------|-------------|
| stay_id | INTEGER | Unique ICU stay identifier |
| subject_id | INTEGER | Patient identifier |
| hadm_id | INTEGER | Hospital admission identifier |
| intime | TIMESTAMP | ICU admission time |
| outtime | TIMESTAMP | ICU discharge time |
| los | NUMERIC | Length of ICU stay (days) |

---

## 4. Diagnoses (Observed Only)

### Table: diagnoses_icd

| Column | Type | Description |
|------|------|-------------|
| subject_id | INTEGER | Patient identifier |
| hadm_id | INTEGER | Hospital admission identifier |
| seq_num | INTEGER | Order of diagnosis assignment |
| icd_code | VARCHAR(7) | ICD-9 or ICD-10 diagnosis code |
| icd_version | INTEGER | ICD version (9 or 10) |

**Note:**  
This table does NOT contain comorbidity indices.  
Scores such as Charlson Comorbidity Index are **derived** from `icd_code` and `icd_version`.

---

## 5. Vital Signs and Bedside Measurements

### Table: chartevents

| Column | Type | Description |
|------|------|-------------|
| subject_id | INTEGER | Patient identifier |
| hadm_id | INTEGER | Hospital admission identifier |
| stay_id | INTEGER | ICU stay identifier |
| charttime | TIMESTAMP | Time of measurement |
| itemid | INTEGER | Identifier for type of measurement |
| value | TEXT | Recorded value |
| valuenum | NUMERIC | Numeric representation of value |
| valueuom | TEXT | Unit of measurement |

**Examples of measurements (via itemid):**
- Heart rate  
- Blood pressure  
- Respiratory rate  
- Temperature  
- SpO₂  

---

## 6. Laboratory Measurements

### Table: labevents

| Column | Type | Description |
|------|------|-------------|
| subject_id | INTEGER | Patient identifier |
| hadm_id | INTEGER | Hospital admission identifier |
| itemid | INTEGER | Lab test identifier |
| charttime | TIMESTAMP | Time lab was drawn |
| value | TEXT | Lab result |
| valuenum | NUMERIC | Numeric lab result |
| valueuom | TEXT | Unit of measurement |

**Examples of labs (via itemid):**
- Creatinine  
- BUN  
- Lactate  
- White blood cell count  
- Hemoglobin  
- Platelets  
- Sodium  
- Potassium  

---

## 7. Medications

### Table: prescriptions

| Column | Type | Description |
|------|------|-------------|
| subject_id | INTEGER | Patient identifier |
| hadm_id | INTEGER | Hospital admission identifier |
| starttime | TIMESTAMP | Medication start time |
| stoptime | TIMESTAMP | Medication stop time |
| drug | TEXT | Medication name |
| drug_type | TEXT | Type of drug entry |
| dose_val_rx | TEXT | Dose value |
| dose_unit_rx | TEXT | Dose unit |
| route | TEXT | Route of administration |

---

## 8. Procedures

### Table: procedureevents

| Column | Type | Description |
|------|------|-------------|
| subject_id | INTEGER | Patient identifier |
| hadm_id | INTEGER | Hospital admission identifier |
| stay_id | INTEGER | ICU stay identifier |
| starttime | TIMESTAMP | Procedure start time |
| endtime | TIMESTAMP | Procedure end time |
| itemid | INTEGER | Procedure identifier |
| value | NUMERIC | Procedure-related value |
| valueuom | TEXT | Unit of measurement |

**Examples (via itemid):**
- Mechanical ventilation  
- Dialysis  

---

## 9. Derived Tables (Provided by MIMIC-IV)

### Table: mimiciv_derived.sofa

Code reference: https://github.com/MIT-LCP/mimic-iv/blob/master/concepts/score/sofa.sql

| Column | Type | Description |
|------|------|-------------|
| subject_id | INTEGER | Patient identifier |
| hadm_id | INTEGER | Hospital admission identifier |
| stay_id | INTEGER | ICU stay identifier |
| starttime | TIMESTAMP | Start time of score window |
| endtime | TIMESTAMP | End time of score window |
| sofa_score | INTEGER | Sequential Organ Failure Assessment score |

---

## Notes on Derived Variables
I intent to derive these variables if enough sources support. Else I will find alternate approach.
- **Charlson Comorbidity Index (CCI)** is NOT a native column.
- CCI is derived from `diagnoses_icd.icd_code` and `icd_version` using standard mappings.
- Only diagnoses present at or before admission are used when deriving baseline comorbidities.
- Disease category labels are derived AFTER the baseline window to prevent label leakage.

---

## Data Usage Constraints
- Only data from the **early baseline window** (e.g., first 24 hours) are used as predictors.
- Discharge diagnoses, discharge summaries, and post-baseline information are excluded.
- This is an observational risk prediction task, not a diagnostic system.

