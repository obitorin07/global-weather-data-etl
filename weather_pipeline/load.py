"""
=============================================================================
Author: Kiran
Website: kirananalyst.com
Bio: I have experience in turning raw data into actionable insights 
and building robust process automation pipelines.
=============================================================================
This module handles loading the cleaned Pandas DataFrame efficiently 
into our PostgreSQL database.
"""

import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

# Load credentials from the hidden .env file
load_dotenv()
DB_NAME = os.getenv('db_name')
DB_USER = os.getenv('db_user', 'postgres')
DB_PASSWORD = os.getenv('db_password')
DB_HOST = os.getenv('db_host')
DB_PORT = os.getenv('db_port')

def load_to_postgres(df):
    """
    Connects to Postgres and efficiently bulk-inserts our cleaned DataFrame.
    """
    if df.empty:
        return
        
    conn = None
    try:
        # Establish connection to the local PostgreSQL database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        
        # Convert the Pandas DataFrame into a list of tuples, which is the 
        # format psycopg2 requires for insertion.
        tuples = [tuple(x) for x in df.to_numpy()]
        
        # Specify the exact columns we are inserting data into
        cols = ','.join(['city', 'state', 'country', 'latitude', 'longitude', 
                         'observation_date', 'observation_time', 'temperature', 
                         'humidity', 'precipitation', 'wind_speed', 'weather_code', 'source'])
        
        # The SQL INSERT statement with our new UPSERT (ON CONFLICT) logic
        query = f"INSERT INTO weather_data({cols}) VALUES %s ON CONFLICT (city, observation_date, observation_time) DO NOTHING"
        
        # Using execute_values is dramatically faster than a standard loop insert.
        # It batches rows together to optimize network round-trips to the DB.
        execute_values(cur, query, tuples, page_size=10000)
        
        # Save (commit) the changes permanently to the database
        conn.commit()
        
        cur.close()
    except Exception as e:
        print(f"Error loading data into DB: {e}")
        # Rollback the transaction if it failed so we don't insert corrupted data
        if conn:
            conn.rollback()
    finally:
        # Always remember to close your database connection!
        if conn is not None:
            conn.close()
