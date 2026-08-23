# AI Data Cleaning Assistant

An AI-powered data cleaning assistant built with Python, Pandas, Streamlit, and Machine Learning.

# Live Demo

[Open the Live Application](https://ai-data-cleaning-assistant-05.streamlit.app/)

### Problem
Real-world datasets frequently contain missing values, duplicate records, inconsistent formats and anomalous values.

### Solution
A Python-based application that automatically analyzes and cleans datasets while providing data-quality recommendations and downloadable results.

The application allows users to upload CSV datasets, analyze their data quality, identify common data problems, receive cleaning recommendations, clean the dataset, and download the cleaned result.

---

# Features

### Dataset Upload

- Upload CSV files through the Streamlit interface
- Validate uploaded datasets
- Handle empty or invalid CSV files
- Preview uploaded datasets

### Data Analysis

The application analyzes datasets for:

- Missing values
- Duplicate rows
- Data type issues
- Inconsistent values
- Statistical outliers
- Invalid marks
- Dataset structure and information

### Data Cleaning

The application can identify and handle common data quality problems, including:

- Missing values
- Duplicate records
- Data type inconsistencies
- Invalid values
- Inconsistent data

### AI Recommendations

The application provides recommendations based on the problems detected in the dataset.

### Machine Learning

Machine learning techniques are used to assist with anomaly detection in datasets.

### Data Quality Score

The application calculates a data quality score to help users understand the overall quality of their dataset.

### Quality Reports

The application provides information about the dataset before and after cleaning.

### Download

Users can download the cleaned dataset for further use.

---

# Technologies Used

- Python
- Pandas
- NumPy
- Streamlit
- Matplotlib
- Scikit-learn

---

# Project Structure

```text
AI_data_cleaning_assistant/
│
├── app.py
├── analyze_data.py
├── test.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── modules/
│   ├── ai_recommendations.py
│   ├── analysis.py
│   ├── cleaning.py
│   ├── ml_anomaly.py
│   ├── quality_score.py
│   └── report.py
│
├── sample_data/
│   ├── duplicate_columns.csv
│   ├── empty.csv
│   ├── empty_column.csv
│   ├── messy_students.csv
│   ├── no_missing_values.csv
│   ├── test_numbers.csv
│   ├── test_one_column.csv
│   └── text_only.csv
│
└── stress_tests/
    ├── test_corrupted.csv
    ├── test_datatypes.csv
    ├── test_duplicates.csv
    ├── test_empty.csv
    ├── test_empty_column.csv
    ├── test_everything.csv
    ├── test_headers_only.csv
    ├── test_inconsistent.csv
    ├── test_missing.csv
    ├── test_mixed_values.csv
    ├── test_one_column.csv
    └── test_outliers.csv
