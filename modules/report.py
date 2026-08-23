from modules.analysis import (
    find_data_type_issues,
    find_inconsistent_text
)


# ============================================================
# QUALITY REPORT
# ============================================================

def generate_quality_report(
    df,
    cleaned_df,
    before_score,
    after_score,
    recommendations,
    anomalies
):

    report = []


    report.append(
        "AI DATA CLEANING ASSISTANT"
    )

    report.append(
        "=" * 40
    )

    report.append("")


    # ========================================================
    # DATASET INFORMATION
    # ========================================================

    report.append(
        "DATASET INFORMATION"
    )

    report.append(
        "-" * 40
    )

    report.append(
        f"Rows before cleaning: {df.shape[0]}"
    )

    report.append(
        f"Columns: {df.shape[1]}"
    )

    report.append(
        f"Rows after cleaning: {cleaned_df.shape[0]}"
    )

    report.append("")


    # ========================================================
    # PROBLEMS DETECTED
    # ========================================================

    report.append(
        "PROBLEMS DETECTED"
    )

    report.append(
        "-" * 40
    )


    # Missing
    missing_values = int(
        df.isnull().sum().sum()
    )

    report.append(
        f"Missing values: {missing_values}"
    )


    # Duplicates
    duplicate_rows = int(
        df.duplicated().sum()
    )

    report.append(
        f"Duplicate rows: {duplicate_rows}"
    )


    # ========================================================
    # DATA TYPE ISSUES
    # ========================================================

    data_type_issues = (
        find_data_type_issues(df)
    )


    if data_type_issues:

        report.append(
            "Invalid data type values:"
        )

        for column, values in (
            data_type_issues.items()
        ):

            report.append(
                f"- {column}: "
                f"{', '.join(values)}"
            )

    else:

        report.append(
            "Invalid data type values: 0"
        )


    # ========================================================
    # INCONSISTENT TEXT
    # ========================================================

    inconsistent_text = (
        find_inconsistent_text(df)
    )


    if inconsistent_text:

        report.append(
            "Inconsistent text:"
        )

        for column, issues in (
            inconsistent_text.items()
        ):

            for normal_value, variants in (
                issues.items()
            ):

                report.append(
                    f"- {column}: "
                    f"{', '.join(variants)} "
                    f"→ {normal_value}"
                )

    else:

        report.append(
            "Inconsistent text: 0"
        )


    # ========================================================
    # ML ANOMALIES
    # ========================================================

    report.append(
        f"ML anomalies detected: "
        f"{len(anomalies)}"
    )

    report.append("")


    # ========================================================
    # QUALITY SCORE
    # ========================================================

    report.append(
        "DATA QUALITY SCORE"
    )

    report.append(
        "-" * 40
    )

    report.append(
        f"Before cleaning: "
        f"{before_score}/100"
    )

    report.append(
        f"After cleaning: "
        f"{after_score}/100"
    )


    improvement = round(
        after_score - before_score,
        2
    )


    report.append(
        f"Improvement: {improvement}"
    )

    report.append("")


    # ========================================================
    # AI RECOMMENDATIONS
    # ========================================================

    report.append(
        "AI CLEANING RECOMMENDATIONS"
    )

    report.append(
        "-" * 40
    )


    if not recommendations:

        report.append(
            "No recommendations generated."
        )

    else:

        for recommendation in recommendations:

            if not isinstance(
                recommendation,
                dict
            ):

                report.append(
                    f"- {recommendation}"
                )

                continue


            column = recommendation.get(
                "column",
                "Dataset"
            )

            problem = recommendation.get(
                "problem",
                "Unknown"
            )

            action = recommendation.get(
                "recommendation",
                "No recommendation"
            )

            reason = recommendation.get(
                "reason",
                "No reason provided"
            )


            report.append(
                f"Column: {column}"
            )

            report.append(
                f"Problem: {problem}"
            )

            report.append(
                f"Recommendation: {action}"
            )

            report.append(
                f"Reason: {reason}"
            )

            report.append("")


    # ========================================================
    # ML ANOMALIES
    # ========================================================

    report.append(
        "ML ANOMALY DETECTION"
    )

    report.append(
        "-" * 40
    )


    if anomalies.empty:

        report.append(
            "No anomalies detected."
        )

    else:

        report.append(
            f"{len(anomalies)} anomalous "
            "record(s) detected."
        )

        report.append(
            "Anomalies were flagged for review "
            "and were not automatically deleted."
        )

    report.append("")


    # ========================================================
    # CLEANING RESULT
    # ========================================================

    report.append(
        "CLEANING RESULT"
    )

    report.append(
        "-" * 40
    )


    rows_removed = (
        df.shape[0]
        - cleaned_df.shape[0]
    )


    report.append(
        f"Rows removed: {rows_removed}"
    )

    report.append(
        f"Remaining rows: "
        f"{cleaned_df.shape[0]}"
    )

    report.append("")


    report.append(
        "Report generated by "
        "AI Data Cleaning Assistant."
    )


    return "\n".join(
        report
    )