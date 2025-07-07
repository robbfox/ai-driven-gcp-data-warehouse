{{
    dbt_utils.date_spine(
        datepart="day",
        start_date="cast('2016-09-01' as date)",
        end_date="date_add(cast('2018-10-17' as date), interval 1 year)"
    )
}}