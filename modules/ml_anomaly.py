import pandas as pd

from sklearn.ensemble import IsolationForest


def detect_anomalies(df):

    # Select only numerical columns
    numeric_df = df.select_dtypes(
        include="number"
    ).copy()

    # If there are no numerical columns,
    # ML anomaly detection cannot be performed
    if numeric_df.empty:

        return pd.DataFrame()


    # Replace missing numerical values
    # temporarily using the median
    numeric_df = numeric_df.fillna(
        numeric_df.median()
    )


    # Create Isolation Forest model
    model = IsolationForest(
        contamination="auto",
        random_state=42
    )


    # Train model and predict anomalies
    predictions = model.fit_predict(
        numeric_df
    )


    # Add predictions to a copy of the dataset
    result = df.copy()

    result["anomaly"] = predictions


    # Keep only anomalous rows
    anomalies = result[
        result["anomaly"] == -1
    ]


    # Remove helper column
    anomalies = anomalies.drop(
        columns=["anomaly"]
    )


    return anomalies