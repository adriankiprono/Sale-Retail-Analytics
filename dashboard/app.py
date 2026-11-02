import streamlit as st
from sqlalchemy import text
from database import get_engine
import plotly.express as px

# Configure the dashboard
st.set_page_config(
    page_title="Retail Sales Analytics",
    page_icon="📊",
    layout="wide"
)

# Dashboard title
st.title("📊 Retail Sales Analytics Dashboard")

st.write(
    "Analyzing sales performance, profitability, "
    "and customer purchasing patterns."
)

st.divider()

# Dashboard introduction
st.subheader("Business Performance Overview")

st.info(
    "Welcome to the Retail Sales Analytics Dashboard. "
    "We will display sales KPIs and interactive charts here."
)


import pandas as pd

try:
    engine = get_engine()

    query = """
        SELECT
            ROUND(SUM(sales), 2) AS total_revenue,
            ROUND(SUM(profit), 2) AS total_profit,
            COUNT(DISTINCT order_id) AS total_orders,
            ROUND(
                SUM(profit) / NULLIF(SUM(sales), 0) * 100,
                2
            ) AS profit_margin
        FROM superstore_sales;
    """

    kpis = pd.read_sql(query, engine)

    revenue = float(kpis.loc[0, "total_revenue"])
    profit = float(kpis.loc[0, "total_profit"])
    orders = int(kpis.loc[0, "total_orders"])
    margin = float(kpis.loc[0, "profit_margin"])

    st.subheader("Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Revenue", f"${revenue:,.2f}")

    with col2:
        st.metric("Total Profit", f"${profit:,.2f}")

    with col3:
        st.metric("Total Orders", f"{orders:,}")

    with col4:
        st.metric("Profit Margin", f"{margin:.2f}%")

        # Annual sales performance
    st.divider()
    st.subheader("Annual Sales Performance")

    yearly_query = """
        SELECT
            EXTRACT(YEAR FROM order_date)::INTEGER AS sales_year,
            ROUND(SUM(sales), 2) AS total_revenue,
            ROUND(SUM(profit), 2) AS total_profit
        FROM superstore_sales
        GROUP BY EXTRACT(YEAR FROM order_date)
        ORDER BY sales_year;
    """

    yearly_df = pd.read_sql(yearly_query, engine)

    fig = px.line(
        yearly_df,
        x="sales_year",
        y=["total_revenue", "total_profit"],
        markers=True,
        title="Revenue and Profit Trends (2014–2017)",
        labels={
            "sales_year": "Year",
            "value": "Amount (USD)",
            "variable": "Metric"
        }
    )

    fig.update_layout(
        xaxis=dict(
            tickmode="linear",
            dtick=1
        ),
        hovermode="x unified"
    )

    st.plotly_chart(fig, width="stretch")
        # Category performance analysis
    st.divider()
    st.subheader("Sales Performance by Category")

    category_query = """
        SELECT
            category,
            ROUND(SUM(sales), 2) AS total_revenue,
            ROUND(SUM(profit), 2) AS total_profit,
            ROUND(
                SUM(profit) / NULLIF(SUM(sales), 0) * 100,
                2
            ) AS profit_margin
        FROM superstore_sales
        GROUP BY category
        ORDER BY total_revenue DESC;
    """

    category_df = pd.read_sql(category_query, engine)

    # Create interactive bar chart
    category_fig = px.bar(
        category_df,
        x="category",
        y=["total_revenue", "total_profit"],
        barmode="group",
        title="Revenue vs Profit by Category",
        labels={
            "category": "Product Category",
            "value": "Amount (USD)",
            "variable": "Metric"
        }
    )

    category_fig.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(category_fig, width="stretch")

    st.subheader("Category Profitability Summary")

    st.dataframe(
        category_df,
        width="stretch",
        hide_index=True,
        column_config={
            "category": "Category",
            "total_revenue": st.column_config.NumberColumn(
                "Revenue ($)",
                format="$%.2f"
            ),
            "total_profit": st.column_config.NumberColumn(
                "Profit ($)",
                format="$%.2f"
            ),
            "profit_margin": st.column_config.NumberColumn(
                "Profit Margin (%)",
                format="%.2f%%"
            )
        }
    )
        # Regional sales performance
    st.divider()
    st.subheader("Regional Sales Performance")

    region_query = """
        SELECT
            region,
            ROUND(SUM(sales), 2) AS total_revenue,
            ROUND(SUM(profit), 2) AS total_profit,
            COUNT(DISTINCT order_id) AS total_orders,
            ROUND(
                SUM(profit) / NULLIF(SUM(sales), 0) * 100,
                2
            ) AS profit_margin
        FROM superstore_sales
        GROUP BY region
        ORDER BY total_revenue DESC;
    """

    region_df = pd.read_sql(region_query, engine)

    region_fig = px.bar(
        region_df,
        x="region",
        y=["total_revenue", "total_profit"],
        barmode="group",
        title="Revenue vs Profit by Region",
        labels={
            "region": "Region",
            "value": "Amount (USD)",
            "variable": "Metric"
        }
    )

    region_fig.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(region_fig, width="stretch")
    st.subheader("Regional Profitability Summary")

    st.dataframe(
        region_df,
        width="stretch",
        hide_index=True,
        column_config={
            "region": "Region",
            "total_revenue": st.column_config.NumberColumn(
                "Revenue ($)",
                format="$%.2f"
            ),
            "total_profit": st.column_config.NumberColumn(
                "Profit ($)",
                format="$%.2f"
            ),
            "total_orders": st.column_config.NumberColumn(
                "Orders",
                format="%d"
            ),
            "profit_margin": st.column_config.NumberColumn(
                "Profit Margin (%)",
                format="%.2f%%"
            )
        }
    )
        # Discount profitability analysis
    st.divider()
    st.subheader("Discount Impact on Profitability")

    discount_query = """
        WITH discount_data AS (
            SELECT
                CASE
                    WHEN discount = 0 THEN 'No Discount'
                    WHEN discount <= 0.20 THEN '1-20%'
                    WHEN discount <= 0.40 THEN '21-40%'
                    WHEN discount <= 0.60 THEN '41-60%'
                    ELSE 'Above 60%'
                END AS discount_range,
                discount,
                sales,
                profit
            FROM superstore_sales
        )
        SELECT
            discount_range,
            COUNT(*) AS sales_lines,
            ROUND(AVG(discount) * 100, 2) AS avg_discount_pct,
            ROUND(SUM(sales), 2) AS total_revenue,
            ROUND(SUM(profit), 2) AS total_profit,
            ROUND(
                SUM(profit) / NULLIF(SUM(sales), 0) * 100,
                2
            ) AS profit_margin
        FROM discount_data
        GROUP BY discount_range
    """

    with engine.connect() as conn:
        discount_df = pd.read_sql_query(
            text(discount_query),
            conn
        )

    discount_order = [
        "No Discount",
        "1-20%",
        "21-40%",
        "41-60%",
        "Above 60%"
    ]

    discount_fig = px.bar(
        discount_df,
        x="discount_range",
        y="profit_margin",
        color="profit_margin",
        color_continuous_scale="RdYlGn",
        category_orders={
            "discount_range": discount_order
        },
        title="Profit Margin by Discount Range",
        labels={
            "discount_range": "Discount Range",
            "profit_margin": "Profit Margin (%)"
        },
        text="profit_margin"
    )

    discount_fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    discount_fig.update_layout(
        coloraxis_showscale=False
    )

    discount_fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="gray"
    )

    st.plotly_chart(discount_fig, width="stretch")
    st.subheader("Discount Profitability Summary")

    discount_df["discount_range"] = pd.Categorical(
        discount_df["discount_range"],
        categories=discount_order,
        ordered=True
    )

    discount_df = discount_df.sort_values("discount_range")

    st.dataframe(
        discount_df,
        width="stretch",
        hide_index=True,
        column_config={
            "discount_range": "Discount Range",
            "sales_lines": "Sales Lines",
            "avg_discount_pct": st.column_config.NumberColumn(
                "Average Discount (%)",
                format="%.2f%%"
            ),
            "total_revenue": st.column_config.NumberColumn(
                "Revenue ($)",
                format="$%.2f"
            ),
            "total_profit": st.column_config.NumberColumn(
                "Profit ($)",
                format="$%.2f"
            ),
            "profit_margin": st.column_config.NumberColumn(
                "Profit Margin (%)",
                format="%.2f%%"
            )
        }
    )
    st.warning(
        "Business Insight: Discount bands above 20% "
        "show negative aggregate profit margins. "
        "Review discount policies, especially for "
        "loss-making products and regions."
    )

        # Furniture profitability analysis
    st.divider()
    st.subheader("Furniture Profitability Analysis")

    furniture_query = """
        SELECT
            sub_category,
            ROUND(SUM(sales), 2) AS total_revenue,
            ROUND(SUM(profit), 2) AS total_profit,
            ROUND(AVG(discount) * 100, 2) AS avg_discount_pct,
            ROUND(
                SUM(profit) / NULLIF(SUM(sales), 0) * 100,
                2
            ) AS profit_margin
        FROM superstore_sales
        WHERE category = 'Furniture'
        GROUP BY sub_category
        ORDER BY total_profit ASC;
    """

    with engine.connect() as conn:
        furniture_df = pd.read_sql_query(
            text(furniture_query),
            conn
        )

    furniture_fig = px.bar(
        furniture_df,
        x="sub_category",
        y="total_profit",
        color="total_profit",
        color_continuous_scale="RdYlGn",
        title="Furniture Profit by Subcategory",
        labels={
            "sub_category": "Subcategory",
            "total_profit": "Profit (USD)"
        }
    )

    furniture_fig.update_layout(
        coloraxis_showscale=False
    )

    furniture_fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="gray"
    )

    st.plotly_chart(furniture_fig, width="stretch")

    st.subheader("Explore Furniture Subcategories")

    selected_subcategory = st.selectbox(
        "Select a Furniture Subcategory",
        options=furniture_df["sub_category"].tolist()
    )

    selected_data = furniture_df[
        furniture_df["sub_category"] == selected_subcategory
    ].iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Revenue",
            f"${float(selected_data['total_revenue']):,.2f}"
        )

    with col2:
        st.metric(
            "Profit",
            f"${float(selected_data['total_profit']):,.2f}"
        )

    with col3:
        st.metric(
            "Profit Margin",
            f"{float(selected_data['profit_margin']):.2f}%"
        )

        # Regional drill-down for the selected subcategory
    st.divider()
    st.subheader("Regional Furniture Drill-Down")

    regional_furniture_query = """
        SELECT
            sub_category,
            region,
            ROUND(SUM(sales), 2) AS total_revenue,
            ROUND(SUM(profit), 2) AS total_profit,
            ROUND(AVG(discount) * 100, 2) AS avg_discount_pct,
            ROUND(
                SUM(profit) / NULLIF(SUM(sales), 0) * 100,
                2
            ) AS profit_margin
        FROM superstore_sales
        WHERE category = 'Furniture'
        GROUP BY sub_category, region
        ORDER BY sub_category, region;
    """

    with engine.connect() as conn:
        regional_furniture_df = pd.read_sql_query(
            text(regional_furniture_query),
            conn
        )

    # Filter based on the dropdown from Step 25
    selected_region_df = regional_furniture_df[
        regional_furniture_df["sub_category"] == selected_subcategory
    ].copy()

    # Create regional profitability chart
    regional_furniture_fig = px.bar(
        selected_region_df,
        x="region",
        y="total_profit",
        color="total_profit",
        color_continuous_scale="RdYlGn",
        title=f"{selected_subcategory}: Profit by Region",
        labels={
            "region": "Region",
            "total_profit": "Profit (USD)"
        },
        hover_data=[
            "total_revenue",
            "avg_discount_pct",
            "profit_margin"
        ]
    )

    regional_furniture_fig.update_layout(
        coloraxis_showscale=False
    )

    regional_furniture_fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="gray"
    )

    st.plotly_chart(
        regional_furniture_fig,
        width="stretch"
    )
    st.subheader(
        f"{selected_subcategory}: Regional Performance Summary"
    )

    st.dataframe(
        selected_region_df[
            [
                "region",
                "total_revenue",
                "total_profit",
                "avg_discount_pct",
                "profit_margin"
            ]
        ],
        width="stretch",
        hide_index=True,
        column_config={
            "region": "Region",
            "total_revenue": st.column_config.NumberColumn(
                "Revenue ($)",
                format="$%.2f"
            ),
            "total_profit": st.column_config.NumberColumn(
                "Profit ($)",
                format="$%.2f"
            ),
            "avg_discount_pct": st.column_config.NumberColumn(
                "Average Discount (%)",
                format="%.2f%%"
            ),
            "profit_margin": st.column_config.NumberColumn(
                "Profit Margin (%)",
                format="%.2f%%"
            )
        }
    )

except Exception as error:
    st.error("Failed to load dashboard KPIs.")
    st.exception(error)