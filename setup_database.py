import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get DB credentials from environment variables
DB_NAME = os.getenv('db_name')
DB_USER = os.getenv('db_user', 'postgres') # Assuming 'postgres' if not in .env
DB_PASSWORD = os.getenv('db_password')
DB_HOST = os.getenv('db_host')
DB_PORT = os.getenv('db_port')

def create_tables():
    """ Connect to the PostgreSQL database server and create tables """
    commands = (
        """
        CREATE TABLE IF NOT EXISTS weather_data (
            id SERIAL PRIMARY KEY,
            city VARCHAR(100),
            state VARCHAR(100),
            country VARCHAR(100),
            latitude DECIMAL(9, 6),
            longitude DECIMAL(9, 6),
            observation_date DATE,
            observation_time TIME,
            temperature DECIMAL(5, 2),
            humidity INTEGER,
            precipitation DECIMAL(5, 2),
            wind_speed DECIMAL(5, 2),
            weather_code INTEGER,
            loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source VARCHAR(100),
            UNIQUE(city, observation_date, observation_time)
        )
        """
    )
    
    conn = None
    try:
        # Connect to the PostgreSQL server
        print(f"Connecting to the PostgreSQL database {DB_NAME}...")
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        
        cur = conn.cursor()
        
        # Create table one by one
        print("Creating table 'weather_data'...")
        cur.execute(commands)
        
        # Close communication with the PostgreSQL database server
        cur.close()
        
        # Commit the changes
        conn.commit()
        print("Table created successfully!")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL or creating table:")
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")

if __name__ == '__main__':
    create_tables()
