"""
=============================================================================
Author: Kiran
Website: kirananalyst.com
Bio: I have experience in turning raw data into actionable insights 
and building robust process automation pipelines.
=============================================================================
This module handles the extraction of data from the Open-Meteo API and dynamically
pulls a list of major global cities.
"""

import requests
import geonamescache
import time

def get_global_cities(limit=350):
    """
    Get a diverse list of major global cities using geonamescache.
    We pull the top cities by population to ensure we capture multiple states/regions
    for large countries like India and the USA, rather than just single capitals.
    """
    # Load the offline database of cities and countries
    gc = geonamescache.GeonamesCache()
    cities = gc.get_cities()
    
    # Sort cities by population from highest to lowest
    sorted_cities = sorted(cities.values(), key=lambda x: x['population'], reverse=True)
    
    target_cities = []
    countries = gc.get_countries()
    
    # Loop through the largest cities up to our limit
    for city in sorted_cities[:limit]:
        country_code = city['countrycode']
        # Map the country code to the full country name
        country_name = countries[country_code]['name'] if country_code in countries else country_code
        
        # Package the metadata into a dictionary
        target_cities.append({
            "country": country_name,
            "state": city.get('admin1code', 'N/A'),
            "city": city['name'],
            "lat": city['latitude'],
            "lon": city['longitude']
        })
        
    return target_cities

def extract_historical_weather_for_city(city_metadata, start_date_str, end_date_str):
    """
    Extracts historical hourly weather data for a single city between two dates.
    """
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={city_metadata['lat']}&longitude={city_metadata['lon']}&"
        f"start_date={start_date_str}&end_date={end_date_str}&"
        f"hourly=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,weather_code&"
        f"timezone=auto"
    )
    
    # Fetch the data from the API
    response = requests.get(url)
    
    # Sleep to respect Open-Meteo burst rate limits (preventing Status 429 errors)
    time.sleep(1.5) 
    
    if response.status_code == 200:
        data = response.json()
        return data.get("hourly", {})
    else:
        print(f"Failed to fetch data for {city_metadata['city']} - API Status {response.status_code}")
        return {}
