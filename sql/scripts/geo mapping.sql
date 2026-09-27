COPY dim_geography (system_id, region_id, system_name, region_name, is_central_hub)
FROM 'C:/Users/durki/OneDrive/Desktop/MIS581/data/dim_geography.csv'
DELIMITER ','
CSV HEADER;

select *
from dim_geography
where system_name = 'Jita'
limit 5;