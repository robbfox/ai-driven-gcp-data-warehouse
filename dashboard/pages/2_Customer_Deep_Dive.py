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
st.set_page_config(page_title="Customer Deep Dive", layout="wide")

st.title("👥 Customer Deep Dive")

# --- SQL Queries ---
# --- SQL Queries ---
customers_by_state_query = """
SELECT
    c.customer_state,
    COUNT(DISTINCT f.customer_unique_id) AS customer_count,
    SUM(f.proportional_item_payment_value) as total_revenue
FROM
    `robbproject1.olist_analytics.fct_order_items` AS f
JOIN
    `robbproject1.olist_analytics.dim_customers` AS c ON f.customer_unique_id = c.customer_unique_id -- <<< THE FINAL, CORRECT JOIN
GROUP BY
    c.customer_state
ORDER BY
    customer_count DESC
"""

# --- Data Loading ---
customers_by_state_data = run_query(customers_by_state_query)


# --- A great debugging trick for the future ---
# st.write("Raw data from BigQuery:")
# st.dataframe(customers_by_state_data)
# By uncommenting the lines above, you can see the actual data returned from the query.
# If it's empty, you know the problem is in the SQL.


# --- Visualizations ---
st.header("Customer Distribution and Value by State")

# Chart 1: Customer Count by State
fig_customer_count = px.bar(
    customers_by_state_data,
    x='customer_state',
    y='customer_count',
    title='Number of Customers by State',
    labels={'customer_state': 'State', 'customer_count': 'Number of Customers'}
)
st.plotly_chart(fig_customer_count, use_container_width=True)


# Chart 2: Revenue by State
fig_customer_revenue = px.bar(
    customers_by_state_data.sort_values('total_revenue', ascending=False),
    x='customer_state',
    y='total_revenue',
    title='Total Revenue by State',
    labels={'customer_state': 'State', 'total_revenue': 'Total Revenue (R$)'}
)
st.plotly_chart(fig_customer_revenue, use_container_width=True)

st.dataframe(customers_by_state_data)