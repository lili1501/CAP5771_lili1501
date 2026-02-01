
-----------------------------------------------------------------------
DATABASE TABLES AND RELATIONSHIPS (DATABASE MANAGEMENT)
-----------------------------------------------------------------------

This project uses the MIMIC-IV clinical database. The analysis requires a subset of core
tables that capture patient demographics, hospital admissions, ICU stays, diagnoses,
clinical measurements, laboratory tests, medications, and procedures. The database
follows a relational design with well-defined primary and foreign keys.

The key tables required for this project are:

1. patients
   This table contains patient-level demographic information. The primary key is
   subject_id, which uniquely identifies each patient and is used to link patient data
   across all other tables.

2. admissions
   This table contains hospital admission-level information such as admission time,
   discharge time, admission type, insurance, and ethnicity. It is linked to patients
   through subject_id and represents a single hospitalization using hadm_id as the
   primary key.

3. icustays
   This table contains ICU-level information, including ICU admission and discharge
   times. It links to admissions using hadm_id and to patients using subject_id. The
   primary key is stay_id, which uniquely identifies each ICU stay.

4. diagnoses_icd
   This table contains ICD-9 and ICD-10 diagnosis codes assigned during a hospital
   admission. It is linked to admissions through hadm_id and to patients through
   subject_id. These codes are used to derive baseline comorbidities and to construct
   disease category outcome labels.

5. chartevents
   This table stores time-stamped bedside measurements such as vital signs. It links to
   patients, admissions, and ICU stays using subject_id, hadm_id, and stay_id. The
   itemid field identifies the type of clinical measurement.

6. labevents
   This table contains laboratory test results. It links to patients and admissions using
   subject_id and hadm_id. The itemid field identifies the specific laboratory test.

7. prescriptions
   This table contains medication orders during a hospital stay. It links to patients and
   admissions using subject_id and hadm_id and is used to identify early medication
   exposure such as antibiotics or vasopressors.

8. procedureevents
   This table records ICU procedures such as mechanical ventilation and dialysis. It
   links to patients, admissions, and ICU stays using subject_id, hadm_id, and stay_id.

9. mimiciv_derived tables (e.g., sofa)
   These tables contain precomputed severity scores derived from raw clinical data.
   They link to patients, admissions, and ICU stays and are used as baseline severity
   indicators.

-----------------------------------------------------------------------
DATABASE CONNECTION OVERVIEW (TEXTUAL DB DIAGRAM)
-----------------------------------------------------------------------

patients (subject_id)
        |
        |--< admissions (hadm_id, subject_id)
                |
                |--< icustays (stay_id, hadm_id, subject_id)
                |        |
                |        |--< chartevents
                |        |--< procedureevents
                |
                |--< diagnoses_icd
                |--< labevents
                |--< prescriptions

All tables are connected through consistent use of subject_id and hadm_id, with ICU-
specific data additionally linked through stay_id.

-----------------------------------------------------------------------
UNSTRUCTURED DATA CONSIDERATIONS
-----------------------------------------------------------------------

MIMIC-IV includes unstructured clinical text data such as discharge summaries,
radiology reports, and progress notes stored in the note-related tables as a csv file.

These notes will be later used by feature engineering if required.

Unstructured text would be transformed into structured features before integration
with the main analytical dataset.


