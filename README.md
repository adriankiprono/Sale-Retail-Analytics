# Sale-Retail-Analytics

# Retail Sales Analytics Dashboard

## Project Overview

An end-to-end retail sales analytics project built using Python,
PostgreSQL, SQL, and Streamlit.

The project analyzes retail sales transactions to identify
revenue trends, profitability, product performance, and
the impact of discounts on business performance.

## Technologies Used

- Python
- PostgreSQL
- SQL
- Pandas
- SQLAlchemy
- Streamlit
- Matplotlib

## Dataset

The project uses a Superstore-style retail sales dataset
containing 9,994 transaction records.

The dataset includes sales, profit, discounts, product
categories, customer segments, and geographical regions.

## Key Performance Indicators

| Metric | Value |
|--------|-------|
| Total Revenue | $2,297,200.86 |
| Total Profit | $286,397.02 |
| Total Orders | 5,009 |
| Profit Margin | 12.47% |

## Key Business Insights

- Technology generated the highest revenue and profit.
- Furniture had a relatively low profit margin.
- Heavy discounting was associated with significant losses.
- Tables and Bookcases were loss-making subcategories.
- Revenue increased strongly during 2016 and 2017.

## Project Workflow

1. Data exploration using Python and Pandas.
2. Data cleaning and validation.
3. Loading cleaned data into PostgreSQL.
4. SQL queries for business analysis.
5. Interactive dashboard development using Streamlit.
6. Visualization of KPIs and business trends.

## Running the Project

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies from requirements.txt.
4. Set up the PostgreSQL database.
5. Configure Streamlit database credentials locally.
6. Run the dashboard:

```bash
streamlit run dashboard/app.py
```

## Future Improvements

- Automated ETL pipelines.
- Dashboard deployment.
- Additional customer segmentation analysis.
- Sales forecasting.

## Author

Retail Sales Analytics Portfolio Project
