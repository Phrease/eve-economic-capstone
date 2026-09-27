-- Date Dimensions
-- Extracting date components from the interval timestamp variable
CREATE TABLE dim_date (
	date_key INT PRIMARY KEY,
	full_date DATE NOT NULL,
	year INT NOT NULL,
	month INT NOT NULL,
	day INT NOT NULL
);

-- Geography Dimensions
-- Maps the categorical identifiers to specific systems and regions
CREATE TABLE dim_geography (
	system_id INT PRIMARY KEY,
	region_id INT NOT NULL,
	system_name VARCHAR(100),
	region_name VARCHAR (100),
	is_central_hub BOOLEAN
);

-- Item Dimensions
-- Maps the categorical identifiers to item classifications and manufacturing
CREATE TABLE dim_item (
	type_id INT PRIMARY KEY,
	item_name VARCHAR(255),
	item_vategory VARCHAR(100)
);

-- Market and Combat Events Fact Table
-- Unifies the disparate market telemetry and combat destruction logs
CREATE TABLE fact_market_events (
	transaction_id VARCHAR(255) PRIMARY KEY,
	date_key INT REFERENCES dim_date(date_key),
	event_timestamp TIMESTAMP NOT NULL,
	is_buy_order BOOLEAN,
	type_id INT REFERENCES dim_item(type_id),
	system_id INT REFERENCES dim_geography(system_id),
	price_isk NUMERIC (24, 2),
	volume_total BIGINT,
	event_category VARCHAR(50),
	destroyed_isk NUMERIC (24, 2)
);