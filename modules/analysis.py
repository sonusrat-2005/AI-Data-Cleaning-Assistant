import pandas as pd


# ============================================================
# DATASET INFORMATION
# ============================================================

def get_dataset_info(df):

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": df.columns.tolist()
    }


# ============================================================
# MISSING VALUES
# ============================================================

def find_missing_values(df):

    missing_count = df.isnull().sum()

    if len(df) > 0:
        missing_percentage = (
            missing_count / len(df)
        ) * 100
    else:
        missing_percentage = missing_count * 0

    return {
        "count": missing_count[
            missing_count > 0
        ],
        "percentage": missing_percentage[
            missing_percentage > 0
        ]
    }


# ============================================================
# DUPLICATES
# ============================================================

def find_duplicates(df):

    return int(
        df.duplicated().sum()
    )


# ============================================================
# DATA TYPES
# ============================================================

def check_data_types(df):

    return df.dtypes


# ============================================================
# OUTLIERS
# ============================================================

def find_outliers(df):

    outliers = {}

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    for column in numeric_columns:

        values = df[column].dropna()

        if len(values) < 4:
            continue

        Q1 = values.quantile(0.25)
        Q3 = values.quantile(0.75)

        IQR = Q3 - Q1

        if IQR == 0:
            continue

        lower_limit = Q1 - 1.5 * IQR
        upper_limit = Q3 + 1.5 * IQR

        column_outliers = df[
            (df[column] < lower_limit)
            |
            (df[column] > upper_limit)
        ]

        if not column_outliers.empty:

            outliers[column] = column_outliers

    return outliers


# ============================================================
# INVALID MARKS
# ============================================================

def find_invalid_marks(df):

    if "Marks" not in df.columns:

        return df.iloc[0:0]

    marks_numeric = pd.to_numeric(
        df["Marks"],
        errors="coerce"
    )

    invalid = df[
        (
            marks_numeric < 0
        )
        |
        (
            marks_numeric > 100
        )
        |
        (
            marks_numeric.isna()
            &
            df["Marks"].notna()
        )
    ]

    return invalid


# ============================================================
# INVALID AGE
# ============================================================

def find_invalid_age(df):

    if "Age" not in df.columns:

        return df.iloc[0:0]

    age_numeric = pd.to_numeric(
        df["Age"],
        errors="coerce"
    )

    invalid = df[
        (
            age_numeric < 0
        )
        |
        (
            age_numeric > 120
        )
        |
        (
            age_numeric.isna()
            &
            df["Age"].notna()
        )
    ]

    return invalid


# ============================================================
# DATA TYPE ISSUES
# ============================================================

def find_data_type_issues(df):

    issues = {}

    # --------------------------------------------------------
    # AGE
    # --------------------------------------------------------

    if "Age" in df.columns:

        age_numeric = pd.to_numeric(
            df["Age"],
            errors="coerce"
        )

        invalid_mask = (
            age_numeric.isna()
            &
            df["Age"].notna()
        )

        if invalid_mask.any():

            issues["Age"] = (
                df.loc[
                    invalid_mask,
                    "Age"
                ]
                .astype(str)
                .tolist()
            )

    # --------------------------------------------------------
    # MARKS
    # --------------------------------------------------------

    if "Marks" in df.columns:

        marks_numeric = pd.to_numeric(
            df["Marks"],
            errors="coerce"
        )

        invalid_mask = (
            marks_numeric.isna()
            &
            df["Marks"].notna()
        )

        if invalid_mask.any():

            issues["Marks"] = (
                df.loc[
                    invalid_mask,
                    "Marks"
                ]
                .astype(str)
                .tolist()
            )

    return issues


# ============================================================
# INCONSISTENT TEXT
# ============================================================

def find_inconsistent_text(df):

    inconsistencies = {}

    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:

        values = df[column].dropna()

        if values.empty:
            continue

        values = values.astype(str)

        normalized = (
            values
            .str.strip()
            .str.lower()
        )

        groups = {}

        for original, normalized_value in zip(
            values,
            normalized
        ):

            groups.setdefault(
                normalized_value,
                set()
            )

            groups[
                normalized_value
            ].add(original)

        column_issues = {}

        for normalized_value, variants in groups.items():

            if len(variants) > 1:

                column_issues[
                    normalized_value
                ] = sorted(
                    variants
                )

        if column_issues:

            inconsistencies[column] = (
                column_issues
            )

    return inconsistencies


# ============================================================
# COMPLETE ANALYSIS
# ============================================================

def analyze_dataset(df):

    return {

        "dataset_info":
            get_dataset_info(df),

        "missing_values":
            find_missing_values(df),

        "duplicates":
            find_duplicates(df),

        "data_types":
            check_data_types(df),

        "outliers":
            find_outliers(df),

        "invalid_marks":
            find_invalid_marks(df),

        "invalid_age":
            find_invalid_age(df),

        "data_type_issues":
            find_data_type_issues(df),

        "inconsistent_text":
            find_inconsistent_text(df)
    }


# ============================================================
# DATASET VALIDATION
# ============================================================

def validate_dataset(
    df,
    original_columns=None
):

    errors = []

    if df.empty:

        errors.append(
            "The dataset is empty."
        )

        return errors

    if len(df.columns) == 0:

        errors.append(
            "The dataset has no columns."
        )

        return errors

    if len(df.columns) == 1:

        errors.append(
            "The dataset contains only one column. "
            "Please check the CSV format."
        )

    empty_columns = df.columns[
        df.isnull().all()
    ].tolist()

    if empty_columns:

        errors.append(
            "The following columns contain no data: "
            +
            ", ".join(
                empty_columns
            )
        )

    if original_columns is not None:

        duplicate_columns = []

        seen = set()

        for column in original_columns:

            if column in seen:

                if column not in duplicate_columns:

                    duplicate_columns.append(
                        column
                    )

            else:

                seen.add(column)

        if duplicate_columns:

            errors.append(
                "The dataset contains duplicate "
                "column names: "
                +
                ", ".join(
                    duplicate_columns
                )
            )

    return errors