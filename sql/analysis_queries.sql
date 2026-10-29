-- Run these on sales.db (SQLite). Example: sqlite3 sales.db < sql/analysis_queries.sql

-- 1. Total revenue and number of orders
SELECT COUNT(*) AS total_orders, ROUND(SUM(total_sales), 2) AS total_revenue
FROM sales;

-- 2. Revenue by region
SELECT region, ROUND(SUM(total_sales), 2) AS revenue
FROM sales
GROUP BY region
ORDER BY revenue DESC;

-- 3. Top 3 products by revenue
SELECT product, SUM(quantity) AS units_sold, ROUND(SUM(total_sales), 2) AS revenue
FROM sales
GROUP BY product
ORDER BY revenue DESC
LIMIT 3;

-- 4. Monthly revenue trend
SELECT strftime('%Y-%m', order_date) AS month, ROUND(SUM(total_sales), 2) AS revenue
FROM sales
GROUP BY month
ORDER BY month;

-- 5. Data quality check: duplicate order IDs (should return 0 rows)
SELECT order_id, COUNT(*) AS cnt
FROM sales
GROUP BY order_id
HAVING cnt > 1;
