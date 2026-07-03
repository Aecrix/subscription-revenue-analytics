"""
Subscription Revenue Intelligence Platform
------------------------------------------
Dataset Generator

This script:
1. Loads the IBM Telco Customer Churn dataset.
2. Cleans and standardizes the raw data.
3. Generates relational SaaS datasets:
   - users.csv
   - subscriptions.csv
   - payments.csv
   - engagement_logs.csv
"""

# Imports
from pathlib import Path
import random

import numpy as np
import pandas as pd
from faker import Faker

from dateutil.relativedelta import relativedelta

# Configuration
RANDOM_SEED = 42

REFERENCE_DATE = pd.Timestamp("2025-12-31").normalize()
PAYMENT_HISTORY_START = pd.Timestamp("2024-01-01").normalize()

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

fake = Faker()
Faker.seed(RANDOM_SEED)

# Project Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

TELCO_DATA_PATH = RAW_DATA_DIR / "telco_customer_churn.csv"

COLUMN_MAPPING = {
    "customerID": "customer_id",
    "gender": "gender",
    "SeniorCitizen": "senior_citizen",
    "Partner": "partner",
    "Dependents": "dependents",
    "tenure": "tenure",
    "PhoneService": "phone_service",
    "MultipleLines": "multiple_lines",
    "InternetService": "internet_service",
    "OnlineSecurity": "online_security",
    "OnlineBackup": "online_backup",
    "DeviceProtection": "device_protection",
    "TechSupport": "tech_support",
    "StreamingTV": "streaming_tv",
    "StreamingMovies": "streaming_movies",
    "Contract": "contract",
    "PaperlessBilling": "paperless_billing",
    "PaymentMethod": "payment_method",
    "MonthlyCharges": "monthly_charges",
    "TotalCharges": "total_charges",
    "Churn": "churn",
}

COUNTRIES = [
    "United States",
    "Canada",
    "United Kingdom",
    "Germany",
    "India",
    "Australia",
]

INDUSTRIES = [
    "Technology",
    "Finance",
    "Healthcare",
    "Retail",
    "Education",
    "Manufacturing",
]

COMPANY_SIZES = ["Startup", "SMB", "Mid-Market", "Enterprise"]

ACQUISITION_CHANNELS = [
    "Organic Search",
    "Google Ads",
    "LinkedIn",
    "Referral",
    "Email Campaign",
    "Partner",
]

DEVICE_TYPES = ["Desktop", "Mobile", "Tablet"]

PLAN_MAPPING = {
    "Month-to-month": "Starter",
    "One year": "Pro",
    "Two year": "Enterprise",
}

PLAN_PRICING = {"Starter": 29, "Pro": 79, "Enterprise": 199}

BILLING_MAPPING = {
    "Month-to-month": "Monthly",
    "One year": "Annual",
    "Two year": "Annual",
}

DISCOUNT_OPTIONS = [0, 5, 10, 15]

DISCOUNT_PROBABILITIES = [0.70, 0.15, 0.10, 0.05]

PAYMENT_STATUS = ["Paid", "Failed", "Refunded"]

PAYMENT_STATUS_PROBABILITIES = [0.94, 0.04, 0.02]

EVENT_TYPES = [
    "Login",
    "Dashboard View",
    "Report Export",
    "Workflow Created",
    "Workflow Executed",
    "API Call",
    "Settings Update",
]

DEVICES = ["Desktop", "Mobile", "Tablet"]


# Load Dataset
def load_telco_data(file_path: Path) -> pd.DataFrame:
    """
    Load and standardize the IBM Telco Customer Churn dataset.

    Parameters
    ----------
    file_path : Path
        Path to the raw CSV file.

    Returns
    -------
    pd.DataFrame
        Cleaned dataframe.
    """

    print("Loading Telco dataset...")

    df = pd.read_csv(file_path)

    print(f"Dataset loaded successfully.")
    print(f"Rows    : {len(df)}")
    print(f"Columns : {len(df.columns)}")
    print()

    print("Renaming columns...")
    df.rename(columns=COLUMN_MAPPING, inplace=True)

    print("Converting total_charges to numeric...")
    df["total_charges"] = pd.to_numeric(df["total_charges"], errors="coerce")

    missing_values = df.isna().sum().sum()
    print(f"Missing values detected: {missing_values}")
    print()

    return df


