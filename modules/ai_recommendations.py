import pandas as pd


# ============================================================
# AI CLEANING RECOMMENDATIONS
# ============================================================

def generate_recommendations(df):

    recommendations = []

    # ========================================================
    # MISSING VALUES
    # ========================================================

    for column in df.columns:

        missing_count = int(
            df[column].isnull().sum()
        )

        if missing_count > 0:

            if pd.api.types.is_numeric_dtype(
                df[column]
            ):

                recommendations.append({

                    "column": column,

                    "problem": "Missing values",

                    "recommendation":
                        "Fill missing values using the median.",

                    "reason":
                        "This is a numerical column. "
                        "Median is less affected by extreme "
                        "values than the mean."
                })

            else:

                recommendations.append({

                    "column": column,

                    "problem": "Missing values",

                    "recommendation":
                        "Fill missing values using the mode.",

                    "reason":
                        "This is a text or categorical "
                        "column. The mode represents the "
                        "most common value."
                })


    # ========================================================
    # DUPLICATES
    # ========================================================

    duplicate_count = int(
        df.duplicated().sum()
    )

    if duplicate_count > 0:

        recommendations.append({

            "column": "Dataset",

            "problem": "Duplicate rows",

            "recommendation":
                "Remove duplicate rows.",

            "reason":
                "Duplicate records can cause repeated "
                "information and may affect analysis results."
        })


    # ========================================================
    # INVALID NUMERICAL DATA
    # ========================================================

    if "Age" in df.columns:

        age_numeric = pd.to_numeric(
            df["Age"],
            errors="coerce"
        )

        invalid_age = (
            age_numeric.isna()
            &
            df["Age"].notna()
        )

        if invalid_age.any():

            recommendations.append({

                "column": "Age",

                "problem":
                    "Non-numeric values",

                "recommendation":
                    "Convert valid values to numbers "
                    "and replace invalid values with the "
                    "median age.",

                "reason":
                    "Age should contain numerical values."
            })


    if "Marks" in df.columns:

        marks_numeric = pd.to_numeric(
            df["Marks"],
            errors="coerce"
        )

        invalid_marks = (
            marks_numeric.isna()
            &
            df["Marks"].notna()
        )

        if invalid_marks.any():

            recommendations.append({

                "column": "Marks",

                "problem":
                    "Non-numeric values",

                "recommendation":
                    "Convert valid values to numbers "
                    "and replace invalid values with "
                    "the median marks.",

                "reason":
                    "Marks should contain numerical "
                    "values between 0 and 100."
            })


    # ========================================================
    # INCONSISTENT TEXT
    # ========================================================

    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:

        values = df[column].dropna()

        if values.empty:
            continue

        normalized = (
            values.astype(str)
            .str.strip()
            .str.lower()
        )

        if len(
            set(values.astype(str))
        ) != len(
            set(normalized)
        ):

            recommendations.append({

                "column": column,

                "problem":
                    "Inconsistent text formatting",

                "recommendation":
                    "Standardize text using consistent "
                    "capitalization and remove extra spaces.",

                "reason":
                    "Different text representations "
                    "can be treated as separate categories "
                    "during analysis."
            })


    # ========================================================
    # RETURN
    # ========================================================

    return recommendations