# Imports
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

SERVER = r"NEXUS-POINT\SQLEXPRESS"
DATABASE = "SRWarehouse"
DRIVER = "ODBC Driver 18 for SQL Server"

CONNECTION_STRING = (
    f"mssql+pyodbc://@{SERVER}/{DATABASE}"
    f"?driver={quote_plus(DRIVER)}"
    "&trusted_connection=yes"
    "&Encrypt=yes"
    "&TrustServerCertificate=yes"
)

engine = create_engine(CONNECTION_STRING)

# Clearing existing warehouse to prevent PK errors
def clear_warehouse():
    """Clear warehouse tables before loading fresh data."""

    with engine.begin() as conn:
        conn.execute(text("DELETE FROM fact_payments"))
        conn.execute(text("DELETE FROM fact_subscriptions"))
        conn.execute(text("DELETE FROM dim_plans"))
        conn.execute(text("DELETE FROM dim_users"))

    print("Warehouse tables cleared.")

#Loading Data
def load_processed_data():
    """Load all processed datasets into memory."""

    datasets = {
        "users": pd.read_csv(PROCESSED_DATA_DIR / "users.csv"),
        "subscriptions": pd.read_csv(PROCESSED_DATA_DIR / "subscriptions.csv"),
        "payments": pd.read_csv(PROCESSED_DATA_DIR / "payments.csv"),
        "engagement_logs": pd.read_csv(PROCESSED_DATA_DIR / "engagement_logs.csv"),
    }

    return datasets

# Populating dim_users Table
def load_dim_users(users_df):
    """Load the dim_users table."""

    print(users_df.columns.tolist())

    dim_users = users_df[
        [
            "user_id",
            "customer_id",
            "signup_date",
            "signup_year",
            "signup_month",
            "country",
            "industry",
            "company_size",
            "acquisition_channel",
            "device_type",
        ]
    ]

    dim_users.to_sql(
        name="dim_users",
        con=engine,
        if_exists="append",
        index=False,
    )

    print(f"Loaded {len(dim_users):,} rows into dim_users.")

# Populating dim_plans Table
def load_dim_plans(subscriptions_df):
    """Load the dim_plans table."""

    dim_plans = (
        subscriptions_df[
            [
                "plan_name",
                "billing_cycle",
                "monthly_price",
            ]
        ]
        .drop_duplicates()
        .sort_values(
            by=["plan_name", "billing_cycle"]
        )
        .reset_index(drop=True)
    )

    dim_plans.to_sql(
        name="dim_plans",
        con=engine,
        if_exists="append",
        index=False,
    )

    print(f"Loaded {len(dim_plans):,} rows into dim_plans.")

# Populating fact_subscription Table
def load_fact_subscriptions(subscriptions_df):
    """Load the fact_subscriptions table."""

    plan_lookup = pd.read_sql(
        """
        SELECT
            plan_id,
            plan_name,
            billing_cycle
        FROM dim_plans
        """,
        con=engine,
    )

    fact_subscriptions = subscriptions_df.merge(
        plan_lookup,
        on=["plan_name", "billing_cycle"],
        how="left",
        validate="many_to_one",
    )

    fact_subscriptions = fact_subscriptions[
        [
            "subscription_id",
            "user_id",
            "plan_id",
            "start_date",
            "end_date",
            "subscription_status",
            "discount_pct",
            "final_monthly_price",
            "subscription_length_days",
        ]
    ]

    if fact_subscriptions["plan_id"].isna().any():
        raise ValueError(
            "One or more subscriptions could not be matched to a plan."
        )

    fact_subscriptions.to_sql(
        name="fact_subscriptions",
        con=engine,
        if_exists="append",
        index=False,
    )

    print(f"Loaded {len(fact_subscriptions):,} rows into fact_subscriptions.")

# Populating fact_payments Table
def load_fact_payments(payments_df):
    """Load the fact_payments table."""

    fact_payments = payments_df[
        [
            "payment_id",
            "subscription_id",
            "payment_date",
            "amount",
            "payment_status",
            "refund_flag",
            "payment_month",
        ]
    ]

    fact_payments.to_sql(
        name="fact_payments",
        con=engine,
        if_exists="append",
        index=False,
    )

    print(f"Loaded {len(fact_payments):,} rows into fact_payments.")

# Running pipeline
def run_load_pipeline():
    """Run the complete warehouse loading pipeline."""

    with engine.connect() as conn:
        print("Successfully connected to SQL Server!")

    datasets = load_processed_data()

    clear_warehouse()

    load_dim_users(datasets["users"])
    load_dim_plans(datasets["subscriptions"])
    load_fact_subscriptions(datasets["subscriptions"])
    load_fact_payments(datasets["payments"])

    print("Warehouse loading completed successfully.")

if __name__ == "__main__":
    run_load_pipeline()