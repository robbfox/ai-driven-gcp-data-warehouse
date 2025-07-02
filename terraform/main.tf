


terraform {
  backend "gcs" {
    bucket = "robb-gemini-bq"
    prefix = "terraform/state"
  }
}

# Terraform configuration for Google BigQuery Data Warehouse



provider "google" {
  project = var.project_id
  region  = "us-central1"
}


# This block tells Terraform how to find the existing GCS bucket
import {
  id = "robbproject1-olist-ecommerce-data" # The GCP resource ID
  to = google_storage_bucket.olist_ecommerce_data  # The Terraform resource address
}

# This block tells Terraform how to find the existing BigQuery dataset
import {
  id = "robbproject1:olist_ecommerce" # The GCP resource ID
  to = google_bigquery_dataset.olist_ecommerce # The Terraform resource address
}

resource "google_storage_bucket" "olist_ecommerce_data" {
  name          = "robbproject1-olist-ecommerce-data"
  location      = "US"
  force_destroy = false # Set to true for easy cleanup during development, but be cautious in production
}


resource "google_bigquery_dataset" "olist_ecommerce" {
  dataset_id = "olist_ecommerce"
  location   = "US"
}

resource "google_bigquery_table" "olist_customers_dataset" {
  dataset_id = google_bigquery_dataset.olist_ecommerce.dataset_id
  table_id   = "olist_customers_dataset"
  schema = <<EOF
[
  {"name": "customer_id", "type": "STRING"},
  {"name": "customer_unique_id", "type": "STRING"},
  {"name": "customer_zip_code_prefix", "type": "INTEGER"},
  {"name": "customer_city", "type": "STRING"},
  {"name": "customer_state", "type": "STRING"}
]
EOF
}

resource "google_bigquery_table" "olist_geolocation_dataset" {
  dataset_id = google_bigquery_dataset.olist_ecommerce.dataset_id
  table_id   = "olist_geolocation_dataset"
  schema = <<EOF
[
  {"name": "geolocation_zip_code_prefix", "type": "INTEGER"},
  {"name": "geolocation_lat", "type": "FLOAT"},
  {"name": "geolocation_lng", "type": "FLOAT"},
  {"name": "geolocation_city", "type": "STRING"},
  {"name": "geolocation_state", "type": "STRING"}
]
EOF
}

resource "google_bigquery_table" "olist_orders_dataset" {
  dataset_id = google_bigquery_dataset.olist_ecommerce.dataset_id
  table_id   = "olist_orders_dataset"
  schema = <<EOF
[
  {"name": "order_id", "type": "STRING"},
  {"name": "customer_id", "type": "STRING"},
  {"name": "order_status", "type": "STRING"},
  {"name": "order_purchase_timestamp", "type": "TIMESTAMP"},
  {"name": "order_approved_at", "type": "TIMESTAMP"},
  {"name": "order_delivered_carrier_date", "type": "TIMESTAMP"},
  {"name": "order_delivered_customer_date", "type": "TIMESTAMP"},
  {"name": "order_estimated_delivery_date", "type": "TIMESTAMP"}
]
EOF
}

resource "google_bigquery_table" "olist_order_items_dataset" {
  dataset_id = google_bigquery_dataset.olist_ecommerce.dataset_id
  table_id   = "olist_order_items_dataset"
  schema = <<EOF
[
  {"name": "order_id", "type": "STRING"},
  {"name": "order_item_id", "type": "INTEGER"},
  {"name": "product_id", "type": "STRING"},
  {"name": "seller_id", "type": "STRING"},
  {"name": "shipping_limit_date", "type": "TIMESTAMP"},
  {"name": "price", "type": "FLOAT"},
  {"name": "freight_value", "type": "FLOAT"}
]
EOF
}

resource "google_bigquery_table" "olist_order_payments_dataset" {
  dataset_id = google_bigquery_dataset.olist_ecommerce.dataset_id
  table_id   = "olist_order_payments_dataset"
  schema = <<EOF
[
  {"name": "order_id", "type": "STRING"},
  {"name": "payment_sequential", "type": "INTEGER"},
  {"name": "payment_type", "type": "STRING"},
  {"name": "payment_installments", "type": "INTEGER"},
  {"name": "payment_value", "type": "FLOAT"}
]
EOF
}

resource "google_bigquery_table" "olist_order_reviews_dataset" {
  dataset_id = google_bigquery_dataset.olist_ecommerce.dataset_id
  table_id   = "olist_order_reviews_dataset"
  schema = <<EOF
[
  {"name": "review_id", "type": "STRING"},
  {"name": "order_id", "type": "STRING"},
  {"name": "review_score", "type": "INTEGER"},
  {"name": "review_comment_title", "type": "STRING"},
  {"name": "review_comment_message", "type": "STRING"},
  {"name": "review_creation_date", "type": "TIMESTAMP"},
  {"name": "review_answer_timestamp", "type": "TIMESTAMP"}
]
EOF
}

resource "google_bigquery_table" "olist_products_dataset" {
  dataset_id = google_bigquery_dataset.olist_ecommerce.dataset_id
  table_id   = "olist_products_dataset"
  schema = <<EOF
[
  {"name": "product_id", "type": "STRING"},
  {"name": "product_category_name", "type": "STRING"},
  {"name": "product_name_lenght", "type": "INTEGER"},
  {"name": "product_description_lenght", "type": "INTEGER"},
  {"name": "product_photos_qty", "type": "INTEGER"},
  {"name": "product_weight_g", "type": "INTEGER"},
  {"name": "product_length_cm", "type": "INTEGER"},
  {"name": "product_height_cm", "type": "INTEGER"},
  {"name": "product_width_cm", "type": "INTEGER"}
]
EOF
}

resource "google_bigquery_table" "olist_sellers_dataset" {
  dataset_id = google_bigquery_dataset.olist_ecommerce.dataset_id
  table_id   = "olist_sellers_dataset"
  schema = <<EOF
[
  {"name": "seller_id", "type": "STRING"},
  {"name": "seller_zip_code_prefix", "type": "INTEGER"},
  {"name": "seller_city", "type": "STRING"},
  {"name": "seller_state", "type": "STRING"}
]
EOF
}

resource "google_bigquery_table" "product_category_name_translation" {
  dataset_id = google_bigquery_dataset.olist_ecommerce.dataset_id
  table_id   = "product_category_name_translation"
  schema = <<EOF
[
  {"name": "product_category_name", "type": "STRING"},
  {"name": "product_category_name_english", "type": "STRING"}
]
EOF
}
