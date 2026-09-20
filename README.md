<div align="center">
  
# 🌍 Global Weather Data ETL Pipeline

**A fully automated Python & PostgreSQL Data Engineering Pipeline processing millions of records.**

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)

*Architected & Built by [Kiran](https://kirananalyst.com)*

---

</div>

## 📌 Project Overview
This project is an end-to-end Data Engineering **ETL (Extract, Transform, Load)** pipeline built to extract historical weather data for the top global cities, transform the JSON responses into a structured format, and bulk-load the data into a PostgreSQL database for advanced SQL analytics and dashboarding. 

## 🚀 Key Features & Achievements
* **Massive Scale Integration:** Extracted **3.3+ Million rows** of hourly historical weather data across hundreds of major global cities.
* **High-Speed Bulk Loading:** Processed and inserted 3.3M+ records into PostgreSQL in **under 20 minutes** utilizing the highly optimized `psycopg2.extras.execute_values`.
* **Streaming Batch Architecture:** Designed an instant-append memory-efficient loop (Extract -> Transform -> Load per city) rather than hoarding massive arrays in RAM.
* **Intelligent Deduplication:** Implemented database-level `UNIQUE` composite keys and Python-level Upsert (`ON CONFLICT DO NOTHING`) logic to perfectly handle overlapping daily increments.
* **Automated Scalability:** Integrated `geonamescache` for dynamic global city and state targeting, removing the need for hardcoded parameters.
* **Incremental Daily Updates:** Designed two separate execution paths: a heavy-lifting historical script (2-year pull) and a lightweight daily script for seamless incrementing.

## 🗄️ Database Architecture
The data is securely housed in a PostgreSQL instance with the following schema:
```sql
CREATE TABLE weather_data (
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
    UNIQUE(city, observation_date, observation_time) -- Prevents Duplicates!
)
```

## ⚙️ How to Run

### 1. Initial Setup
Install requirements and build the PostgreSQL database:
```bash
pip install -r requirements.txt
python setup_database.py
```

### 2. The Historical Load (Run Once)
To pull the massive initial 2-year dataset:
```bash
python weather_pipeline/run_historical_etl.py
```

### 3. The Incremental Load (Run Daily)
To pull just the latest day's data, modify the `START_DATE` and `END_DATE` in the file, then run:
```bash
python weather_pipeline/run_daily_update.py
```

---
<div align="center">
  <b>Built with ❤️ by an aspiring Data Professional</b><br>
  <a href="https://kirananalyst.com">Visit kirananalyst.com</a>
</div>
