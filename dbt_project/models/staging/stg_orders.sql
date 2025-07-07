-- dbt_project/models/staging/stg_orders.sql

-- This model selects from your REAL source data
-- and does some light cleaning.

SELECT
    order_id,
    customer_id,
    order_status,
    order_purchase_timestamp,
    order_delivered_customer_date,
    order_approved_at,
    order_delivered_carrier_date,
    order_estimated_delivery_date

FROM
    -- This uses the source we defined in sources.yml
    {{ source('olist_ecommerce', 'olist_orders_dataset') }}