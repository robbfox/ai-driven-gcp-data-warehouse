-- models/analytics/fct_order_items.sql -- CORRECTED VERSION

with orders as (
    select * from {{ ref('stg_orders') }}
),
order_items as (
    select * from {{ ref('stg_order_items') }}
),
order_payments as (
    select * from {{ ref('stg_order_payments') }}
),
customers as (
    select * from {{ ref('stg_customers') }}
)

select
    -- Primary Key
    order_items.order_item_id,

    -- Foreign Keys
    orders.order_id,
    orders.customer_id, -- Keep the original customer_id
    customers.customer_unique_id, -- <<< THE NEW, CRUCIAL FOREIGN KEY
    order_items.product_id,
    order_items.seller_id,
    
    -- Timestamps & Status
    orders.order_status,
    orders.order_purchase_timestamp,
    orders.order_approved_at,
    orders.order_delivered_carrier_date,
    orders.order_delivered_customer_date,
    orders.order_estimated_delivery_date,

    -- Financials
    order_items.price as item_price,
    order_items.freight_value as item_freight_value,
    
    -- We can calculate a proportional payment value per item for more accuracy
    -- Handle potential division by zero if total_price is 0
    (order_items.price / NULLIF(total_order_price.total_price, 0)) * order_payments.payment_value as proportional_item_payment_value

from order_items
left join orders on order_items.order_id = orders.order_id
left join order_payments on orders.order_id = order_payments.order_id
-- Join to customers to get the unique ID
left join customers on orders.customer_id = customers.customer_id
left join (
    -- Subquery to get total price per order to calculate proportions
    select 
        order_id, 
        sum(price) as total_price 
    from order_items 
    group by 1
) as total_order_price on orders.order_id = total_order_price.order_id