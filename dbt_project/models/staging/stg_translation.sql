-- models/staging/stg_translation.sql
SELECT
    -- Clean the BOM character here!
    REPLACE(product_category_name, '\ufeff', '') as product_category_name,
    product_category_name_english
FROM
    {{ source('olist_ecommerce', 'product_category_name_translation') }}
WHERE
    -- Your excellent cleaning logic
    product_category_name_english IS NOT NULL AND product_category_name_english != ''