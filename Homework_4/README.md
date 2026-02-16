# Module 4 Homework: Analytics Engineering with dbt

This project focuses on transforming raw New York City taxi trip data (NYC TLC) into structured analytical models using dbt Cloud and BigQuery.

## 📋 Steps Taken

### 1. Environment Setup
* **BigQuery:** Created a `trips_data_all` dataset for raw data and `dbt_prod` for final models.
* **Data Ingestion:** Yellow and Green taxi data for 2019-2020 was loaded into BigQuery using Python scripts or data orchestration tools (e.g., Mage/Airflow).
* **dbt Cloud:** Project initialized and connected to a GitHub repository and BigQuery. Target names were configured as `dev` for development and `prod` for production builds.

---

### 2. Model Development

The project follows a three-layer dbt modeling architecture:
1.  **Staging Models:** Cleaning and type-casting raw tables (`stg_green_tripdata`, `stg_yellow_tripdata`).
2.  **Intermediate Models:** Joining and unioning datasets (`int_trips_unioned`).
3.  **Core Models:** Final facts and dimensions (`fct_trips`, `dim_zones`, `fct_monthly_zone_revenue`).



---

### 3. Homework Question Answers

#### Question 1: dbt Lineage and Execution
When running `dbt run --select int_trips_unioned`, dbt will build **only the `int_trips_unioned` model**.
* *Reason:* Without graph operators (like `+` or `*`), dbt ignores upstream or downstream dependencies.

#### Question 2: dbt Tests
When a new value `6` appears in the `payment_type` column where an `accepted_values` test is defined for `[1, 2, 3, 4, 5]`:
* **Result:** dbt will **fail** the test, return a non-zero exit code, and halt the pipeline.

#### Question 3: Record Count in `fct_monthly_zone_revenue`
After running `dbt build --target prod`, we run the following query:
```sql
SELECT count(*) FROM `your_project.dbt_prod.fct_monthly_zone_revenue`