-- dbt_project/models/staging/stg_orders.sql

-- This model selects from your REAL source data
-- and does some light cleaning.

SELECT
    order_id,
    customer_id,
    order_status,
    order_purchase_timestamp,
    order_delivered_customer_date
FROM
    -- This uses the source we defined in sources.yml
    {{ source('olist_ecommerce', 'olist_orders_dataset') }}