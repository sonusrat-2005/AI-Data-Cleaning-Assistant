import pandas as pd


# ============================================================
# DATA QUALITY SCORE
# ============================================================

def calculate_quality_score(
    df,
    outlier_count=0,
    invalid_count=0,
    inconsistent_count=0
):

    total_rows = len(df)

    total_cells = (
        df.shape[0] * df.shape[1]
    )

    if total_cells == 0:

        return 0


    # ========================================================
    # MISSING VALUES
    # ========================================================

    missing_cells = int(
        df.isnull().sum().sum()
    )

    missing_ratio = (
        missing_cells / total_cells
    )


    # Maximum 30-point penalty
    missing_penalty = min(
        missing_ratio * 30,
        30
    )


    # ========================================================
    # DUPLICATES
    # ========================================================

    duplicate_rows = int(
        df.duplicated().sum()
    )


    if total_rows > 0:

        duplicate_ratio = (
            duplicate_rows / total_rows
        )

    else:

        duplicate_ratio = 0


    # Maximum 20-point penalty
    duplicate_penalty = min(
        duplicate_ratio * 20,
        20
    )


    # ========================================================
    # INVALID DATA
    # ========================================================

    if total_rows > 0:

        invalid_ratio = (
            invalid_count / total_rows
        )

    else:

        invalid_ratio = 0


    # Maximum 20-point penalty
    invalid_penalty = min(
        invalid_ratio * 20,
        20
    )


    # ========================================================
    # INCONSISTENT TEXT
    # ========================================================

    if total_rows > 0:

        inconsistent_ratio = (
            inconsistent_count / total_rows
        )

    else:

        inconsistent_ratio = 0


    # Maximum 15-point penalty
    inconsistent_penalty = min(
        inconsistent_ratio * 15,
        15
    )


    # ========================================================
    # OUTLIERS
    # ========================================================

    if total_rows > 0:

        outlier_ratio = (
            outlier_count / total_rows
        )

    else:

        outlier_ratio = 0


    # Maximum 15-point penalty
    outlier_penalty = min(
        outlier_ratio * 15,
        15
    )


    # ========================================================
    # FINAL SCORE
    # ========================================================

    score = (
        100
        - missing_penalty
        - duplicate_penalty
        - invalid_penalty
        - inconsistent_penalty
        - outlier_penalty
    )


    score = max(
        0,
        min(
            100,
            score
        )
    )


    return round(
        score,
        2
    )