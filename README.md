# AI-Driven GCP Data Warehouse

This project demonstrates the creation and management of a data warehouse on Google Cloud Platform (GCP) using an AI-driven approach. It leverages Terraform for infrastructure as code, dbt for data transformation, and a Streamlit dashboard for data visualization.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [1. Infrastructure Provisioning with Terraform](#1-infrastructure-provisioning-with-terraform)
  - [2. Data Loading](#2-data-loading)
  - [3. Data Transformation with dbt](#3-data-transformation-with-dbt)
  - [4. Running the Dashboard](#4-running-the-dashboard)
- [Project Structure](#project-structure)
- [Data Schema](#data-schema)

## Getting Started

### Prerequisites

- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and configured.
- [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) installed.
- [Python 3.8+](https://www.python.org/downloads/) installed.
- A GCP project with the BigQuery and Cloud Storage APIs enabled.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/ai-driven-gcp-data-warehouse.git
    cd ai-driven-gcp-data-warehouse
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

## Usage

### 1. Infrastructure Provisioning with Terraform

Terraform is used to define and provision the GCP infrastructure, including the BigQuery dataset and tables.

1.  **Navigate to the Terraform directory:**
    ```bash
    cd terraform
    ```

2.  **Initialize Terraform:**
    ```bash
    terraform init
    ```

3.  **Review the execution plan:**
    ```bash
    terraform plan
    ```

4.  **Apply the changes:**
    ```bash
    terraform apply
    ```

### 2. Data Loading

The `src/load_data.py` script loads the raw data from CSV files into the BigQuery tables created by Terraform.

1.  **Set environment variables:**
    ```bash
    export GCP_PROJECT_ID="your-gcp-project-id"
    export GCS_BUCKET_NAME="your-gcs-bucket-name"
    ```

2.  **Run the data loading script:**
    ```bash
    python src/load_data.py
    ```

### 3. Data Transformation with dbt

dbt is used to transform the raw data into a clean, analytics-ready format.

1.  **Navigate to the dbt project directory:**
    ```bash
    cd dbt_project
    ```

2.  **Install dbt dependencies:**
    ```bash
    dbt deps
    ```

3.  **Run the dbt models:**
    ```bash
    dbt run
    ```

### 4. Running the Dashboard

The Streamlit dashboard provides an interactive way to explore the transformed data.

1.  **Navigate to the dashboard directory:**
    ```bash
    cd dashboard
    ```

2.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```

## Project Structure

```
.
├── dashboard/              # Streamlit dashboard files
│   ├── app.py
│   └── pages/
├── dbt_project/            # dbt project for data transformation
│   ├── models/
│   └── dbt_project.yml
├── src/                    # Python scripts
│   └── load_data.py
├── terraform/              # Terraform configuration for infrastructure
│   ├── main.tf
│   └── variables.tf
├── get_schema.py           # Script to extract schemas from CSVs
├── schemas.csv             # CSV schemas
└── requirements.txt        # Python dependencies
```

## Data Schema

The raw data is loaded into the following tables in the `olist_ecommerce` BigQuery dataset.

| File Name                          | Headers                                                                                                                                                           |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `olist_customers_dataset.csv`      | `['customer_id', 'customer_unique_id', 'customer_zip_code_prefix', 'customer_city', 'customer_state']`                                                              |
| `olist_geolocation_dataset.csv`    | `['geolocation_zip_code_prefix', 'geolocation_lat', 'geolocation_lng', 'geolocation_city', 'geolocation_state']`                                                    |
| `olist_orders_dataset.csv`         | `['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']` |
| `olist_order_items_dataset.csv`    | `['order_id', 'order_item_id', 'product_id', 'seller_id', 'shipping_limit_date', 'price', 'freight_value']`                                                          |
| `olist_order_payments_dataset.csv` | `['order_id', 'payment_sequential', 'payment_type', 'payment_installments', 'payment_value']`                                                                       |
| `olist_order_reviews_dataset.csv`  | `['review_id', 'order_id', 'review_score', 'review_comment_title', 'review_comment_message', 'review_creation_date', 'review_answer_timestamp']`                      |
| `olist_products_dataset.csv`       | `['product_id', 'product_category_name', 'product_name_lenght', 'product_description_lenght', 'product_photos_qty', 'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']` |
| `olist_sellers_dataset.csv`        | `['seller_id', 'seller_zip_code_prefix', 'seller_city', 'seller_state']`                                                                                            |
| `product_category_name_translation.csv` | `['product_category_name', 'product_category_name_english']`                                                                                                     |
## Acknowledgements

This project was developed with invaluable support from Google's [gemini-cli](https://blog.google/technology/developers/introducing-gemini-cli-open-source-ai-agent/). This tool was instrumental in generating a code framework, accelerating deployment, debugging, and drafting documentation.