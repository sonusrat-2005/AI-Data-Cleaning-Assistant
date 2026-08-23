import pandas as pd

from modules.quality_score import (
    calculate_quality_score
)


# Load dataset
df = pd.read_csv(
    "sample_data/messy_students.csv"
)


# Calculate quality score
score = calculate_quality_score(
    df
)


print("\n==============================")
print("       DATA QUALITY SCORE")
print("==============================")


print(
    f"Quality Score: {score}/100"
)