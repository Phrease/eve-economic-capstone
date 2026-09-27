INSERT INTO dim_date (date_key, full_date, year, month, day)
SELECT
	TO_CHAR(datum, 'YYYYMMDD')::INT AS date_key,
	datum AS full_date,
	EXTRACT(YEAR FROM datum)::INT AS year,
	EXTRACT(MONTH FROM datum)::INT AS month,
	EXTRACT(DAY FROM datum)::INT AS day
FROM GENERATE_SERIES('2025-01-01'::DATE, '2027-12-31'::DATE, '1 day'::INTERVAL) AS datum;