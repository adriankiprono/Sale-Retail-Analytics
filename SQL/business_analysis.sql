-- RETAIL SALES ANALYTICS
-- Business Analysis Using PostgreSQL

-- 1. Overall Sales KPIs
SELECT
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(
        SUM(profit) / NULLIF(SUM(sales), 0) * 100,
        2
    ) AS profit_margin_percentage
FROM superstore_sales;

-- 2. Category Performance
SELECT
    category,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    SUM(quantity) AS units_sold,
    ROUND(
        SUM(profit) / NULLIF(SUM(sales), 0) * 100,
        2
    ) AS profit_margin_percentage
FROM superstore_sales
GROUP BY category
ORDER BY total_revenue DESC;

-- 3. Regional Performance
SELECT
    region,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(
        SUM(profit) / NULLIF(SUM(sales), 0) * 100,
        2
    ) AS profit_margin_percentage
FROM superstore_sales
GROUP BY region
ORDER BY total_revenue DESC;

-- 4. Yearly Sales Trends
WITH yearly_sales AS (
    SELECT
        EXTRACT(YEAR FROM order_date)::INTEGER AS sales_year,
        SUM(sales) AS total_revenue
    FROM superstore_sales
    GROUP BY EXTRACT(YEAR FROM order_date)
)
SELECT
    sales_year,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(
        LAG(total_revenue) OVER (ORDER BY sales_year),
        2
    ) AS previous_year_revenue,
    ROUND(
        (
            total_revenue -
            LAG(total_revenue) OVER (ORDER BY sales_year)
        ) /
        NULLIF(
            LAG(total_revenue) OVER (ORDER BY sales_year),
            0
        ) * 100,
        2
    ) AS yoy_growth_percentage
FROM yearly_sales
ORDER BY sales_year;

-- 5. Top 10 Products
SELECT
    product_name,
    category,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    SUM(quantity) AS units_sold,
    ROUND(
        SUM(profit) / NULLIF(SUM(sales), 0) * 100,
        2
    ) AS profit_margin_percentage
FROM superstore_sales
GROUP BY product_name, category
ORDER BY total_revenue DESC
LIMIT 10;

-- 6. Discount Impact Analysis
SELECT
    CASE
        WHEN discount = 0 THEN 'No Discount'
        WHEN discount <= 0.20 THEN '1-20%'
        WHEN discount <= 0.40 THEN '21-40%'
        WHEN discount <= 0.60 THEN '41-60%'
        ELSE 'Above 60%'
    END AS discount_range,
    COUNT(*) AS transactions,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(
        SUM(profit) / NULLIF(SUM(sales), 0) * 100,
        2
    ) AS profit_margin_pct
FROM superstore_sales
GROUP BY 1
ORDER BY MIN(discount);

-- 7. Furniture Subcategory Analysis
SELECT
    sub_category,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct,
    ROUND(
        SUM(profit) / NULLIF(SUM(sales), 0) * 100,
        2
    ) AS profit_margin_pct,
    COUNT(*) FILTER (WHERE profit < 0) AS loss_making_lines
FROM superstore_sales
WHERE category = 'Furniture'
GROUP BY sub_category
ORDER BY total_profit ASC;

-- 8. Tables Regional Profitability
SELECT
    region,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct,
    ROUND(
        SUM(profit) / NULLIF(SUM(sales), 0) * 100,
        2
    ) AS profit_margin_pct
FROM superstore_sales
WHERE sub_category = 'Tables'
GROUP BY region
ORDER BY total_profit ASC;