# Subscription Revenue Intelligence Platform

An end-to-end Analytics Engineering project that simulates how a modern SaaS company transforms raw subscription data into business-ready insights using Python, SQL Server, and Tableau.

This project was built to mirror a real analytics workflow—from generating raw business data to building a dimensional data warehouse, writing analytical SQL, and creating executive dashboards for decision-makers.

---

## Business Scenario

The leadership team wants answers to questions like:

- How much recurring revenue are we generating?
- Which subscription plans perform the best?
- Which acquisition channels bring the highest-value customers?
- Which industries generate the most revenue?
- How many customers are churning?
- How is revenue changing month over month?

Instead of answering these manually, this project builds a complete analytics platform capable of answering them automatically.

---

# Tech Stack

| Category | Technology |
|-----------|------------|
| Language | Python |
| Data Processing | Pandas, NumPy |
| Data Generation | Faker |
| Database | SQL Server |
| Database Connectivity | SQLAlchemy, pyodbc |
| Analytics | Advanced SQL |
| BI & Visualization | Tableau |
| Version Control | Git & GitHub |

---

# Project Workflow

```
Raw Data
     │
     ▼
Dataset Generation
     │
     ▼
ETL Pipeline
     │
     ▼
Processed Data
     │
     ▼
SQL Server Data Warehouse
     │
     ▼
Analytical SQL
     │
     ▼
Reporting Views
     │
     ▼
Interactive Tableau Dashboards
```

---

# Repository Structure

```
subscription-revenue-analytics/

├── dashboards/
│   └── tableau/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│
├── scripts/
│   └── generate_dataset.py
│
├── sql/
│   ├── schema.sql
│   └── analysis_queries.sql
│
├── src/
│   ├── etl.py
│   ├── features.py
│   ├── load_to_sql.py
│   └── utils.py
│
├── README.md
└── requirements.txt
```

---

# Dataset

The project uses a synthetic SaaS subscription dataset generated with Python and Faker.

The generated data simulates realistic customer subscriptions, payments, pricing plans, acquisition channels, and engagement activity.

### Dataset Highlights

- 7,043 customers
- 150K+ payment records
- Multiple subscription plans
- Multiple countries
- Multiple industries
- Multiple acquisition channels
- Simulated subscription lifecycle

---

# Phase 1 — Dataset Generation

Built a modular dataset generation pipeline capable of producing realistic business data while ensuring reproducibility.

### Highlights

- Configuration-driven design
- Deterministic outputs using a fixed random seed
- Modular helper functions
- Built-in validation before saving data

---

# Phase 2 — ETL Pipeline

Developed a reusable ETL pipeline in Python using Pandas to prepare raw datasets for analytical workloads.

The pipeline performs:

- Data validation
- Data cleaning
- Standardization
- Missing value handling
- Duplicate removal
- Feature engineering
- Export of analytics-ready datasets

The ETL process is fully orchestrated through a single pipeline function.

---

# Phase 3 — Data Warehouse

Designed a Star Schema data warehouse in SQL Server to support analytical queries.

### Dimension Tables

- dim_users
- dim_plans

### Fact Tables

- fact_subscriptions
- fact_payments

### Implemented

- Primary & Foreign Keys
- Surrogate Keys
- Referential Integrity
- Nonclustered Indexes
- Automated warehouse loading

---

# Phase 4 — Advanced SQL Analytics

Implemented production-style SQL to generate business insights directly from the warehouse.

### SQL Concepts Used

- CTEs
- Window Functions
- CASE Expressions
- Conditional Aggregation
- Views
- Ranking Functions
- Cohort Analysis

### Business Metrics

- Monthly Recurring Revenue (MRR)
- Annual Recurring Revenue (ARR)
- Active Customers
- Churn Rate
- Retention Rate
- ARPU
- Customer Lifetime Value (LTV)
- Revenue Growth
- Revenue by Country
- Revenue by Acquisition Channel
- Plan Performance

To simplify reporting, reusable SQL views were created as a semantic layer for Tableau.

---

# Phase 5 — Tableau Dashboards

Built interactive dashboards connected directly to SQL Server.

### Executive Dashboard

- Revenue KPIs
- Monthly Revenue Trend
- Revenue by Plan
- Revenue by Country
- Revenue by Acquisition Channel

### Customer Dashboard

- Active Customers
- Churn Analysis
- Customer Segmentation
- Top Customers

### Revenue Dashboard

- Revenue Trends
- Industry Analysis
- Geographic Performance
- Plan Performance

Interactive filters allow users to explore metrics by month, country, plan, industry, and acquisition channel.

---

# Key Business Questions Answered

- How is monthly revenue changing over time?
- Which subscription plans generate the highest revenue?
- Which countries contribute the most revenue?
- Which acquisition channels deliver the highest-value customers?
- What is the current customer churn rate?
- How many active customers does the business have?
- Which industries are the most profitable?

---

# Skills Demonstrated

### Analytics Engineering

- ETL Development
- Data Warehousing
- Dimensional Modeling
- Star Schema Design
- Reporting Layer Development

### SQL

- Advanced SQL
- CTEs
- Window Functions
- Views
- Cohort Analysis
- Ranking Functions
- Business KPI Development

### Data Engineering

- Python
- Pandas
- SQLAlchemy
- SQL Server
- Data Validation
- Pipeline Automation

### Business Intelligence

- Tableau
- Interactive Dashboards
- Executive Reporting
- Dashboard Storytelling

---

# Dashboard Preview

### Executive Dashboard

<img width="595" height="497" alt="image" src="https://github.com/user-attachments/assets/e6092547-d8fa-43f4-9c27-a46c8d3642ee" />

### Customer Dashboard

<img width="600" height="500" alt="image" src="https://github.com/user-attachments/assets/eaeca9fb-56cf-4a7b-9c67-8cf1548efd29" />

### Revenue Dashboard

<img width="599" height="497" alt="image" src="https://github.com/user-attachments/assets/ef2031c3-4d44-44b8-9ef7-c4695bf1f016" />

---

# What I Learned

This project gave me hands-on experience in designing an end-to-end analytics workflow rather than solving isolated SQL problems. It strengthened my understanding of ETL pipelines, dimensional modeling, analytical SQL, and building dashboards that answer real business questions.

More importantly, it helped me understand how Analytics Engineers bridge the gap between raw operational data and business decision-making.

---

# Author

**Vihan Sharma**

B.Tech, Electronics & Communication Engineering  
IIIT Ranchi

- GitHub: https://github.com/Aecrix
- LinkedIn: *(Add your LinkedIn profile here)*
