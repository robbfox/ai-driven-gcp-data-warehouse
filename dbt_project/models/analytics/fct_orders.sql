-- This model joins three staging models to create a rich 'fact' table about orders.

-- First, we use Common Table Expressions (CTEs) to import our staging models
WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

order_items AS (
    SELECT * FROM {{ ref('stg_order_items') }} -- You would create this model
),

products AS (
    SELECT * FROM {{ ref('stg_products') }} -- And this one too
)

-- Now, we write our final SELECT statement, joining these CTEs
SELECT
    -- Keys
    oi.order_id,
    oi.order_item_id,
    o.customer_id,
    oi.product_id,
    oi.seller_id,

    -- Timestamps
    o.order_purchase_timestamp,

    -- Product Info (from the products model)
    p.product_category_name,

    -- Financials (from the order_items model)
    oi.price,
    oi.freight_value,
    (oi.price + oi.freight_value) as total_value -- A simple calculated metric

FROM
    order_items AS oi
LEFT JOIN orders AS o
    ON oi.order_id = o.order_id
LEFT JOIN products AS p
    ON oi.product_id = p.product_id