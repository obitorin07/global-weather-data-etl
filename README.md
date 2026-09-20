# Global Weather Data ETL & Analytics Pipeline

**Portfolio:** [kirananalyst.com](https://www.kirananalyst.com/)

## Overview

This project is an automated ETL pipeline that collects weather data from a public REST API, cleans and processes it using Python, stores it in PostgreSQL, and uses SQL to analyze the data.

The main goal is to build a practical end-to-end data pipeline and work with real data instead of manually downloaded files.

## What This Project Does

- Collects weather data from a public API
- Extracts and processes the API response using Python
- Cleans and validates the data using Pandas
- Stores the processed data in PostgreSQL
- Uses SQL to analyze weather trends and patterns
- Allows the pipeline to be run again as new data becomes available

## Project Flow

```text
Public Weather API
        ↓
     Python
        ↓
Extract & Process
        ↓
Clean & Validate
        ↓
    PostgreSQL
        ↓
   SQL Analysis
        ↓
     Insights
```

## Tech Stack

- Python
- Requests
- Pandas
- REST API
- PostgreSQL
- SQL
- Git & GitHub

## Data Source

Weather data is collected from the **Open-Meteo API**, which provides weather information for locations around the world without requiring an API key.

## Project Objective

The project focuses on practical data engineering and analytics skills, including:

- API data extraction
- Data cleaning and validation
- ETL workflow design
- PostgreSQL data storage
- SQL analysis
- Working with structured and time-based data
