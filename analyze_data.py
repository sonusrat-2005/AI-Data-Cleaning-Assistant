import pandas as pd

from modules.analysis import analyze_dataset
from modules.cleaning import clean_dataset


df = pd.read_csv("sample_data/messy_students.csv")

results = analyze_dataset(df)

cleaned_df = clean_dataset(df)

print("\n===== CLEANING RESULTS =====")

print("Original rows:", len(df))
print("Cleaned rows:", len(cleaned_df))

print("\nCleaned Dataset:")
print(cleaned_df)

print("\nCleaned Data Types:")
print(cleaned_df.dtypes)

print("\nPotential Outliers:")

outliers = results["outliers"]

if outliers:
    for column, rows in outliers.items():
        print(f"\nColumn: {column}")
        print(rows)
else:
    print("No potential outliers detected.")

print("\nInvalid Marks:")

invalid_marks = results["invalid_marks"]

if invalid_marks.empty:
    print("No invalid marks found.")
else:
    print(invalid_marks)