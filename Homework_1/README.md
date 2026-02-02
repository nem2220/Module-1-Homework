cat <<EOF > README.md
# Module 1 Homework: Docker, SQL, and Terraform
**Course:** Data Engineering Zoomcamp 2026  
**Batch:** 2026

This repository contains the solutions for Homework #1. The project demonstrates how to containerize an ingestion pipeline (ETL) using Docker and perform SQL analysis on New York City taxi data.

---

## 🚀 Infrastructure Setup

### 1. Start the Database
Use Docker Compose to launch PostgreSQL and pgAdmin in the background:
```bash
docker-compose up -d
```

### 2. Build the Ingestion Image
Build a custom Docker image that contains the Python ETL script:
```bash
docker build -t taxi_ingest:v001 .
```

### 3. Run the Ingestion Pipeline
Execute the container to download and upload Green Taxi data for November 2025:
```bash
docker run -it \
    --network=pipeline_default \
    taxi_ingest:v001 \
    --pg-user=root \
    --pg-pass=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --year=2025 \
    --month=11 \
    --target-table=green_taxi_data
```

---

## 📊 SQL Analysis & Solutions

### Question 3: Counting short trips
*How many trips in November 2025 had a trip distance of less than or equal to 1 mile?*

```sql
SELECT 
    COUNT(1)
FROM 
    green_taxi_data
WHERE 
    lpep_pickup_datetime >= '2025-11-01' 
    AND lpep_pickup_datetime < '2025-12-01'
    AND trip_distance <= 1.0;
```

### Question 4: Longest trip for each day
*Which was the pick-up day with the longest trip distance? (Considering trips < 100 miles).*

```sql
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
```

### Question 5: Biggest pickup zone
*Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?*

```sql
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
```

### Question 6: Largest tip
*For passengers picked up in "East Harlem North" in November 2025, which drop-off zone had the largest tip?*

```sql
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
```

---

## 🛠 Tech Stack
* **Docker & Docker Compose** — Infrastructure orchestration.
* **Python (Pandas, SQLAlchemy, Click)** — ETL logic and data processing.
* **PostgreSQL** — Relational database for data storage.
* **SQL** — Data analysis and transformations.
EOF