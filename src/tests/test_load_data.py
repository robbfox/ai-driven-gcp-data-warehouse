import os
from unittest.mock import MagicMock, patch
from src.load_data import main
from google.cloud import bigquery

@patch.dict(os.environ, {"GCP_PROJECT_ID": "test-project", "GCS_BUCKET_NAME": "test-bucket"}, clear=True)
@patch("src.load_data.bigquery.Client")
def test_load_data(mock_bigquery_client):
    """
    Tests the main data loading script to ensure it calls BigQuery correctly.
    """
    # Arrange: Set up mocks for BigQuery client and the load job
    mock_client_instance = MagicMock()
    mock_bigquery_client.return_value = mock_client_instance

    # Mock the dataset and table methods to return a MagicMock with a settable table_id
    mock_dataset = MagicMock()
    mock_client_instance.dataset.return_value = mock_dataset

    def mock_table_factory(table_name):
        mock_table_ref = MagicMock()
        mock_table_ref.table_id = table_name  # Set the table_id attribute
        return mock_table_ref

    mock_dataset.table.side_effect = mock_table_factory

    mock_job = MagicMock()
    mock_client_instance.load_table_from_uri.return_value = mock_job

    mock_table = MagicMock()
    mock_table.num_rows = 123  # Mock number of rows loaded
    mock_client_instance.get_table.return_value = mock_table

    # Act: Run the main script
    main()

    # Assert: Verify the interactions with the BigQuery client
    assert mock_client_instance.load_table_from_uri.call_count == 9
    assert mock_job.result.call_count == 9  # Ensure we wait for each job to complete

    # Define expected files and corresponding tables
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
    
    # Check that the correct URIs and table references were used
    calls = mock_client_instance.load_table_from_uri.call_args_list
    actual_uris = sorted([call.args[0] for call in calls])
    expected_uris = sorted([f"gs://test-bucket/{fname}" for fname in csv_files])
    assert actual_uris == expected_uris

    actual_table_ids = sorted([call.args[1].table_id for call in calls])
    expected_table_ids = sorted([fname.replace(".csv", "") for fname in csv_files])
    assert actual_table_ids == expected_table_ids

    # Verify the job configuration for each call
    for call in calls:
        job_config = call.kwargs["job_config"]
        assert isinstance(job_config, bigquery.LoadJobConfig)
        assert job_config.source_format == bigquery.SourceFormat.CSV
        assert job_config.skip_leading_rows == 1
        assert job_config.write_disposition == "WRITE_TRUNCATE"