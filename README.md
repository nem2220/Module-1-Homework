# Module-1-Homework
data engineering zoomcamp

Start Services with Docker Compose
docker-compose up

Build the Docker Image
docker build -t taxi_ingest:v001 .


Running the Ingestion Script with Docker Compose
docker run -it \
    --network=pipeline_default \
    taxi_ingest:v001 \
    --pg-user=root \
    --pg-pass=root \
    --pg-host=pgdatabase \
    --pg-db=ny_taxi \
    --year=2025 \
    --month=11 \
    --target-table=green_taxi_data

Question 3. Counting short trips
For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile?

SELECT 
    COUNT(1)
FROM 
    green_taxi_data
WHERE 
    lpep_pickup_datetime >= '2025-11-01' 
    AND lpep_pickup_datetime < '2025-12-01'
    AND trip_distance <= 1.0;

Question 4. Longest trip for each day
Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors).
Use the pick up time for your calculations.

SELECT 
    lpep_pickup_datetime::DATE AS pickup_day,
    MAX(trip_distance) AS max_distance
FROM 
    green_taxi_data
WHERE 
    trip_distance < 100
GROUP BY 
    pickup_day
ORDER BY 
    max_distance DESC
LIMIT 1;

Question 5. Biggest pickup zone
Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?
SELECT 
    z."Zone" AS pickup_zone,
    SUM(t.total_amount) AS total_amount_sum
FROM 
    green_taxi_data t
JOIN 
    zone_lookup z ON t."PULocationID" = z."LocationID"
WHERE 
    t.lpep_pickup_datetime::DATE = '2025-11-18'
GROUP BY 
    1
ORDER BY 
    2 DESC
LIMIT 1;

Question 6. Largest tip
For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?
Note: it's tip, not trip. We need the name of the zone, not the ID.
SELECT 
    do_z."Zone" AS dropoff_zone,
    MAX(t.tip_amount) AS max_tip
FROM 
    green_taxi_data t
JOIN 
    zone_lookup pu_z ON t."PULocationID" = pu_z."LocationID"
JOIN 
    zone_lookup do_z ON t."DOLocationID" = do_z."LocationID"
WHERE 
    pu_z."Zone" = 'East Harlem North'
    AND t.lpep_pickup_datetime >= '2025-11-01' 
    AND t.lpep_pickup_datetime < '2025-12-01'
GROUP BY 
    1
ORDER BY 
    2 DESC
LIMIT 1;