# dagster-demo

A simple Dagster project for trying out **Dagster Cloud Serverless**.

## Quick start (local)

```bash
pip install dagster
dagster dev -f dagster_demo/definitions.py
```

## Assets

| Asset | Description |
|---|---|
| `raw_sales_orders` | Simulated raw order data |
| `raw_customers` | Customer dimension table |
| `daily_revenue` | Aggregated revenue per day |
| `product_summary` | Per-product metrics |
| `bi_report` | Final JSON report for dashboard |

## Deploy to Dagster Cloud

1. Push this repo to GitHub.
2. In Dagster Cloud → **Deployments** → **Create a serverless deployment**.
3. Select GitHub and connect the repo.
4. Done — assets appear in the UI automatically.
