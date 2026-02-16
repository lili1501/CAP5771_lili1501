# Creating the SQLite Database (`mimic.db`)

This project uses a SQLite database built from the MIMIC-IV dataset.

Due to PhysioNet licensing restrictions, the `.db` file is not included in this repository.  
You must generate it locally after obtaining credentialed access to MIMIC-IV.

---

## Step 1: Obtain MIMIC-IV Access

1. Complete the required CITI training.
2. Create a PhysioNet account.
3. Request credentialed access to **MIMIC-IV Clinical Database**.

PhysioNet:  
https://physionet.org/

After approval, download the MIMIC-IV dataset.
Note: Not all the datasets needs to be downloaded for this project.
Required: 
- hosp
  - patients
  - admissions
  - diagnoses_icd
  - labevents
  - d.labitems (mapping)

- icu
  - icustays
  - inputevents
  - outputevents
  - chartevents
  - d_items (mapping)

Optional
- hosp
  - diagnoses_icd
  - d_icd_diagnoses
  - d_icd_procedures
- icu
  - inputevents
  - procedurevents

---

## Step 2: Organize the Files

After downloading and extracting the dataset, place the required CSV files in:

1. hosp: mimic dataset/hosp
2. icu: mimic dataset/icu

## Step 2: Create tables

Import required libraries (sqlite3) and use the code under DATA ACQUISITION (DATABASE MANAGEMENT) in Milestone1.ipynb for schema and rest of the procedures.

![Milesrtone1](Milestone1.ipynb)

