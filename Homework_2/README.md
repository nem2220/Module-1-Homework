# Module 1 Homework: Kestra Backfill & GCP (BigQuery / Cloud Storage)
**Course:** Data Engineering Zoomcamp 2026  
**Batch:** 2026

This repository contains the flows and instructions to run a Kestra-based backfill for NYC taxi data (Green & Yellow). It also includes guidance for using the GCP Console (BigQuery & Cloud Storage) to answer the homework questions.

---

## 🚀 Infrastructure Setup

### 1. Start local Kestra stack
Start the local stack (for example with Docker Compose in the `Homework_2` folder) so Kestra is available to run flows and backfills.

```bash
docker-compose up -d
```

### 2. Set the GCP secret in Kestra
Use `flows/01_gcp_kv.yaml` in the Kestra UI to create a key-value secret that stores your encoded GCP service account (do not commit raw `service-account.json`).

If you need to encode your local service account file for the local stack, run the following to append the encoded value to `.env_encoded`:

```bash
echo SECRET_GCP_SERVICE_ACCOUNT=$(cat service-account.json | base64 -w 0) >> .env_encoded
```

Store `.env_encoded` securely and do not commit it to the repository.

### 3. Provision cloud resources (optional)
Use `flows/02_gcp_setup.yaml` to provision GCP resources required for the backfill, or create them manually via the GCP Console.

This starts Kestra and any local dependencies required to run and test the flows.

---

## Flows overview 🔁
- `01_gcp_kv.yaml` — create a Kestra key-value secret that stores the encoded GCP service account.
- `02_gcp_setup.yaml` — provision GCP resources required for the backfill (project, buckets, policies).
- `03_gcp_taxi_backfill.yaml` — scheduled backfill flow that downloads taxi CSVs from DataTalksClub releases and writes to GCS/BigQuery.

The flow downloads release artifacts using the template:

```
https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{{inputs.taxi}}/{{render(vars.file)}}.gz
```

`vars.file` renders to names such as `green_tripdata_2020-04.csv`.

---

## 📊 SQL Analysis & Solutions
Below are concise BigQuery SQL snippets you can paste into the **BigQuery** Console to answer Q1–Q5 and a YAML snippet for Q6.

### Q1 — Uncompressed file size for `yellow_tripdata_2020-12.csv`
If the CSV was loaded into BigQuery as `yellow_tripdata_202012`, check table metadata:

```sql
SELECT table_name, row_count, size_bytes
FROM `your_project.your_dataset`.INFORMATION_SCHEMA.TABLES
WHERE table_name = 'yellow_tripdata_202012';
```

### Q2 — Rendered value of `vars.file` when `taxi=green`, `year=2020`, `month=04`
- **Answer:** `green_tripdata_2020-04.csv`.

### Q3 — Total rows for Yellow taxi in 2020
Exact count across monthly wildcard tables:

```sql
SELECT COUNT(*) AS total_rows
FROM `your_project.your_dataset.yellow_tripdata_*`
WHERE _TABLE_SUFFIX BETWEEN '202001' AND '202012';
```

Cheaper alternative (metadata):

```sql
SELECT SUM(row_count) AS approx_total_rows
FROM `your_project.your_dataset`.INFORMATION_SCHEMA.TABLES
WHERE table_name LIKE 'yellow_tripdata_%'
  AND REGEXP_EXTRACT(table_name, r'(\d{6})$') BETWEEN '202001' AND '202012';
```

### Q4 — Total rows for Green taxi in 2020
Replace `yellow` with `green` in Q3 queries:

```sql
SELECT COUNT(*) AS total_rows
FROM `your_project.your_dataset.green_tripdata_*`
WHERE _TABLE_SUFFIX BETWEEN '202001' AND '202012';
```

### Q5 — Rows in `yellow_tripdata_2021-03`
If monthly tables use suffix `202103`:

```sql
SELECT COUNT(*) AS march_2021_rows
FROM `your_project.your_dataset.yellow_tripdata_*`
WHERE _TABLE_SUFFIX = '202103';
```

### Q6 — Configure timezone to New York in a Schedule trigger
Add `timezone: "America/New_York"` to the trigger block, for example:

```yaml
triggers:
  - id: daily_backfill
    type: schedule
    cron: "0 0 * * *"
    timezone: "America/New_York"
```

---

## 🛠 Tech Stack
* **Kestra** — orchestrates scheduled flows and backfills.
* **Google Cloud (BigQuery & Cloud Storage)** — data storage and querying.
* **Docker & Docker Compose** — local Kestra stack and dependencies.

---

If you'd like saved BigQuery queries or example Kestra backfill JSON payloads added to this repo, say which and I'll add them.