from datetime import datetime
from typing import Optional, Union
from rich.progress import track
from .weather_server import WeatherServer
from .utils import GeoMap as geo_map
from .utils import format_date


class SunshineFinder:
    """Find all sunny cities in China.

    Args:
        date (Union[int, str], optional):
            Date to query weather:
                - Number of days from today (1-7 for free subscription API,
                  1-30 for standard and premium subscription API).
                - Specific date in `YYYYMMDD` format (e.g., "20240623").
                - Period in `YYYYMMDD-YYYYMMDD` format (e.g., "20240623-20240627").

    Examples:
        .. code-block:: python

        from where_sunshine import sunshine_finder

        sunny_cities = sunshine_finder.sunny_cities("华东")
    """
    weather_server = WeatherServer()
    date: Union[int, str] = 7
    result: dict = dict()

    def fetch_weather(
        self,
        location: str,
        date: Optional[Union[int, str]] = None,
    ):
        query_dates = format_date(self.date if date is None else date)
        cities = location_to_cities(location)
        for city in track(cities, description="Fetching"):
            if city not in self.result:
                self.result[city] = {}
                response = self.weather_server(city, date=date)
                self.result[city]["daily"] = response["daily"]
                self.result[city]["link"] = response["link"] 
            else:
                dates = [
                    datetime.strptime(day_weather["date"], "%Y-%m-%d").date()
                    for day_weather in self.result[city]["daily"]
                ]
                if query_dates[-1] > dates[-1]:
                    response = self.weather_server(city, date=date)
                    self.result[city]["daily"] = response["daily"]
                    self.result[city]["link"] = response["link"]
        return {city: self.result[city] for city in cities}
    
    @classmethod
    def sunny_cities(cls, location="中国", date: Union[int, str] = None) -> dict:
        """Return a list of sunny cities and their weather base on the location.

        Args:
            location (str, optional):
                The cities location. It can be a region, a province, or a city.
                Defaults to "中国".
            date (Union[int, str], optional):
                Date to query weather:
                    - Number of days from today (1-7 for free subscription API,
                    1-30 for standard and premium subscription API).
                    - Specific date in `YYYYMMDD` format (e.g., "20240623").
                    - Period in `YYYYMMDD-YYYYMMDD` format (e.g., "20240623-20240627").
        """
        fetch_result = cls.fetch_weather(cls, location, date)
        result = dict()
        for city, daily_weather in fetch_result.items():
            for day_weather in daily_weather["daily"]:
                if day_weather["weather"] == "晴":
                    result[city] = daily_weather
                    continue
        return result
    
    @classmethod
    def cloudy_cities(cls, location="中国", date: Union[int, str] = None) -> dict:
        """Return a list of cloudy cities and their weather base on the location.

        Args:
            location (str, optional):
                The cities location. It can be a region, a province, or a city.
                Defaults to "中国".
            date (Union[int, str], optional):
                Date to query weather:
                    - Number of days from today (1-7 for free subscription API,
                    1-30 for standard and premium subscription API).
                    - Specific date in `YYYYMMDD` format (e.g., "20240623").
                    - Period in `YYYYMMDD-YYYYMMDD` format (e.g., "20240623-20240627").
        """
        fetch_result = cls.fetch_weather(cls, location, date)
        result = dict()
        for city, daily_weather in fetch_result.items():
            for day_weather in daily_weather["daily"]:
                if "云" in day_weather["weather"]:
                    result[city] = daily_weather
                    continue
        return result


def location_to_cities(location) -> list[str]:
    """Return a list of cities base on the location."""
    if location == "中国":
        return geo_map.all_cities()
    for province in geo_map.all_provinces():
        if location in province:
            return geo_map.province_to_cities(province)
    for region in geo_map.all_regions():
        if location in region:
            return geo_map.region_to_cities(region)
    for city in geo_map.all_cities():
        if location in city:
            return [city]
    raise ValueError("Can't find the location.")
