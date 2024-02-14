CREATE or replace TABLE erpnext-403906.ny_taxi.green_taxi_2022_non_partitioned AS
SELECT
  *,
  PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', lpep_dropoff_datetime) AS lpep_dropoff_datetime_new,
  PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', lpep_pickup_datetime) AS lpep_pickup_datetime_new
FROM
  erpnext-403906.ny_taxi.test2;


ALTER TABLE erpnext-403906.ny_taxi.green_taxi_2022_non_partitioned
DROP COLUMN lpep_pickup_datetime,
DROP COLUMN lpep_dropoff_datetime;

-- Rename columns lpep_pickup_datetime_new and lpep_dropoff_datetime_new
ALTER TABLE erpnext-403906.ny_taxi.green_taxi_2022_non_partitioned
RENAME COLUMN lpep_pickup_datetime_new TO lpep_pickup_datetime,
RENAME COLUMN lpep_dropoff_datetime_new TO lpep_dropoff_datetime;

CREATE OR REPLACE TABLE erpnext-403906.ny_taxi.green_taxi_2022_pickup_partitioned_tripdata
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY PUlocationID AS (
  SELECT * FROM erpnext-403906.ny_taxi.green_taxi_2022_non_partitioned
);


SELECT DISTINCT PULocationID 
FROM erpnext-403906.ny_taxi.green_taxi_2022_non_partitioned
WHERE CAST(lpep_pickup_datetime  AS date) > '2022-06-01' or CAST(lpep_pickup_datetime AS date) <= '2022-06-30';


SELECT DISTINCT PULocationID 
FROM erpnext-403906.ny_taxi.green_taxi_2022_pickup_partitioned_tripdata
WHERE CAST(lpep_pickup_datetime  AS date) > '2022-06-01' or CAST(lpep_pickup_datetime AS date) <= '2022-06-30';

