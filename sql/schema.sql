-- Subscription Revenue Analytics
-- Analytics Warehouse Schema

IF DB_ID('SRWarehouse') IS NULL
BEGIN
    CREATE DATABASE SRWarehouse;
END;
GO

USE SRWarehouse;
GO

-- Dimension Table: Users
CREATE TABLE dim_users
(
    user_id INT PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    signup_date DATE NOT NULL,
    signup_year INT NOT NULL,
    signup_month INT NOT NULL,
    country VARCHAR(100),
    industry VARCHAR(100),
    company_size VARCHAR(50),
    acquisition_channel VARCHAR(100),
    device_type VARCHAR(50)
);
GO

-- Dimension Table: Plans
CREATE TABLE dim_plans
(
    plan_id INT IDENTITY(1,1) PRIMARY KEY,
    plan_name VARCHAR(50) NOT NULL,
    billing_cycle VARCHAR(20) NOT NULL,
    monthly_price DECIMAL(10,2) NOT NULL
);
GO

-- Fact Table: Subscriptions
CREATE TABLE fact_subscriptions
(
    subscription_id INT PRIMARY KEY,

    user_id INT NOT NULL,
    plan_id INT NOT NULL,

    start_date DATE NOT NULL,
    end_date DATE NULL,

    subscription_status VARCHAR(20) NOT NULL,

    discount_pct DECIMAL(5,2) NOT NULL,
    final_monthly_price DECIMAL(10,2) NOT NULL,

    subscription_length_days INT,

    CONSTRAINT FK_fact_subscriptions_users
        FOREIGN KEY (user_id)
        REFERENCES dim_users(user_id),

    CONSTRAINT FK_fact_subscriptions_plans
        FOREIGN KEY (plan_id)
        REFERENCES dim_plans(plan_id)
);
GO


-- Fact Table: Payments
CREATE TABLE fact_payments
(
    payment_id INT PRIMARY KEY,

    subscription_id INT NOT NULL,

    payment_date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,

    payment_status VARCHAR(20) NOT NULL,

    refund_flag BIT NOT NULL,

    payment_month VARCHAR(7) NOT NULL,

    CONSTRAINT FK_fact_payments_subscriptions
        FOREIGN KEY (subscription_id)
        REFERENCES fact_subscriptions(subscription_id)
);
GO

-- Nonclustered Indexes

-- Foreign Keys
CREATE NONCLUSTERED INDEX IX_fact_subscriptions_user_id
ON fact_subscriptions(user_id);
GO

CREATE NONCLUSTERED INDEX IX_fact_subscriptions_plan_id
ON fact_subscriptions(plan_id);
GO

CREATE NONCLUSTERED INDEX IX_fact_payments_subscription_id
ON fact_payments(subscription_id);
GO

-- Frequently Filtered Dates
CREATE NONCLUSTERED INDEX IX_fact_subscriptions_start_date
ON fact_subscriptions(start_date);
GO

CREATE NONCLUSTERED INDEX IX_fact_payments_payment_date
ON fact_payments(payment_date);
GO



SELECT * FROM dim_plans;

SELECT COUNT(*) FROM fact_subscriptions;

SELECT TOP (10)
    subscription_id,
    user_id,
    plan_id,
    subscription_status
FROM fact_subscriptions;

SELECT COUNT(*) AS users
FROM dim_users;

SELECT COUNT(*) AS plans
FROM dim_plans;

SELECT COUNT(*) AS subscriptions
FROM fact_subscriptions;

SELECT COUNT(*) AS payments
FROM fact_payments;

SELECT TOP (10)
    p.payment_id,
    p.payment_date,
    p.amount,
    s.subscription_status,
    u.country,
    pl.plan_name,
    pl.billing_cycle
FROM fact_payments AS p
JOIN fact_subscriptions AS s
    ON p.subscription_id = s.subscription_id
JOIN dim_users AS u
    ON s.user_id = u.user_id
JOIN dim_plans AS pl
    ON s.plan_id = pl.plan_id;