# Generate Users
def generate_users(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate the users dimension table.
    """

    print("Generating users table...")

    reference_date = REFERENCE_DATE

    users = pd.DataFrame()

    users["user_id"] = np.arange(1, len(df) + 1)

    users["customer_id"] = df["customer_id"]

    users["gender"] = df["gender"]

    users["senior_citizen"] = df["senior_citizen"]

    users["partner"] = df["partner"]

    users["dependents"] = df["dependents"]

    users["signup_date"] = REFERENCE_DATE - pd.to_timedelta(df["tenure"] * 30, unit="D")

    users["country"] = np.random.choice(
        COUNTRIES, len(users), p=[0.45, 0.10, 0.10, 0.10, 0.15, 0.10]
    )

    users["industry"] = np.random.choice(INDUSTRIES, len(users))

    users["company_size"] = np.random.choice(
        COMPANY_SIZES, len(users), p=[0.35, 0.35, 0.20, 0.10]
    )

    users["acquisition_channel"] = np.random.choice(ACQUISITION_CHANNELS, len(users))

    users["device_type"] = np.random.choice(
        DEVICE_TYPES, len(users), p=[0.55, 0.35, 0.10]
    )

    return users


# Helper Function
def add_months(start_date, months):
    """
    Add calendar months to a date.

    Parameters
    ----------
    start_date : pd.Timestamp
        Subscription start date.

    months : int
        Number of months to add.

    Returns
    -------
    pd.Timestamp
        Date after adding the specified number of calendar months.
    """
    return start_date + pd.DateOffset(months=int(months))


# Generate Subscription table
def generate_subscriptions(users: pd.DataFrame, telco: pd.DataFrame) -> pd.DataFrame:
    """
    Generate the subscriptions table.
    """

    print("Generating subscriptions table...")

    subscriptions = pd.DataFrame()

    subscriptions["subscription_id"] = np.arange(100001, 100001 + len(users))

    subscriptions["user_id"] = users["user_id"]

    subscriptions["plan_name"] = telco["contract"].map(PLAN_MAPPING)

    subscriptions["billing_cycle"] = telco["contract"].map(BILLING_MAPPING)

    subscriptions["subscription_status"] = np.where(
        telco["churn"] == "Yes", "Cancelled", "Active"
    )

    subscriptions["start_date"] = users["signup_date"]

    subscriptions["end_date"] = np.where(
        subscriptions["subscription_status"] == "Cancelled",
        [
            add_months(start_date, tenure)
            for start_date, tenure in zip(users["signup_date"], telco["tenure"])
        ],
        pd.NaT,
    )

    subscriptions["monthly_price"] = subscriptions["plan_name"].map(PLAN_PRICING)

    subscriptions["discount_pct"] = np.random.choice(
        DISCOUNT_OPTIONS, size=len(users), p=DISCOUNT_PROBABILITIES
    )

    subscriptions["final_monthly_price"] = (
        subscriptions["monthly_price"] * (1 - subscriptions["discount_pct"] / 100)
    ).round(2)

    return subscriptions


# Generating Payment Schedule
def generate_payment_schedule(subscription: pd.Series) -> list[pd.Timestamp]:
    """
    Generate invoice dates for a single subscription.
    """

    invoice_dates = []

    current_date = max(subscription["start_date"], PAYMENT_HISTORY_START)

    final_date = (
        REFERENCE_DATE
        if pd.isna(subscription["end_date"])
        else min(subscription["end_date"], REFERENCE_DATE)
    )

    interval = (
        relativedelta(months=1)
        if subscription["billing_cycle"] == "Monthly"
        else relativedelta(years=1)
    )

    while current_date <= final_date:
        invoice_dates.append(current_date)
        current_date += interval

    return invoice_dates


# Generating Payments
def generate_payments(subscriptions: pd.DataFrame) -> pd.DataFrame:
    """
    Generate payment history for all subscriptions.
    """

    print("Generating payments table...")

    payments = []

    payment_id = 500001

    for _, subscription in subscriptions.iterrows():

        invoice_dates = generate_payment_schedule(subscription)

        for invoice_date in invoice_dates:

            status = np.random.choice(PAYMENT_STATUS, p=PAYMENT_STATUS_PROBABILITIES)

            payments.append(
                {
                    "payment_id": payment_id,
                    "subscription_id": subscription["subscription_id"],
                    "payment_date": invoice_date,
                    "amount": subscription["final_monthly_price"],
                    "payment_status": status,
                    "refund_flag": status == "Refunded",
                }
            )

            payment_id += 1

    return pd.DataFrame(payments)


# Generating Engagement Logs
def generate_engagement_logs(users: pd.DataFrame) -> pd.DataFrame:
    """
    Generate engagement events.
    """

    print("Generating engagement logs...")

    logs = []

    event_id = 900001

    for _, user in users.iterrows():

        n_events = np.random.randint(15, 40)

        for _ in range(n_events):

            logs.append(
                {
                    "event_id": event_id,
                    "user_id": user["user_id"],
                    "event_time": fake.date_time_between(
                        start_date=PAYMENT_HISTORY_START.to_pydatetime(),
                        end_date=REFERENCE_DATE.to_pydatetime(),
                    ),
                    "event_type": np.random.choice(EVENT_TYPES),
                    "session_duration": max(1, int(np.random.normal(18, 6))),
                    "device": np.random.choice(DEVICES, p=[0.55, 0.35, 0.10]),
                }
            )

            event_id += 1

    return pd.DataFrame(logs)


# Validating User Table
def validate_users(users: pd.DataFrame) -> None:
    """
    Validate the generated users dataset.
    Raises an exception if a critical validation fails.
    """

    print("\nValidating users table...")

    # Check row count
    assert len(users) > 0, "Users table is empty."

    # Check primary key
    assert users["user_id"].is_unique, "Duplicate user_id values found."

    # Null checks
    required_columns = ["user_id", "customer_id", "signup_date"]

    for column in required_columns:

        assert users[column].isna().sum() == 0, f"Null values found in {column}"

    # Duplicate customer ids
    assert users["customer_id"].is_unique, "Duplicate customer_id values found."

    print("Users table validation passed.\n")


# Validating Subscription table
def validate_subscriptions(subscriptions: pd.DataFrame) -> None:

    print("Validating subscriptions table...")

    assert subscriptions["subscription_id"].is_unique

    assert subscriptions["user_id"].is_unique

    assert subscriptions["monthly_price"].min() > 0

    assert (
        subscriptions["final_monthly_price"] <= subscriptions["monthly_price"]
    ).all()

    print("Subscriptions validation passed.\n")


# Adding imperfections in user table (to make the dataset more realistic)
def inject_user_noise(users: pd.DataFrame) -> pd.DataFrame:
    """
    Introduce realistic missing values.
    """

    print("Injecting realistic data imperfections...")

    users = users.copy()

    acquisition_mask = np.random.rand(len(users)) < 0.05

    users.loc[acquisition_mask, "acquisition_channel"] = np.nan

    device_mask = np.random.rand(len(users)) < 0.03

    users.loc[device_mask, "device_type"] = np.nan

    return users


# Validating Payments
def validate_payments(payments: pd.DataFrame) -> None:

    print("Validating payments table...")

    assert payments["payment_id"].is_unique

    assert payments["subscription_id"].notna().all()

    assert (payments["amount"] > 0).all()

    print("Payments validation passed.\n")


# Validating Engagement Logs
def validate_engagement_logs(logs: pd.DataFrame) -> None:

    print("Validating engagement logs...")

    assert logs["event_id"].is_unique

    assert logs["user_id"].notna().all()

    assert (logs["session_duration"] > 0).all()

    print("Engagement logs validation passed.\n")


# Save dataset
def save_dataframe(df: pd.DataFrame, filename: str) -> None:
    """
    Save dataframe to the raw data directory.
    """

    output_path = RAW_DATA_DIR / filename

    df.to_csv(output_path, index=False)

    print(f"Saved -> {filename}")


# Main Function
def main():

    print("=" * 60)
    print("Subscription Revenue Intelligence Platform")
    print("=" * 60)
    print()

    df = load_telco_data(TELCO_DATA_PATH)

    users = generate_users(df)
    validate_users(users)
    users = inject_user_noise(users)
    save_dataframe(users, "users.csv")

    subscriptions = generate_subscriptions(users, df)
    validate_subscriptions(subscriptions)
    save_dataframe(subscriptions, "subscriptions.csv")

    payments = generate_payments(subscriptions)
    validate_payments(payments)
    save_dataframe(payments, "payments.csv")

    logs = generate_engagement_logs(users)
    validate_engagement_logs(logs)
    save_dataframe(logs, "engagement_logs.csv")

    print()
    print("=" * 60)
    print("Dataset generation completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
