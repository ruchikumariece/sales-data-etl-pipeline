# Sales Data ETL Pipeline

A small Python + SQL project that takes messy sales data, cleans it, validates it, loads it into a SQLite database, and prepares a clean file for a Power BI dashboard.

> Note: the data is **synthetic** (created by `generate_sample_data.py`) and made intentionally messy to practice data quality work.

## What it does
1. **Extract** - reads a raw CSV file (520 rows).
2. **Transform** - removes duplicate rows, fixes text casing and spaces, converts prices like `$850` to numbers, removes impossible dates and invalid quantities, fills missing customer names, and adds a `total_sales` column.
3. **Validate** - runs automated checks (unique order IDs, no missing values, positive quantities and prices, valid regions). The pipeline stops if a check fails.
4. **Load** - saves the clean data into a SQLite table (`sales`) and a clean CSV.
5. **Report** - writes a data quality report showing how many problems were found and fixed.
6. **Analyze** - SQL queries for revenue by region, top products, and monthly trend.

## Data quality results (sample run)
| Check | Count |
|---|---|
| Raw rows | 520 |
| Duplicate rows removed | 20 |
| Missing customer names filled | 12 |
| Invalid dates removed | 8 |
| Invalid quantities removed | 10 |
| Clean rows loaded | 482 |

## Tools
Python (pandas), SQL (SQLite), Power BI, Git/GitHub

## How to run
```bash
pip install -r requirements.txt
python generate_sample_data.py   # creates data/raw/sales_raw.csv
python etl_pipeline.py           # cleans, validates, loads
```
Then run the queries in `sql/analysis_queries.sql` on `sales.db`
(use DB Browser for SQLite, or `sqlite3 sales.db < sql/analysis_queries.sql`).

## Power BI dashboard
Open Power BI Desktop, import `data/clean/sales_clean.csv`, and build visuals: revenue by region, top products, monthly trend. Add a screenshot to a `screenshots/` folder and link it here.

## What I learned
- Raw data usually has problems; checking quality first saves time later.
- Automated validation checks catch errors before data reaches reports.
- A repeatable script is better than fixing data by hand.
