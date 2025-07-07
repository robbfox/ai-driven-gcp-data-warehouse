-- models/marts/dim_customers.sql

WITH customers AS (
    SELECT
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix,
        customer_city,
        customer_state
    FROM {{ ref('stg_customers') }}
),

geolocations AS (
    SELECT

        geolocation_zip_code_prefix,
        geolocation_lat AS latitude,
        geolocation_lng AS longitude
    FROM {{ ref('stg_geolocations') }}
),

-- First, let's get the latest known location for each unique customer
customer_locations AS (
    SELECT
        c.customer_unique_id,
        c.customer_city,
        c.customer_state,
        g.latitude,
        g.longitude,
        -- We rank each customer's orders to find their most recent one
        ROW_NUMBER() OVER (PARTITION BY c.customer_unique_id ORDER BY c.customer_id DESC) as rn
    FROM
        customers c
    LEFT JOIN geolocations g ON c.customer_zip_code_prefix = g.geolocation_zip_code_prefix
)

SELECT
    customer_unique_id,
    customer_city,
    customer_state,
    latitude,
    longitude
FROM customer_locations
-- This ensures we get one row per unique customer, based on their latest order's location
WHERE rn = 1