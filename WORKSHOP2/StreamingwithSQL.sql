CREATE MATERIALIZED VIEW calcualtion as SELECT
    tz1.zone AS pickup_location,
    tz2.zone AS dropoff_location,
    MIN(tpep_dropoff_datetime - tpep_pickup_datetime) AS min_trip_time,
    MAX(tpep_dropoff_datetime - tpep_pickup_datetime) AS max_trip_time,
    AVG(tpep_dropoff_datetime - tpep_pickup_datetime) AS avg_trip_time
FROM trip_data AS t
INNER JOIN taxi_zone AS tz1 ON t.pulocationid = tz1.location_id
INNER JOIN taxi_zone AS tz2 ON t.dolocationid = tz2.location_id
GROUP BY tz1.zone, tz2.zone;



CREATE MATERIALIZED VIEW MAXavg_trip_time AS SELECT
    pickup_location,
    dropoff_location,
    MAX(avg_trip_time) AS max_avg_trip_time
FROM calcualtion
GROUP BY pickup_location, dropoff_location
ORDER BY max_avg_trip_time DESC
LIMIT 1;
{# 
pickup_location | dropoff_location | max_avg_trip_time
-----------------+------------------+-------------------
Yorkville East  | Steinway         | 23:59:33
#}


CREATE MATERIALIZED VIEW Countofmaxavg AS
SELECT * FROM calcualtion WHERE pickup_location = 'Yorkville East' AND dropoff_location = 'Steinway' ;

{# 
1
#}



WITH LatestPickup AS (
    SELECT MAX(tpep_pickup_datetime) AS latest_pickup
    FROM trip_data
)
SELECT
    tz1.Zone AS pickup_location,
    COUNT(*) AS pickup_count
FROM trip_data AS t
INNER JOIN taxi_zone AS tz1 ON t.pulocationid = tz1.location_id
CROSS JOIN LatestPickup
WHERE t.tpep_pickup_datetime >= (latest_pickup - INTERVAL '17 hours')
GROUP BY tz1.zone
ORDER BY pickup_count DESC
LIMIT 3;


{# 
   pickup_location   | pickup_count
---------------------+--------------
 LaGuardia Airport   |           19
 JFK Airport         |           17
 Lincoln Square East |           17
 #}