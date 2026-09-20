# Data Dictionary: Global Weather Database

This document explains exactly what each column in the `weather_data` PostgreSQL table means, written in simple, plain English.

| Column Name | Data Type | What it means |
| :--- | :--- | :--- |
| **id** | Integer | A unique, automatically generated number for every single row in the database. |
| **city** | Text | The name of the city where the weather was recorded (e.g., "Mumbai"). |
| **state** | Text | The state, province, or region the city is located in (e.g., "Maharashtra"). |
| **country** | Text | The country the city is located in (e.g., "India"). |
| **latitude** | Decimal | The exact GPS latitude coordinate of the city. |
| **longitude** | Decimal | The exact GPS longitude coordinate of the city. |
| **observation_date** | Date | The specific date the weather occurred (format: YYYY-MM-DD). |
| **observation_time** | Time | The specific hour of the day the weather was recorded (e.g., "14:00:00"). |
| **temperature** | Decimal | The temperature at that exact hour, measured in Celsius (°C). |
| **humidity** | Integer | The relative humidity percentage at that exact hour (0 to 100%). |
| **precipitation** | Decimal | The amount of rain or snow that fell during that hour, measured in millimeters (mm). |
| **wind_speed** | Decimal | How fast the wind was blowing, measured in kilometers per hour (km/h). |
| **weather_code** | Integer | A special number code from the API that tells you the general weather condition (e.g., 0 = Clear sky, 61 = Rain, 71 = Snow). |
| **loaded_at** | Timestamp | The exact date and time that our Python script inserted this row into the database. |
| **source** | Text | Where we got this data from (in our case, it will always say "Open-Meteo Archive API"). |
