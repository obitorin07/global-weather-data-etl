"""
=============================================================================
Author: Kiran
Website: kirananalyst.com
Bio: I have experience in turning raw data into actionable insights 
and building robust process automation pipelines.
=============================================================================
This is the INCREMENTAL Daily ETL script.
Instead of pulling years of data, you run this script to pull just one or two
days of data and instantly append it to your existing millions of rows.
"""

from extract import get_global_cities, extract_historical_weather_for_city
from transform import transform_data
from load import load_to_postgres
import time

# =======================================================
# MANUALLY CHANGE THESE DATES TO PULL INCREMENTAL DATA
# Format must be YYYY-MM-DD
# =======================================================
START_DATE = "2026-09-18"
END_DATE = "2026-09-19"

def run_incremental_pipeline():
    start_time = time.time()
    
    print("====================================================")
    print("   INCREMENTAL DAILY WEATHER ETL PIPELINE RUNNING   ")
    print("====================================================")
    print(f"Timeframe: {START_DATE} to {END_DATE}")
    
    # 1. Generate our dynamic list of 150 global cities
    print("Finding the top 150 cities in the world...")
    cities = get_global_cities(limit=150)
    
    total_inserted_rows = 0
    
    # 2. The Instant-Append Loop
    for i, city_meta in enumerate(cities):
        try:
            print(f"[{i+1}/{len(cities)}] Updating {city_meta['city']}, {city_meta['state']}, {city_meta['country']}...")
            
            # EXTRACT
            raw_data = extract_historical_weather_for_city(city_meta, START_DATE, END_DATE)
            if not raw_data:
                continue
                
            # TRANSFORM
            clean_df = transform_data(raw_data, city_meta)
            if clean_df.empty:
                continue
                
            # LOAD
            load_to_postgres(clean_df)
            
            total_inserted_rows += len(clean_df)
            
        except Exception as e:
            print(f"Failed to process {city_meta['city']} - {e}")
            continue

    end_time = time.time()
    print("====================================================")
    print(f"   UPDATE COMPLETE (Took {round(end_time - start_time, 2)} seconds)")
    print(f"   TOTAL NEW ROWS LOADED: {total_inserted_rows}")
    print("====================================================")

if __name__ == "__main__":
    run_incremental_pipeline()
