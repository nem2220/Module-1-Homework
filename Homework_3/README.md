# Module 1 — Homework 3: Yellow Taxi → GCS & BigQuery
**Course:** Data Engineering Zoomcamp 2026

This file documents the steps, SQL statements, and answers for Homework 3. The exercise loads NYC Yellow Taxi 2024 data into a Google Cloud Storage (GCS) bucket, registers it as an external table in BigQuery, and performs several analytical queries.

---

## 🚀 Loading data to GCS

- Run the loader script to upload the Parquet files to your GCS bucket:

```bash
python load_yellow_taxi_data.py
```

- Notes:
  - Ensure you have a Service Account with `Storage Admin` (GCS) privileges or are authenticated via the `gcloud` SDK.
  - Update the target bucket name inside `load_yellow_taxi_data.py` before running.

## 📦 Create BigQuery dataset and tables

- Create an external table over the Parquet files in the GCS bucket:

```sql
CREATE OR REPLACE EXTERNAL TABLE `YellowTaxiTrip.external_yellow_taxi`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dezoomcamp_hw3_2025/yellow_tripdata_*.parquet']
);
```

- Copy the external table into a native BigQuery table (optional for faster queries):

```sql
CREATE OR REPLACE TABLE `YellowTaxiTrip.native_yellow_taxi` AS
SELECT * FROM `YellowTaxiTrip.external_yellow_taxi`;
```

---

## 📊 Questions & Solutions

### Question 1 — Counting records
What is the count of records for the 2024 Yellow Taxi data?

```sql
SELECT count(*) FROM `YellowTaxiTrip.native_yellow_taxi`;
```

- Answer: 20,332,093

### Question 2 — Data read estimation
Count the distinct number of `PULocationID` for the full dataset on both tables, and report the estimated bytes read.

```sql
SELECT count(distinct PULocationID) FROM `YellowTaxiTrip.native_yellow_taxi`;
```

- Estimated bytes processed (native table): 155.12 MB

```sql
SELECT count(distinct PULocationID) FROM `YellowTaxiTrip.external_yellow_taxi`;
```

- Estimated bytes processed (external table): 0 B

### Question 3 — Understanding columnar storage
Demonstrate how BigQuery reads only requested columns and how that affects bytes processed.

```sql
SELECT PULocationID FROM `YellowTaxiTrip.native_yellow_taxi`;
-- estimated bytes: 155.12 MB

SELECT PULocationID, DOLocationID FROM `YellowTaxiTrip.native_yellow_taxi`;
-- estimated bytes: 310.24 MB
```

- Explanation: BigQuery is columnar and scans only the columns requested. Selecting two columns reads approximately twice the data of selecting one column.

### Question 4 — Counting zero-fare trips
How many records have `fare_amount = 0`?

```sql
SELECT count(*) FROM `YellowTaxiTrip.native_yellow_taxi`
WHERE fare_amount = 0;
```

- Answer: 8,333

### Question 5 — Partitioning and clustering
What is the best table design if queries always filter by `tpep_dropoff_datetime` and order by `VendorID`?

- Recommended strategy: Partition by `DATE(tpep_dropoff_datetime)` and cluster by `VendorID`.

```sql
CREATE OR REPLACE TABLE `YellowTaxiTrip.optimized_yellow_taxi`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID
AS
SELECT * FROM `YellowTaxiTrip.native_yellow_taxi`;
```

### Question 6 — Partition benefits
Retrieve distinct `VendorID` values between `2024-03-01` and `2024-03-15` (inclusive) and compare estimated bytes processed when querying the full/native table vs. the partitioned table.

```sql
SELECT distinct VendorID FROM `YellowTaxiTrip.native_yellow_taxi`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15 23:59:59';
-- estimated bytes (native table): 310.24 MB

SELECT distinct VendorID FROM `YellowTaxiTrip.optimized_yellow_taxi`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15 23:59:59';
-- estimated bytes (partitioned table): 26.84 MB
```

- Conclusion: Partitioning greatly reduces the amount of data scanned for time-bound queries.

---

## 🛠 Tech Stack
- **Python** — data upload script (`load_yellow_taxi_data.py`)
- **Google Cloud Storage (GCS)** — storage for Parquet files
- **BigQuery** — analytical queries and table storage
