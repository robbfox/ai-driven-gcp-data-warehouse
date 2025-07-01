
import pandas
from unittest.mock import MagicMock, patch
from src.load_data import main

# Sample DataFrame to be returned by the mocked pandas.read_csv
sample_df = pandas.DataFrame({'col1': [1, 2], 'col2': ['A', 'B']})

@patch('src.load_data.bigquery.Client')
@patch('src.load_data.pandas.read_csv')
def test_load_data(mock_read_csv, mock_bigquery_client):
    """
    Tests the main data loading script.
    """
    # Set up the mock for pandas.read_csv to return a sample DataFrame
    mock_read_csv.return_value = sample_df

    # Set up the mock for the BigQuery client
    mock_client_instance = MagicMock()
    mock_bigquery_client.return_value = mock_client_instance

    # Run the main script
    main()

    # Verify that the BigQuery client's load_table_from_dataframe method was called 9 times
    assert mock_client_instance.load_table_from_dataframe.call_count == 9

    # Verify that the data is loaded to the correct tables
    expected_table_ids = [
        "olist_ecommerce.olist_customers_dataset",
        "olist_ecommerce.olist_geolocation_dataset",
        "olist_ecommerce.olist_order_items_dataset",
        "olist_ecommerce.olist_order_payments_dataset",
        "olist_ecommerce.olist_order_reviews_dataset",
        "olist_ecommerce.olist_orders_dataset",
        "olist_ecommerce.olist_products_dataset",
        "olist_ecommerce.olist_sellers_dataset",
        "olist_ecommerce.product_category_name_translation",
    ]

    # Get the actual table IDs from the mock calls
    actual_table_ids = [
        call.args[1] for call in mock_client_instance.load_table_from_dataframe.call_args_list
    ]

    # Sort the lists to ensure the comparison is order-independent
    assert sorted(actual_table_ids) == sorted(expected_table_ids)
