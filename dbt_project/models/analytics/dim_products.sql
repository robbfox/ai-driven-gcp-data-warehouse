-- models/marts/dim_products.sql

WITH products AS (
    SELECT
        product_id,
        product_category_name,
        product_weight_g,
        product_length_cm,
        product_height_cm,
        product_width_cm
    FROM {{ ref('stg_products') }}
),

-- In your stg_translation model, you should have already cleaned the BOM character
translation AS (
    SELECT
        product_category_name,
        product_category_name_english
    FROM {{ ref('stg_translation') }}
)

SELECT
    -- The primary key of the dimension table
    p.product_id,

    -- The clean, user-facing category name
    COALESCE(t.product_category_name_english, 'no_category') as product_category_name_english,

    -- Other useful product attributes
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm

FROM
    products p
LEFT JOIN translation t ON p.product_category_name = t.product_category_name