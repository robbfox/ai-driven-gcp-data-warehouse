SELECT
    geolocation_zip_code_prefix,
    geolocation_lat,
    geolocation_lng,
    geolocation_city,
    geolocation_state

FROM
    {{ source('olist_ecommerce', 'olist_geolocation_dataset') }}