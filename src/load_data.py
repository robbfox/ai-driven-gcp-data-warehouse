import os
import pandas
from google.cloud import bigquery

def main():
    # Define the list of CSV filenames
    csv_files = [
        "olist_customers_dataset.csv",
        "olist_geolocation_dataset.csv",
        "olist_order_items_dataset.csv",
        "olist_order_payments_dataset.csv",
        "olist_order_reviews_dataset.csv",
        "olist_orders_dataset.csv",
        "olist_products_dataset.csv",
        "olist_sellers_dataset.csv",
        "product_category_name_translation.csv",
    ]

    # Establish a connection to the Google Cloud BigQuery client
    client = bigquery.Client()

    # Define the GCS bucket name
    bucket_name = os.environ.get("GCS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable not set.")

    # Loop through each filename
    for filename in csv_files:
        # Construct the full GCS path to the CSV
        gcs_path = f"gs://{bucket_name}/{filename}"

        # Read the CSV file into a pandas DataFrame directly from GCS
        df = pandas.read_csv(gcs_path)

        # Determine the correct destination table ID
        table_id = f"olist_ecommerce.{filename.replace('.csv', '')}"

        # Configure and run a load job
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_APPEND",
            autodetect=True,  # Use autodetect for schema
        )

        job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()  # Wait for the job to complete

        # Print a status message
        print(f"Loaded data from {filename} to {table_id}")

if __name__ == "__main__":
    main()