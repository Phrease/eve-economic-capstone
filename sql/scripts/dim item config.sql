TRUNCATE TABLE dim_item CASCADE;

COPY dim_item (type_id, item_name, item_category)
FROM 'C:/Users/durki/OneDrive/Desktop/MIS581/data/dim_item.csv'
DELIMITER ','
CSV HEADER;