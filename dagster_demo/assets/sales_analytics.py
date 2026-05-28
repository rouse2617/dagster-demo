import json
import random
from datetime import datetime, timedelta

from dagster import AssetKey, AssetOut, asset, multi_asset


@asset(
    group_name="raw_data",
    description="Simulated raw sales orders ingested from an external system.",
)
def raw_sales_orders() -> list[dict]:
    """Ingest raw sales order data (simulates an API / DB extract)."""
    records = []
    for i in range(50):
        records.append(
            {
                "order_id": f"ORD-{1000+i}",
                "product": random.choice(["Widget A", "Widget B", "Gadget C"]),
                "quantity": random.randint(1, 10),
                "unit_price": round(random.uniform(5.0, 100.0), 2),
                "timestamp": (
                    datetime.now() - timedelta(days=random.randint(0, 30))
                ).isoformat(),
            }
        )
    return records


@asset(
    group_name="raw_data",
    description="Simulated customer metadata.",
)
def raw_customers() -> list[dict]:
    """Customer dimension table."""
    return [
        {"customer_id": "C001", "name": "Alice", "tier": "gold"},
        {"customer_id": "C002", "name": "Bob", "tier": "silver"},
        {"customer_id": "C003", "name": "Charlie", "tier": "gold"},
        {"customer_id": "C004", "name": "Diana", "tier": "bronze"},
    ]


@multi_asset(
    group_name="analytics",
    outs={
        "daily_revenue": AssetOut(
            key=AssetKey("daily_revenue"),
            description="Aggregated revenue per day.",
        ),
        "product_summary": AssetOut(
            key=AssetKey("product_summary"),
            description="Per-product total revenue, orders, and avg unit price.",
        ),
    },
    deps=[AssetKey("raw_sales_orders"), AssetKey("raw_customers")],
)
def analytics_models(raw_sales_orders: list[dict], raw_customers: list[dict]) -> tuple:
    """Compute daily revenue and product summaries from raw data."""
    # ── daily revenue ──────────────────────────────────────────────
    daily: dict[str, float] = {}
    for row in raw_sales_orders:
        day = row["timestamp"][:10]
        revenue = row["quantity"] * row["unit_price"]
        daily[day] = daily.get(day, 0.0) + revenue

    daily_revenue = [{"date": d, "revenue": round(r, 2)} for d, r in sorted(daily.items())]

    # ── product summary ────────────────────────────────────────────
    prod: dict[str, dict] = {}
    for row in raw_sales_orders:
        p = row["product"]
        rev = row["quantity"] * row["unit_price"]
        if p not in prod:
            prod[p] = {"orders": 0, "total_revenue": 0.0, "total_qty": 0}
        prod[p]["orders"] += 1
        prod[p]["total_revenue"] += rev
        prod[p]["total_qty"] += row["quantity"]

    product_summary = [
        {
            "product": p,
            "total_revenue": round(v["total_revenue"], 2),
            "total_orders": v["orders"],
            "total_quantity": v["total_qty"],
            "avg_unit_price": round(v["total_revenue"] / v["total_qty"], 2),
        }
        for p, v in sorted(prod.items())
    ]

    return daily_revenue, product_summary


@asset(
    group_name="reports",
    description="A final JSON report blob served to a BI dashboard.",
    deps=[AssetKey("daily_revenue"), AssetKey("product_summary")],
)
def bi_report(context) -> str:
    """Render a final report combining daily revenue and product summary."""
    report = {
        "generated_at": datetime.now().isoformat(),
        "title": "Sales Analytics Report",
        "daily_revenue": len(context.assets.daily_revenue),
        "product_summary": len(context.assets.product_summary),
    }
    return json.dumps(report, indent=2)
