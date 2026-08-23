import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from modules.analysis import (
    analyze_dataset,
    validate_dataset
)

from modules.cleaning import (
    clean_dataset
)

from modules.ai_recommendations import (
    generate_recommendations
)

from modules.ml_anomaly import (
    detect_anomalies
)

from modules.quality_score import (
    calculate_quality_score
)

from modules.report import (
    generate_quality_report
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Data Cleaning Assistant",
    page_icon="🧹",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title(
    "🧹 AI Data Cleaning Assistant"
)

st.write(
    "Clean, analyze and improve your datasets."
)

st.write(
    "Upload a CSV file to detect missing values, "
    "duplicates, data-type issues and potential outliers."
)


# ============================================================
# FILE UPLOADER
# ============================================================

uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)


# ============================================================
# MAIN APPLICATION
# ============================================================

if uploaded_file is not None:

    # ========================================================
    # READ CSV
    # ========================================================

    try:

        df = pd.read_csv(
            uploaded_file
        )

    except Exception as e:

        st.error(
            f"❌ Could not read the CSV file: {e}"
        )

        st.stop()


    # ========================================================
    # CHECK EMPTY DATASET
    # ========================================================

    if df.empty:

        st.warning(
            "⚠️ The uploaded CSV file is empty."
        )

        st.stop()


    # ========================================================
    # DATASET PREVIEW
    # ========================================================

    st.header(
        "📊 Dataset Preview"
    )

    st.dataframe(
        df,
        use_container_width=True
    )


    # ========================================================
    # DATASET INFORMATION
    # ========================================================

    st.header(
        "📋 Dataset Information"
    )

    info_col1, info_col2, info_col3, info_col4 = (
        st.columns(4)
    )


    with info_col1:

        st.metric(
            "Rows",
            df.shape[0]
        )


    with info_col2:

        st.metric(
            "Columns",
            df.shape[1]
        )


    with info_col3:

        st.metric(
            "Missing Values",
            int(
                df.isnull().sum().sum()
            )
        )


    with info_col4:

        st.metric(
            "Duplicate Rows",
            int(
                df.duplicated().sum()
            )
        )


    # ========================================================
    # ANALYZE DATASET
    # ========================================================

    try:

        results = analyze_dataset(
            df
        )

    except Exception as e:

        st.error(
            f"❌ Could not analyze the dataset: {e}"
        )

        st.stop()


    # ========================================================
    # VALIDATE DATASET
    # ========================================================

    try:

        validation_result = validate_dataset(
            df
        )

    except Exception:

        validation_result = []


    # ========================================================
    # VALIDATION MESSAGES
    # ========================================================

    if validation_result:

        st.warning(
            "⚠️ Dataset validation issues detected."
        )

        for error in validation_result:

            st.write(
                f"• {error}"
            )


    # ========================================================
    # DATA TYPES
    # ========================================================

    st.subheader(
        "🔤 Data Types"
    )

    data_types = df.dtypes.astype(str)

    st.dataframe(
        data_types.rename(
            "Data Type"
        )
    )


    # ========================================================
    # MISSING VALUES
    # ========================================================

    st.subheader(
        "⚠️ Missing Values"
    )

    missing_values = df.isnull().sum()

    st.dataframe(
        missing_values.rename(
            "Missing Values"
        )
    )


    # ========================================================
    # DUPLICATES
    # ========================================================

    st.subheader(
        "🔁 Duplicate Rows"
    )

    duplicate_count = int(
        df.duplicated().sum()
    )


    if duplicate_count > 0:

        st.warning(
            f"⚠️ {duplicate_count} duplicate "
            f"row(s) found."
        )

    else:

        st.success(
            "✅ No duplicate rows found."
        )


    # ========================================================
    # INVALID DATA TYPE ISSUES
    # ========================================================

    st.subheader(
        "🔢 Data Type Issues"
    )

    data_type_issues = results.get(
        "data_type_issues",
        {}
    )


    if data_type_issues:

        st.warning(
            "⚠️ Non-numeric values were detected "
            "in numerical fields."
        )

        for column, values in data_type_issues.items():

            st.write(
                f"**{column}:** {values}"
            )

    else:

        st.success(
            "✅ No obvious numerical data-type issues found."
        )


    # ========================================================
    # INCONSISTENT TEXT
    # ========================================================

    st.subheader(
        "🔤 Text Consistency"
    )

    inconsistent_text = results.get(
        "inconsistent_text",
        {}
    )


    if inconsistent_text:

        st.warning(
            "⚠️ Inconsistent text formatting detected."
        )

        for column, issues in inconsistent_text.items():

            st.write(
                f"**Column: {column}**"
            )

            for normal_value, variants in issues.items():

                st.write(
                    f"• {variants} → "
                    f"standard form: {normal_value}"
                )

    else:

        st.success(
            "✅ No obvious inconsistent text detected."
        )


    # ========================================================
    # PHASE 16
    # VISUAL DATA ANALYSIS
    # ========================================================

    st.header(
        "📊 Visual Data Analysis"
    )

    st.write(
        "Charts below help visualize data quality "
        "and numerical distributions."
    )


    # ========================================================
    # MISSING VALUES CHART
    # ========================================================

    st.subheader(
        "📊 Missing Values Chart"
    )

    missing_data = df.isnull().sum()

    missing_data = missing_data[
        missing_data > 0
    ]


    if missing_data.empty:

        st.success(
            "✅ No missing values found."
        )

    else:

        fig, ax = plt.subplots()

        missing_data.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title(
            "Missing Values by Column"
        )

        ax.set_xlabel(
            "Columns"
        )

        ax.set_ylabel(
            "Number of Missing Values"
        )

        plt.xticks(
            rotation=45
        )

        plt.tight_layout()

        st.pyplot(
            fig
        )

        plt.close(
            fig
        )


    # ========================================================
    # NUMERICAL DISTRIBUTIONS
    # ========================================================

    st.subheader(
        "📈 Numerical Distributions"
    )

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns


    if len(numeric_columns) == 0:

        st.info(
            "ℹ️ No numerical columns were found."
        )

    else:

        tabs = st.tabs(
            [
                str(column)
                for column in numeric_columns
            ]
        )


        for tab, column in zip(
            tabs,
            numeric_columns
        ):

            with tab:

                numeric_data = df[
                    column
                ].dropna()


                if numeric_data.empty:

                    st.info(
                        f"No usable numerical data "
                        f"found in {column}."
                    )

                    continue


                fig, ax = plt.subplots()

                ax.hist(
                    numeric_data,
                    bins=10
                )

                ax.set_title(
                    f"Distribution of {column}"
                )

                ax.set_xlabel(
                    column
                )

                ax.set_ylabel(
                    "Frequency"
                )

                ax.grid(
                    axis="y",
                    alpha=0.3
                )

                plt.tight_layout()

                st.pyplot(
                    fig
                )

                plt.close(
                    fig
                )


    # ========================================================
    # PHASE 17
    # AI CLEANING RECOMMENDATIONS
    # ========================================================

    st.header(
        "🤖 AI Cleaning Recommendations"
    )


    try:

        recommendations = (
            generate_recommendations(
                df
            )
        )

    except Exception as e:

        recommendations = []

        st.warning(
            f"⚠️ AI recommendations could not "
            f"be generated: {e}"
        )


    if not recommendations:

        st.success(
            "✅ No major cleaning recommendations "
            "were generated."
        )

    else:

        for recommendation in recommendations:

            # Handle dictionary recommendations
            if isinstance(
                recommendation,
                dict
            ):

                with st.container(
                    border=True
                ):

                    st.markdown(
                        "### 📌 "
                        + str(
                            recommendation.get(
                                "column",
                                "Dataset"
                            )
                        )
                    )

                    st.write(
                        "**Problem:** "
                        + str(
                            recommendation.get(
                                "problem",
                                "Unknown"
                            )
                        )
                    )

                    st.write(
                        "**🤖 Recommendation:** "
                        + str(
                            recommendation.get(
                                "recommendation",
                                "No recommendation"
                            )
                        )
                    )

                    st.write(
                        "**💡 Reason:** "
                        + str(
                            recommendation.get(
                                "reason",
                                "No reason provided"
                            )
                        )
                    )

            else:

                st.write(
                    f"• {recommendation}"
                )


    # ========================================================
    # PHASE 18
    # ML ANOMALY DETECTION
    # ========================================================

    st.header(
        "🤖 ML Anomaly Detection"
    )


    try:

        anomalies = detect_anomalies(
            df
        )

    except Exception as e:

        anomalies = pd.DataFrame()

        st.warning(
            f"⚠️ ML anomaly detection could "
            f"not be performed: {e}"
        )


    if anomalies.empty:

        st.success(
            "✅ No unusual records were detected."
        )

    else:

        st.warning(
            f"⚠️ {len(anomalies)} unusual "
            f"record(s) detected."
        )

        st.write(
            "These records have been flagged "
            "for review. They have NOT been "
            "automatically deleted."
        )

        st.dataframe(
            anomalies,
            use_container_width=True
        )


    # ========================================================
    # PHASE 19
    # DATA QUALITY SCORE
    # ========================================================

    st.header(
        "📊 Data Quality Score"
    )


    # ========================================================
    # INVALID DATA COUNT
    # ========================================================

    invalid_count = 0


    invalid_marks = results.get(
        "invalid_marks",
        []
    )


    invalid_age = results.get(
        "invalid_age",
        []
    )


    try:

        invalid_marks_count = len(
            invalid_marks
        )

    except TypeError:

        invalid_marks_count = 0


    try:

        invalid_age_count = len(
            invalid_age
        )

    except TypeError:

        invalid_age_count = 0


    # Avoid double counting rows that could
    # appear in both categories
    invalid_count = max(
        invalid_marks_count,
        invalid_age_count
    )


    # ========================================================
    # OUTLIER COUNT
    # ========================================================

    outlier_count = 0

    outliers = results.get(
        "outliers",
        {}
    )


    if isinstance(
        outliers,
        dict
    ):

        for column, values in outliers.items():

            try:

                outlier_count += len(
                    values
                )

            except TypeError:

                pass


    elif isinstance(
        outliers,
        (list, tuple, set)
    ):

        outlier_count = len(
            outliers
        )


    # ========================================================
    # INCONSISTENT TEXT COUNT
    # ========================================================

    inconsistent_count = 0


    if isinstance(
        inconsistent_text,
        dict
    ):

        for column, issues in inconsistent_text.items():

            if isinstance(
                issues,
                dict
            ):

                for normal_value, variants in issues.items():

                    try:

                        # Count extra variants rather
                        # than counting the standard form
                        inconsistent_count += max(
                            0,
                            len(variants) - 1
                        )

                    except TypeError:

                        pass


    # ========================================================
    # BEFORE CLEANING QUALITY SCORE
    # ========================================================

    try:

        before_quality_score = (
            calculate_quality_score(
                df,
                outlier_count=outlier_count,
                invalid_count=invalid_count,
                inconsistent_count=inconsistent_count
            )
        )

    except Exception as e:

        st.error(
            f"❌ Could not calculate "
            f"quality score: {e}"
        )

        before_quality_score = 0


    # ========================================================
    # DISPLAY BEFORE SCORE
    # ========================================================

    score_col1, score_col2, score_col3 = (
        st.columns(3)
    )


    with score_col1:

        st.metric(
            "Before Cleaning",
            f"{before_quality_score}/100"
        )


    with score_col2:

        st.metric(
            "Missing Values",
            int(
                df.isnull().sum().sum()
            )
        )


    with score_col3:

        st.metric(
            "Duplicate Rows",
            duplicate_count
        )


    # ========================================================
    # CLEAN DATASET
    # ========================================================

    st.header(
        "🧹 Clean Dataset"
    )


    clean_button = st.button(
        "🧹 Clean Dataset",
        type="primary"
    )


    # ========================================================
    # CLEANING PROCESS
    # ========================================================

    if clean_button:

        # ====================================================
        # CLEAN DATASET
        # ====================================================

        try:

            cleaned_df = clean_dataset(
                df
            )

        except Exception as e:

            st.error(
                f"❌ Could not clean the dataset: {e}"
            )

            st.stop()


        # ====================================================
        # CHECK CLEANING RESULT
        # ====================================================

        if cleaned_df is None:

            st.error(
                "❌ The cleaning function did not "
                "return a dataset."
            )

            st.stop()


        # ====================================================
        # RE-ANALYZE CLEANED DATASET
        # ====================================================

        try:

            cleaned_results = analyze_dataset(
                cleaned_df
            )

        except Exception as e:

            st.error(
                f"❌ Could not analyze the cleaned "
                f"dataset: {e}"
            )

            st.stop()


        # ====================================================
        # CLEANED OUTLIER COUNT
        # ====================================================

        cleaned_outlier_count = 0


        cleaned_outliers = cleaned_results.get(
            "outliers",
            {}
        )


        if isinstance(
            cleaned_outliers,
            dict
        ):

            for column, values in cleaned_outliers.items():

                try:

                    cleaned_outlier_count += len(
                        values
                    )

                except TypeError:

                    pass


        # ====================================================
        # CLEANED INVALID DATA COUNT
        # ====================================================

        cleaned_invalid_marks = (
            cleaned_results.get(
                "invalid_marks",
                []
            )
        )

        cleaned_invalid_age = (
            cleaned_results.get(
                "invalid_age",
                []
            )
        )


        try:

            cleaned_invalid_marks_count = len(
                cleaned_invalid_marks
            )

        except TypeError:

            cleaned_invalid_marks_count = 0


        try:

            cleaned_invalid_age_count = len(
                cleaned_invalid_age
            )

        except TypeError:

            cleaned_invalid_age_count = 0


        cleaned_invalid_count = max(
            cleaned_invalid_marks_count,
            cleaned_invalid_age_count
        )


        # ====================================================
        # CLEANED INCONSISTENT TEXT COUNT
        # ====================================================

        cleaned_inconsistent_count = 0


        cleaned_inconsistent = (
            cleaned_results.get(
                "inconsistent_text",
                {}
            )
        )


        if isinstance(
            cleaned_inconsistent,
            dict
        ):

            for column, issues in (
                cleaned_inconsistent.items()
            ):

                if isinstance(
                    issues,
                    dict
                ):

                    for normal_value, variants in (
                        issues.items()
                    ):

                        try:

                            cleaned_inconsistent_count += max(
                                0,
                                len(variants) - 1
                            )

                        except TypeError:

                            pass


        # ====================================================
        # AFTER CLEANING QUALITY SCORE
        # ====================================================

        try:

            after_quality_score = (
                calculate_quality_score(
                    cleaned_df,
                    outlier_count=cleaned_outlier_count,
                    invalid_count=cleaned_invalid_count,
                    inconsistent_count=(
                        cleaned_inconsistent_count
                    )
                )
            )

        except Exception as e:

            st.error(
                f"❌ Could not calculate "
                f"after-cleaning score: {e}"
            )

            after_quality_score = 0


        # ====================================================
        # QUALITY IMPROVEMENT
        # ====================================================

        st.subheader(
            "📊 Data Quality Improvement"
        )


        quality_col1, quality_col2 = (
            st.columns(2)
        )


        with quality_col1:

            st.metric(
                "Before Cleaning",
                f"{before_quality_score}/100"
            )


        with quality_col2:

            improvement = round(
                after_quality_score
                - before_quality_score,
                2
            )


            st.metric(
                "After Cleaning",
                f"{after_quality_score}/100",
                delta=improvement
            )


        # ====================================================
        # SUCCESS MESSAGE
        # ====================================================

        st.success(
            "🎉 Dataset cleaned successfully!"
        )


        # ====================================================
        # BEFORE VS AFTER ROWS
        # ====================================================

        st.subheader(
            "📈 Before vs After Cleaning"
        )


        before_rows = df.shape[0]

        after_rows = cleaned_df.shape[0]

        rows_removed = (
            before_rows - after_rows
        )


        row_col1, row_col2 = (
            st.columns(2)
        )


        with row_col1:

            st.metric(
                "Rows Before",
                before_rows
            )


        with row_col2:

            st.metric(
                "Rows After",
                after_rows,
                delta=after_rows - before_rows
            )


        # ====================================================
        # CLEANING SUMMARY
        # ====================================================

        st.subheader(
            "📝 Cleaning Summary"
        )


        missing_before = int(
            df.isnull().sum().sum()
        )

        missing_after = int(
            cleaned_df.isnull().sum().sum()
        )


        duplicate_before = int(
            df.duplicated().sum()
        )

        duplicate_after = int(
            cleaned_df.duplicated().sum()
        )


        summary_col1, summary_col2, summary_col3 = (
            st.columns(3)
        )


        with summary_col1:

            st.metric(
                "Missing Values",
                missing_after,
                delta=(
                    missing_after
                    - missing_before
                )
            )


        with summary_col2:

            st.metric(
                "Duplicate Rows",
                duplicate_after,
                delta=(
                    duplicate_after
                    - duplicate_before
                )
            )


        with summary_col3:

            st.metric(
                "Rows Removed",
                rows_removed
            )


        # ====================================================
        # CLEANED DATASET
        # ====================================================

        st.subheader(
            "✨ Cleaned Dataset"
        )


        st.dataframe(
            cleaned_df,
            use_container_width=True
        )


        # ====================================================
        # PHASE 20
        # GENERATE QUALITY REPORT
        # ====================================================

        try:

            quality_report = (
                generate_quality_report(
                    df=df,
                    cleaned_df=cleaned_df,
                    before_score=before_quality_score,
                    after_score=after_quality_score,
                    recommendations=recommendations,
                    anomalies=anomalies
                )
            )

        except Exception as e:

            quality_report = ""

            st.error(
                f"❌ Could not generate "
                f"quality report: {e}"
            )


        # ====================================================
        # DOWNLOAD SECTION
        # ====================================================

        st.header(
            "📥 Downloads"
        )


        # ====================================================
        # DOWNLOAD CLEANED CSV
        # ====================================================

        st.subheader(
            "📥 Download Cleaned Dataset"
        )


        cleaned_csv = (
            cleaned_df
            .to_csv(
                index=False
            )
            .encode(
                "utf-8"
            )
        )


        st.download_button(
            label="📥 Download Cleaned CSV",
            data=cleaned_csv,
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )


        # ====================================================
        # QUALITY REPORT
        # ====================================================

        st.subheader(
            "📄 Quality Report"
        )


        if quality_report:

            with st.expander(
                "👁️ View Quality Report"
            ):

                st.text(
                    quality_report
                )


            report_bytes = (
                quality_report
                .encode(
                    "utf-8"
                )
            )


            st.download_button(
                label="📄 Download Quality Report",
                data=report_bytes,
                file_name="data_quality_report.txt",
                mime="text/plain"
            )

        else:

            st.warning(
                "⚠️ Quality report could not "
                "be generated."
            )