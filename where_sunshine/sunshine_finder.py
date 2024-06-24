import json
from typing import Optional, List, Union
from rich.progress import track
from .weather_service import WeatherService


class SunshineFinder:
    """Find all sunny cities in China.

    Args:
        filepath (str):
            Path to the cities directory.
        weather_service (WeatherService):
            Weather service.
        date (Union[int, str], optional):
            Date to query weather:
                - Number of days from today (1-7 for free subscription API,
                  1-30 for standard and premium subscription API).
                - Specific date in `YYYYMMDD` format (e.g., "20240623").
                - Period in `YYYYMMDD-YYYYMMDD` format (e.g., "20240623-20240627").

    Examples:
        .. code-block:: python

        sunny_cities = SunshineFinder.sunny_cities()
        cloudy_cities = SunshineFinder.cloudy_cities()
    """
    filepath: str = "data/cities_cn.json"
    weather_service: WeatherService = WeatherService()
    result: Optional[dict] = None
    date: Union[int, str] = 7

    def __init__(
        self, 
        filepath: Optional[str]=None, 
        weather_service: Optional[WeatherService]=None,
        date: Optional[Union[int, str]]=None,
    ):
        self.filepath = filepath if filepath is not None else self.filepath
        self.weather_service = weather_service if weather_service is not None else self.weather_service
        self.date = date if date is not None else self.date
    
    @classmethod
    def fetch_weather(
        cls, date: Optional[Union[int, str]] = None, cities: Optional[List[str]] = None
    ):
        date = cls.date if date is None else date
        cities = cls.all_cities() if cities is None else cities
        result = dict()
        for city in track(cities, description="Fetching"):
            result[city] = cls.weather_service(city, date=date)["daily"]
        return result
    
    @classmethod
    def sunny_cities(cls):
        cls.result = cls.fetch_weather() if cls.result is None else cls.result
        result = dict()
        for city, daily_weather in cls.result.items():
            for day_weather in daily_weather:
                if day_weather["weather"] == "晴":
                    result[city] = daily_weather
                    continue
        return result
    
    @classmethod
    def cloudy_cities(cls):
        cls.result = cls.fetch_weather() if cls.result is None else cls.result
        result = dict()
        for city, daily_weather in cls.result.items():
            for day_weather in daily_weather:
                if "云" in day_weather["weather"]:
                    result[city] = daily_weather
                    continue
        return result
    
    def __call__(self, *args, **kwargs):
        self.result = self.fetch_weather(*args, **kwargs)
        return self.result

    @classmethod
    def all_cities(cls):
        with open(cls.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        all_cities = [
            city
            for regions in data.values()
            for cities in regions.values()
            for city in cities
        ]
        return all_cities
