# dagster-demo

Dagster + dbt demo project for trying out **Dagster Cloud Serverless (dbt)**.

## Project structure

```
dagster-demo/
├── dbt_project.yml          # dbt project config
├── profiles.yml             # local DuckDB profile
├── models/
│   ├── schema.yml           # sources & model tests
│   ├── daily_revenue.sql    # revenue aggregated by day
│   ├── product_summary.sql  # per-product metrics
│   └── customer_orders.sql  # customer-tier enrichment
├── seeds/
│   ├── raw_sales_orders.csv # 50 simulated orders
│   └── raw_customers.csv    # 8 customer records
├── dagster_demo/
│   └── definitions.py       # dbt → Dagster asset wrapping
└── pyproject.toml
```

## Quick start (local)

```bash
pip install dagster dagster-dbt dbt-duckdb
cd dagster-demo
dbt seed
dbt build
dagster dev
```

## Deploy to Dagster Cloud

1. Push this repo to GitHub.
2. In Dagster Cloud → **Deployments** → **Create a serverless deployment**.
3. Select **dbt** as project type, connect the repo, branch `main`.
4. Done — assets appear in the UI automatically.
