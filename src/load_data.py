# src/load_data.py

import os
from google.cloud import bigquery
from google.cloud.exceptions import NotFound

def main():
    """
    Loads data from GCS files into corresponding BigQuery tables.
    This script tells BigQuery to load data directly from GCS.
    """
    print("--- Starting BigQuery data loading script ---")

    try:
        # Get environment variables
        project_id = os.environ.get("GCP_PROJECT_ID")
        bucket_name = os.environ.get("GCS_BUCKET_NAME")
        dataset_id = "olist_ecommerce"

        if not project_id or not bucket_name:
            print("ERROR: GCP_PROJECT_ID or GCS_BUCKET_NAME env variables are not set.")
            exit(1)

        print(f"Project ID: {project_id}")
        print(f"GCS Bucket: {bucket_name}")
        print(f"BigQuery Dataset: {dataset_id}")

        # Initialize the BigQuery Client
        client = bigquery.Client(project=project_id)

        # List of CSV filenames to load.
        # Make sure these filenames EXACTLY match the files in your GCS bucket.
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

        # Loop through each file and load it into the corresponding table
        for filename in csv_files:
            table_name = filename.replace('.csv', '')
            print(f"\nProcessing: {filename} -> {table_name}")

            # Construct the full GCS URI for the source file
            uri = f"gs://{bucket_name}/{filename}"

            # Construct the full BigQuery table reference
            table_ref = client.dataset(dataset_id).table(table_name)
            
            # Configure the load job. We are NOT using autodetect.
            # We trust the schema created by Terraform.
            job_config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.CSV,
                # Assumes the first row of your CSV is a header.
                # If not, set this to 0.
                skip_leading_rows=1,
                # This will replace the table content on every run.
                # Use "WRITE_APPEND" if you want to add to it instead.
                write_disposition="WRITE_TRUNCATE",
                allow_quoted_newlines=True,
                max_bad_records=1000 
            )

            # Start the load job
            load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config)
            print(f"  Starting job {load_job.job_id} to load {uri} into {table_name}.")

            load_job.result()  # Wait for the job to complete.

            # Check the results
            destination_table = client.get_table(table_ref)
            print(f"  SUCCESS: Loaded {destination_table.num_rows} rows.")

    except NotFound as e:
        print(f"!!!!!! ERROR: A resource was not found. Did Terraform run correctly? Is the file in GCS? Details: {e}")
        exit(1)
    except Exception as e:
        print(f"!!!!!! AN UNEXPECTED ERROR OCCURRED: {e}")
        exit(1)

    print("\n--- Data loading script finished successfully! ---")

if __name__ == "__main__":
    main()