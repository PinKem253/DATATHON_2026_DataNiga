import pandas as pd
from sklearn.preprocessing import StandardScaler


def preprocess_sales_data(df, train=True):
    """
    Preprocess sales data: convert Date to datetime, create time-based features.
    For train, include Revenue and COGS.
    For test, only Date.
    """
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    # Create time features
    df["days_since_start"] = (df["Date"] - df["Date"].min()).dt.days
    df["day_of_week"] = df["Date"].dt.dayofweek
    df["month"] = df["Date"].dt.month
    df["year"] = df["Date"].dt.year

    if train:
        # For training, we have Revenue and COGS
        # But for baseline, we might not need scaling yet
        pass
    else:
        # For test, remove Revenue and COGS if present (in sample_submission they are placeholders)
        if "Revenue" in df.columns:
            df = df.drop(["Revenue", "COGS"], axis=1)

    return df
