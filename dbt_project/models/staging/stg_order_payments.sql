-- dbt_project/models/staging/stg_order_payments.sql

SELECT
    order_id,
    payment_sequential,
    payment_type,
    payment_installments,
    payment_value
FROM
    {{ source('olist_ecommerce', 'olist_order_payments_dataset') }}