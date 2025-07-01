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

    # Get the absolute path to the project's root directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(project_root, "data")

    # Loop through each filename
    for filename in csv_files:
        # Construct the full file path to the CSV in the data/ directory
        file_path = os.path.join(data_dir, filename)

        # Read the CSV file into a pandas DataFrame
        df = pandas.read_csv(file_path)

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