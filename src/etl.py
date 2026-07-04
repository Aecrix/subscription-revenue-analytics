from pathlib import Path

import pandas as pd

import logging

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Extract
def load_raw_data() -> dict[str, pd.DataFrame]:
    """
    Load all raw datasets into memory.

    Returns:
        Dictionary mapping dataset name to DataFrame.
    """
    datasets = {
        "users": pd.read_csv(RAW_DATA_DIR / "users.csv"),
        "subscriptions": pd.read_csv(RAW_DATA_DIR / "subscriptions.csv"),
        "payments": pd.read_csv(RAW_DATA_DIR / "payments.csv"),
        "engagement_logs": pd.read_csv(RAW_DATA_DIR / "engagement_logs.csv"),
    }

    return datasets


# Validation
def validate_dataset(name: str, df: pd.DataFrame) -> None:
    """
    Perform basic validation checks on a dataset.
    Raises ValueError if validation fails.
    """

    if df.empty:
        raise ValueError(f"{name} dataset is empty.")

    if df.columns.duplicated().any():
        raise ValueError(f"{name} contains duplicate column names.")

    logger.info("%s passed validation.", name)


# Cleaning
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove leading/trailing whitespace from column names.
    """
    df = df.copy()
    df.columns = df.columns.str.strip()

    return df


# Standardization
DATE_COLUMNS = {
    "users": ["signup_date"],
    "subscriptions": ["start_date", "end_date"],
    "payments": ["payment_date"],
    "engagement_logs": ["event_time"],
}

MISSING_VALUE_RULES = {
    "users": {
        "industry": "Unknown",
        "company_size": "Unknown",
        "acquisition_channel": "Unknown",
        "device": "Unknown",
    },
    "subscriptions": {
        "discount_pct": 0,
    },
}


def standardize_dates(
    name: str,
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert date columns to datetime.
    """

    df = df.copy()

    for column in DATE_COLUMNS.get(name, []):
        df[column] = pd.to_datetime(df[column], errors="coerce")

    return df


# Missing Values
def handle_missing_values(
    name: str,
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Fill missing values according to predefined rules.
    """
    df = df.copy()

    rules = MISSING_VALUE_RULES.get(name, {})

    for column, value in rules.items():
        if column in df.columns:
            df[column] = df[column].fillna(value)

    return df


# Duplicate Removal
def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from a dataset.
    """
    df = df.copy()

    df = df.drop_duplicates()

    return df


# Feature Engineering
def engineer_features(
    name: str,
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create analytics-ready features.
    """
    df = df.copy()

    if name == "users":
        df["signup_year"] = df["signup_date"].dt.year
        df["signup_month"] = df["signup_date"].dt.month

    elif name == "subscriptions":
        df["subscription_length_days"] = (df["end_date"] - df["start_date"]).dt.days

    elif name == "payments":
        df["payment_month"] = df["payment_date"].dt.to_period("M").astype(str)

    elif name == "engagement_logs":
        df["event_date"] = df["event_time"].dt.date

    return df


# Persistence
def save_processed_dataset(
    name: str,
    df: pd.DataFrame,
) -> None:
    """
    Save a processed dataset to the processed data directory.
    """
    output_path = PROCESSED_DATA_DIR / f"{name}.csv"

    df.to_csv(output_path, index=False)

    logger.info("Saved %s", output_path.name)


# Pipeline
def run_etl() -> dict[str, pd.DataFrame]:
    """
    Execute the complete ETL pipeline.
    """
    datasets = load_raw_data()

    for name, df in datasets.items():
        logger.info("%s: %s", name, df.shape)

        validate_dataset(name, df)

        df = clean_column_names(df)
        df = standardize_dates(name, df)
        df = handle_missing_values(name, df)
        df = remove_duplicates(df)
        df = engineer_features(name, df)

        save_processed_dataset(name, df)

        datasets[name] = df

    return datasets


if __name__ == "__main__":
    datasets = run_etl()
