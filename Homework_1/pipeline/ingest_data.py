import pandas as pd
from sqlalchemy import create_engine
import time
import click

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default=2025, type=int, help='Year of the data')
@click.option('--month', default=11, type=int, help='Month of the data')
@click.option('--target-table', default='green_taxi_data', help='Target table name')
def ingest_data(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, target_table):
    
    # 1. Формуємо URL динамічно (додаємо 0 перед місяцем, якщо він < 10)
    taxi_url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{year}-{month:02d}.parquet'
    zones_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv'

    # 2. Створюємо підключення
    connection_string = f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
    engine = create_engine(connection_string)

    # 3. Завантаження даних таксі
    print(f"Connecting to database at {pg_host}...")
    print(f"Downloading taxi data for {year}-{month:02d}...")
    
    try:
        t_start = time.time()
        df = pd.read_parquet(taxi_url)
        
        # Записуємо в базу (replace видаляє стару таблицю, якщо вона була)
        df.to_sql(name=target_table, con=engine, if_exists='replace', chunksize=10000)
        
        t_end = time.time()
        print(f"Success! {len(df)} rows loaded into '{target_table}' in {t_end - t_start:.2f}s")
        
    except Exception as e:
        print(f"Error during taxi ingestion: {e}")

    # 4. Завантаження зон (завжди в одну й ту саму таблицю)
    print("Downloading zone lookup data...")
    try:
        df_z = pd.read_csv(zones_url)
        df_z.to_sql(name='zone_lookup', con=engine, if_exists='replace', index=False)
        print(f"Success! {len(df_z)} zones loaded into 'zone_lookup'")
    except Exception as e:
        print(f"Error during zone ingestion: {e}")

if __name__ == '__main__':
    ingest_data()