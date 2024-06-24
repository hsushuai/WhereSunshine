import os

__all__ = [
    "city_lookup_api",
    "top_city_api",
    "poi_lookup_api",
    "poi_range_api",
    "now_weather_api",
    "daily_weather_api",
    "hour_weather_api",
    "minutely_precipitation_api",
    "grid_now_weather_api",
    "grid_daily_weather_api",
    "grid_hour_weather_api",
    "warning_weather_api",
    "warning_city_list_api",
    "weather_indices_api",
    "aqi_now_api",
    "aqi_daily_api",
    "historical_aqi_api",
    "historical_weather_api",
    "typhoon_forecast_api",
    "typhoon_track_api",
    "typhoon_list_api",
    "ocean_tide_api",
    "ocean_currents_api",
    "solar_radiation_hour_api",
    "astronomy_sun_api",
    "astronomy_moon_api",
    "astronomy_solar_elevation_angle_api"
]

from .weather_api import (
    city_lookup_api,
    top_city_api,
    poi_lookup_api,
    poi_range_api,
    now_weather_api,
    daily_weather_api,
    hour_weather_api,
    minutely_precipitation_api,
    grid_now_weather_api,
    grid_daily_weather_api,
    grid_hour_weather_api,
    warning_weather_api,
    warning_city_list_api,
    weather_indices_api,
    aqi_now_api,
    aqi_daily_api,
    historical_aqi_api,
    historical_weather_api,
    typhoon_forecast_api,
    typhoon_track_api,
    typhoon_list_api,
    ocean_tide_api,
    ocean_currents_api,
    solar_radiation_hour_api,
    astronomy_sun_api,
    astronomy_moon_api,
    astronomy_solar_elevation_angle_api,
)


api_key = os.environ.get("QWEATHER_API_KEY")


weather_api_url = os.environ.get("WEATHER_API_URL", "https://devapi.qweather.com/v7")
geo_api_url = os.environ.get("GEO_API_URL", "https://geoapi.qweather.com/v2")
