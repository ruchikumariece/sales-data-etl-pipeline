"""
Sales Data ETL Pipeline
Extract -> Clean/Transform -> Validate -> Load (SQLite) -> Export for Power BI
"""
import sqlite3
from pathlib import Path

import pandas as pd

RAW = Path("data/raw/sales_raw.csv")
CLEAN = Path("data/clean/sales_clean.csv")
DB = Path("sales.db")
REPORT = Path("reports/data_quality_report.txt")


def extract(path):
    df = pd.read_csv(path)
    print(f"[Extract] {len(df)} rows read from {path}")
    return df


def transform(df):
    log = {"raw_rows": len(df)}

    # 1. Remove exact duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    log["duplicates_removed"] = before - len(df)

    # 2. Standardize text columns (trim spaces, consistent casing)
    for col in ["customer_name", "region", "product"]:
        df[col] = df[col].astype("string").str.strip()
    df["region"] = df["region"].str.title()
    df["product"] = df["product"].str.title()

    # 3. Treat empty customer names as missing and fill with 'Unknown'
    df["customer_name"] = df["customer_name"].replace("", pd.NA)
    log["missing_customer_name"] = int(df["customer_name"].isna().sum())
    df["customer_name"] = df["customer_name"].fillna("Unknown")

    # 4. Convert price like "$850" to a number
    df["unit_price"] = df["unit_price"].astype(str).str.replace("$", "", regex=False).astype(float)

    # 5. Parse dates; impossible dates become NaT and are dropped
    df["order_date"] = pd.to_datetime(df["order_date"], format="%Y-%m-%d", errors="coerce")
    bad_dates = int(df["order_date"].isna().sum())
    df = df.dropna(subset=["order_date"])
    log["invalid_dates_removed"] = bad_dates

    # 6. Remove invalid quantities (zero or negative)
    bad_qty = int((df["quantity"] <= 0).sum())
    df = df[df["quantity"] > 0]
    log["invalid_quantity_removed"] = bad_qty

    # 7. Add a calculated column
    df["total_sales"] = df["quantity"] * df["unit_price"]

    log["clean_rows"] = len(df)
    return df.reset_index(drop=True), log


def validate(df):
    """Simple automated checks. The pipeline stops if any check fails."""
    checks = {
        "order_id is unique": df["order_id"].is_unique,
        "no missing values": not df.isna().any().any(),
        "all quantities > 0": bool((df["quantity"] > 0).all()),
        "all prices > 0": bool((df["unit_price"] > 0).all()),
        "regions are valid": set(df["region"]).issubset({"North", "South", "East", "West"}),
    }
    for name, passed in checks.items():
        print(f"[Validate] {'PASS' if passed else 'FAIL'} - {name}")
    if not all(checks.values()):
        raise ValueError("Data validation failed - see messages above")
    return checks


def load(df):
    CLEAN.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN, index=False)
    with sqlite3.connect(DB) as conn:
        df.to_sql("sales", conn, if_exists="replace", index=False)
    print(f"[Load] {len(df)} rows loaded into {DB} (table: sales) and {CLEAN}")


def write_report(log, checks):
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = ["DATA QUALITY REPORT", "=" * 30]
    lines += [f"{k}: {v}" for k, v in log.items()]
    lines += ["", "Validation checks:"]
    lines += [f"  {'PASS' if v else 'FAIL'} - {k}" for k, v in checks.items()]
    REPORT.write_text("\n".join(lines))
    print(f"[Report] saved to {REPORT}")


if __name__ == "__main__":
    raw = extract(RAW)
    clean, log = transform(raw)
    checks = validate(clean)
    load(clean)
    write_report(log, checks)
