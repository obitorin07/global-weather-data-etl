"""
=============================================================================
Author: Kiran
Website: kirananalyst.com
Bio: I have experience in turning raw data into actionable insights 
and building robust process automation pipelines.
=============================================================================
This is the MASSIVE Historical ETL script. 
It pulls 2 years of hourly data for 350 global cities. 
Run this exactly ONCE to seed your database with millions of rows.
"""

from extract import get_global_cities, extract_historical_weather_for_city
from transform import transform_data
from load import load_to_postgres
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

def run_historical_pipeline():
    start_time = time.time()
    
    print("====================================================")
    print("   MASSIVE HISTORICAL WEATHER ETL PIPELINE RUNNING  ")
    print("====================================================")
    
    # 1. Generate our dynamic list of 350 global cities
    print("Finding the top 350 cities in the world...")
    cities = get_global_cities(limit=350)
    
    # 2. Calculate the 2-year exact date window
    end_date = datetime.now().date()
    start_date = end_date - relativedelta(years=2)
    end_date_str = end_date.strftime('%Y-%m-%d')
    start_date_str = start_date.strftime('%Y-%m-%d')
    print(f"Timeframe: {start_date_str} to {end_date_str}")
    
    total_inserted_rows = 0
    
    # 3. The Instant-Append Loop
    # Instead of hoarding data in memory, we extract, transform, and load 
    # one city at a time. This keeps memory usage low and instantly populates the DB!
    for i, city_meta in enumerate(cities):
        try:
            print(f"\n[{i+1}/{len(cities)}] Processing {city_meta['city']}, {city_meta['state']}, {city_meta['country']}...")
            
            # EXTRACT
            raw_data = extract_historical_weather_for_city(city_meta, start_date_str, end_date_str)
            if not raw_data:
                continue
                
            # TRANSFORM
            clean_df = transform_data(raw_data, city_meta)
            if clean_df.empty:
                continue
                
            # LOAD
            load_to_postgres(clean_df)
            
            total_inserted_rows += len(clean_df)
            print(f"   -> Inserted {len(clean_df)} rows. Total DB rows: {total_inserted_rows}")
            
        except Exception as e:
            print(f"Failed to process {city_meta['city']} - {e}")
            continue

    end_time = time.time()
    print("====================================================")
    print(f"   PIPELINE COMPLETE (Took {round(end_time - start_time, 2)} seconds)")
    print(f"   TOTAL ROWS LOADED: {total_inserted_rows}")
    print("====================================================")

if __name__ == "__main__":
    run_historical_pipeline()
