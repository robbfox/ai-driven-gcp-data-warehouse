import streamlit as st
import pandas as pd
import plotly.express as px
from google.cloud import bigquery

# --- GCP Project and BQ Client Setup ---
PROJECT_ID = "robbproject1" # Make sure this is your project ID
client = bigquery.Client(project=PROJECT_ID)

# --- Page Configuration (do this once at the top) ---
st.set_page_config(
    page_title="Olist Sales Dashboard",
    page_icon="🇧🇷",
    layout="wide",
)

# --- Caching ---
# This function is perfect. It caches based on the input query string.
@st.cache_data
def run_query(query: str) -> pd.DataFrame:
    """Runs a BigQuery query and returns the results as a Pandas DataFrame."""
    return client.query(query).to_dataframe()

# --- Filter Data ---
# This query runs once to populate the filter dropdown.
@st.cache_data
def get_category_list():
    query = """
    SELECT DISTINCT product_category_name_english
    FROM `robbproject1.olist_analytics.dim_products`
    WHERE product_category_name_english IS NOT NULL
    ORDER BY product_category_name_english
    """
    df = run_query(query)
    return ['All'] + df['product_category_name_english'].tolist()

# --- START OF THE APP, RUNS ON EVERY INTERACTION ---

st.title("🇧🇷 Olist Executive Sales Dashboard")

# 1. RENDER THE FILTER WIDGET AND GET THE USER'S SELECTION
st.sidebar.header("Filters")
category_list = get_category_list()
selected_category = st.sidebar.selectbox(
    "Select a Product Category",
    category_list
)

# 2. CREATE THE DYNAMIC WHERE CLAUSE BASED ON THE SELECTION
where_clause = ""
if selected_category != "All":
    # Using 'p' as the alias for the products table in our queries
    where_clause = f"AND p.product_category_name_english = '{selected_category}'"

# 3. DYNAMICALLY CREATE THE FULL QUERY STRINGS USING THE WHERE CLAUSE
#    These are re-created every time the script runs.
kpi_query = f"""
SELECT
    SUM(oi.proportional_item_payment_value) AS total_revenue,
    COUNT(DISTINCT o.order_id) AS total_orders,
    AVG(timestamp_diff(o.order_delivered_customer_date, o.order_purchase_timestamp, DAY)) as avg_delivery_time
FROM `robbproject1.olist_analytics.fct_order_items` AS oi
JOIN `robbproject1.olist_analytics.stg_orders` as o ON oi.order_id = o.order_id
JOIN `robbproject1.olist_analytics.dim_products` as p ON oi.product_id = p.product_id
WHERE o.order_status = 'delivered' {where_clause}
"""

revenue_by_month_query = f"""
SELECT
    FORMAT_TIMESTAMP('%Y-%m', f.order_purchase_timestamp) AS purchase_month,
    SUM(f.proportional_item_payment_value) AS monthly_revenue
FROM `robbproject1.olist_analytics.fct_order_items` as f
JOIN `robbproject1.olist_analytics.dim_products` as p ON f.product_id = p.product_id
WHERE 1=1 {where_clause}
GROUP BY 1 ORDER BY 1
"""

# This query remains static because we always want to show the overall top 10
revenue_by_category_query = """
SELECT
    p.product_category_name_english AS product_category,
    SUM(oi.proportional_item_payment_value) AS total_revenue
FROM `robbproject1.olist_analytics.fct_order_items` AS oi
JOIN `robbproject1.olist_analytics.dim_products` AS p ON oi.product_id = p.product_id
GROUP BY 1 ORDER BY 2 DESC LIMIT 10
"""

# 4. EXECUTE THE QUERIES AND LOAD DATA
#    run_query will fetch from cache if the query string hasn't changed,
#    or run a new query if it has.
kpi_data = run_query(kpi_query)
revenue_by_month_data = run_query(revenue_by_month_query)
revenue_by_category_data = run_query(revenue_by_category_query)

# 5. DISPLAY KPIs AND CHARTS
st.header("Key Performance Indicators")
if not kpi_data.empty:
    total_revenue = kpi_data['total_revenue'].iloc[0]
    total_orders = kpi_data['total_orders'].iloc[0]
    avg_delivery = kpi_data['avg_delivery_time'].iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"R$ {total_revenue:,.2f}" if total_revenue else "R$ 0.00")
    col2.metric("Total Orders", f"{total_orders:,}" if total_orders else "0")
    col3.metric("Avg. Delivery Time", f"{avg_delivery:.1f} Days" if avg_delivery else "N/A")

# --- This is the NEW, DYNAMIC section for app.py ---

st.header("Visualizations")

# 1. Create the dynamic title based on the filter selection
if selected_category == "All":
    dynamic_title = "Monthly Revenue Over Time (Overall)"
else:
    dynamic_title = f"Monthly Revenue Over Time for: :rainbow[{selected_category}]"

# 2. Use the dynamic title for the subheader AND the chart
st.subheader(dynamic_title) # <-- New subheader for clarity
fig_monthly_revenue = px.line(
    revenue_by_month_data,
    x='purchase_month',
    y='monthly_revenue',
    title=dynamic_title,  # <-- Using the new dynamic title variable
    labels={'purchase_month': 'Month', 'monthly_revenue': 'Total Revenue (R$)'},
    markers=True
)
st.plotly_chart(fig_monthly_revenue, use_container_width=True)



fig_category_revenue = px.bar(
    revenue_by_category_data.sort_values('total_revenue', ascending=True),
    x='total_revenue',
    y='product_category',
    orientation='h',
    title='Top 10 Product Categories by Revenue (Overall)',
    labels={'product_category': 'Product Category', 'total_revenue': 'Total Revenue (R$)'}
)
st.plotly_chart(fig_category_revenue, use_container_width=True)