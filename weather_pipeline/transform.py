"""
=============================================================================
Author: Kiran
Website: kirananalyst.com
Bio: I have experience in turning raw data into actionable insights 
and building robust process automation pipelines.
=============================================================================
This module handles transforming the raw JSON time-series arrays into a structured 
Pandas DataFrame suitable for inserting into PostgreSQL.
"""

import pandas as pd

def transform_data(raw_hourly_data, loc_metadata):
    """
    Takes the raw hourly dictionary of arrays from Open-Meteo and the city's 
    location metadata, and converts it into a clean Pandas DataFrame.
    """
    # If the API returned empty data, return an empty DataFrame
    if not raw_hourly_data or 'time' not in raw_hourly_data:
        return pd.DataFrame()
        
    # Open-Meteo returns hourly data as a dictionary of arrays.
    # Pandas can instantly turn this dictionary into a full DataFrame table!
    df = pd.DataFrame(raw_hourly_data)
    
    # Add our constant location metadata to every single row in the DataFrame
    df['city'] = loc_metadata['city']
    df['state'] = loc_metadata['state']
    df['country'] = loc_metadata['country']
    df['lat'] = loc_metadata['lat']
    df['lon'] = loc_metadata['lon']
    df['source'] = 'Open-Meteo Archive API'
    
    # 1. Handle dates and times
    # The API returns 'time' like '2026-09-20T19:00', so we split it into Date and Time
    df['time'] = pd.to_datetime(df['time'])
    df['observation_date'] = df['time'].dt.date
    df['observation_time'] = df['time'].dt.time
    
    # 2. Rename API columns to perfectly match our PostgreSQL database schema
    df = df.rename(columns={
        'temperature_2m': 'temperature',
        'relative_humidity_2m': 'humidity',
        'wind_speed_10m': 'wind_speed'
    })
    
    # 3. Handle missing values
    # If there is no temperature reading for an hour, we drop that row
    df = df.dropna(subset=['temperature'])
    
    # 4. Select and order columns perfectly to match the exact order of the DB table
    columns_to_load = [
        'city', 'state', 'country', 'lat', 'lon',
        'observation_date', 'observation_time',
        'temperature', 'humidity', 'precipitation',
        'wind_speed', 'weather_code', 'source'
    ]
    
    # Return the beautifully cleaned and ordered data
    clean_df = df[columns_to_load]
    return clean_df
