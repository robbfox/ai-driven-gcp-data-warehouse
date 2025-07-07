import streamlit as st
import pandas as pd
import plotly.express as px
from google.cloud import bigquery

# --- GCP Project and BQ Client Setup ---
PROJECT_ID = "robbproject1" # Make sure this is your project ID
client = bigquery.Client(project=PROJECT_ID)

# --- Caching ---
@st.cache_data
def run_query(query: str) -> pd.DataFrame:
    """Runs a BigQuery query and returns the results as a Pandas DataFrame."""
    return client.query(query).to_dataframe()

# --- Page Configuration ---
st.set_page_config(page_title="Logistics Analysis", layout="wide")

st.title("🚚 Logistics & Operations Analysis")

# --- SQL Queries ---
delivery_delta_query = """
-- This query calculates the difference between estimated and actual delivery.
-- Negative numbers are good (arrived early), positive numbers are bad (arrived late).
SELECT
    p.product_category_name_english AS product_category,
    AVG(TIMESTAMP_DIFF(o.order_delivered_customer_date, o.order_estimated_delivery_date, DAY)) as avg_delivery_delta_days,
    COUNT(o.order_id) as total_orders
FROM
    `robbproject1.olist_analytics.fct_order_items` AS f
JOIN
    `robbproject1.olist_analytics.stg_orders` as o ON f.order_id = o.order_id
JOIN
    `robbproject1.olist_analytics.dim_products` as p ON f.product_id = p.product_id
WHERE
    o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL
    AND o.order_estimated_delivery_date IS NOT NULL
GROUP BY 1
HAVING COUNT(o.order_id) > 50 -- Only show categories with a meaningful number of orders
ORDER BY 2 DESC
"""

avg_delivery_by_seller_state_query = """
SELECT
    s.seller_state,
    AVG(TIMESTAMP_DIFF(o.order_delivered_customer_date, o.order_purchase_timestamp, DAY)) as avg_delivery_time
FROM
    `robbproject1.olist_analytics.fct_order_items` AS f
JOIN
    `robbproject1.olist_analytics.stg_orders` as o ON f.order_id = o.order_id
JOIN
    `robbproject1.olist_analytics.dim_sellers` as s ON f.seller_id = s.seller_id
WHERE
    o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL
GROUP BY 1
ORDER BY 2 DESC
"""


# --- Data Loading ---
delivery_delta_data = run_query(delivery_delta_query)
delivery_by_seller_data = run_query(avg_delivery_by_seller_state_query)


# --- Visualizations ---
st.header("Delivery Performance vs. Estimates")
st.write("This chart shows the average number of days an order arrived early (negative) or late (positive) compared to its estimate, broken down by product category.")

# Chart 1: Delivery Delta by Product Category
fig_delivery_delta = px.bar(
    delivery_delta_data,
    x='avg_delivery_delta_days',
    y='product_category',
    orientation='h',
    title='Average Delivery Time vs. Estimate by Product Category',
    labels={'product_category': 'Product Category', 'avg_delivery_delta_days': 'Avg. Days Early/Late'},
    color='avg_delivery_delta_days',
    color_continuous_scale=px.colors.diverging.RdYlGn_r # Red for late, Green for early
)
fig_delivery_delta.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig_delivery_delta, use_container_width=True)


st.header("Average Delivery Time by Seller State")
st.write("Where do the fastest and slowest shipments originate from?")

# Chart 2: Average Delivery by Seller State
fig_delivery_seller = px.bar(
    delivery_by_seller_data,
    x='seller_state',
    y='avg_delivery_time',
    title='Average Delivery Time by Seller State',
    labels={'seller_state': 'Seller State', 'avg_delivery_time': 'Average Delivery Time (Days)'}
)
st.plotly_chart(fig_delivery_seller, use_container_width=True)