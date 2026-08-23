import pandas as pd


# ============================================================
# CLEAN DATASET
# ============================================================

def clean_dataset(df):

    cleaned_df = df.copy()


    # ========================================================
    # 1. REMOVE DUPLICATES
    # ========================================================

    cleaned_df = (
        cleaned_df
        .drop_duplicates()
        .reset_index(drop=True)
    )


    # ========================================================
    # 2. FIX NUMERICAL COLUMNS
    # ========================================================

    # --------------------------------------------------------
    # AGE
    # --------------------------------------------------------

    if "Age" in cleaned_df.columns:

        age_numeric = pd.to_numeric(
            cleaned_df["Age"],
            errors="coerce"
        )

        # Calculate median from valid values
        age_median = age_numeric.median()

        if pd.notna(age_median):

            cleaned_df["Age"] = (
                age_numeric
                .fillna(age_median)
            )

        else:

            cleaned_df["Age"] = age_numeric


    # --------------------------------------------------------
    # MARKS
    # --------------------------------------------------------

    if "Marks" in cleaned_df.columns:

        marks_numeric = pd.to_numeric(
            cleaned_df["Marks"],
            errors="coerce"
        )

        # Values outside valid range
        marks_numeric = marks_numeric.where(
            marks_numeric.between(
                0,
                100
            )
        )

        marks_median = marks_numeric.median()

        if pd.notna(marks_median):

            cleaned_df["Marks"] = (
                marks_numeric
                .fillna(marks_median)
            )

        else:

            cleaned_df["Marks"] = marks_numeric


    # ========================================================
    # 3. FILL OTHER MISSING VALUES
    # ========================================================

    for column in cleaned_df.columns:

        if cleaned_df[column].isnull().sum() == 0:
            continue


        # Numerical column
        if pd.api.types.is_numeric_dtype(
            cleaned_df[column]
        ):

            median_value = (
                cleaned_df[column]
                .median()
            )

            if pd.notna(median_value):

                cleaned_df[column] = (
                    cleaned_df[column]
                    .fillna(median_value)
                )


        # Text / categorical column
        else:

            mode_values = (
                cleaned_df[column]
                .mode()
            )

            if not mode_values.empty:

                mode_value = (
                    mode_values.iloc[0]
                )

                cleaned_df[column] = (
                    cleaned_df[column]
                    .fillna(mode_value)
                )


    # ========================================================
    # 4. STANDARDIZE TEXT
    # ========================================================

    text_columns = cleaned_df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:

        cleaned_df[column] = (
            cleaned_df[column]
            .astype(str)
            .str.strip()
        )


        # Consistent capitalization
        cleaned_df[column] = (
            cleaned_df[column]
            .str.title()
        )


    # ========================================================
    # 5. RESET INDEX
    # ========================================================

    cleaned_df = (
        cleaned_df
        .reset_index(drop=True)
    )


    return cleaned_df