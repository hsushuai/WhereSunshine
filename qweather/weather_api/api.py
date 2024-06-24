# -*- coding:utf-8 -*-
from abc import ABC, abstractmethod
from typing import Any

import posixpath

import qweather
from qweather.utils.http_client import get

class BaseAPI(ABC):
    @abstractmethod
    def invoke(self, **kwargs: Any):
        ...

    @staticmethod
    def _build_api_url(base_url, *path):
        return posixpath.join(base_url, *path)


class CityLookupAPI(BaseAPI):
    @classmethod
    def invoke(cls, **kwargs):
        kwargs.update(_api_key())
        kwargs = {("range" if k == "scope" else k): v for k, v in kwargs.items()}
        return get(cls._build_api_url(qweather.geo_api_url, "city", "lookup"), **kwargs)


class TopCityAPI(BaseAPI):
    @classmethod
    def invoke(cls, **kwargs):
        kwargs.update(_api_key())
        kwargs = {("range" if k == "scope" else k): v for k, v in kwargs.items()}
        return get(cls._build_api_url(qweather.geo_api_url, "city", "top"), **kwargs)


class POILookupAPI(BaseAPI):
    @classmethod
    def invoke(cls, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.geo_api_url, "poi", "lookup"), **kwargs)


class POIRangeAPI(BaseAPI):
    @classmethod
    def invoke(cls, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.geo_api_url, "poi", "range"), **kwargs)


class NowWeatherAPI(BaseAPI):
    @classmethod
    def invoke(cls, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "weather", "now"), **kwargs)


class DailyWeatherAPI(BaseAPI):
    @classmethod
    def invoke(cls, days, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "weather", days), **kwargs)


class HourWeatherAPI(BaseAPI):
    @classmethod
    def invoke(cls, hours, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "weather", hours), **kwargs)


class MinutelyPrecipitationAPI(BaseAPI):
    @classmethod
    def invoke(cls, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "minutely", "5m"), **kwargs)


class GridNowWeatherAPI(BaseAPI):
    @classmethod
    def invoke(cls, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "grid-weather", "now"), **kwargs)


class GridDailyWeatherAPI(BaseAPI):
    @classmethod
    def invoke(cls, days, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "grid-weather", days), **kwargs)


class GridHourWeatherAPI(BaseAPI):
    @classmethod
    def invoke(cls, hours, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "grid-weather", hours), **kwargs)


class WarningWeatherAPI(BaseAPI):
    @classmethod
    def invoke(cls, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "warning", "now"), **kwargs)


class WarningCityListAPI(BaseAPI):
    @classmethod
    def invoke(cls, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "warning", "list"), **kwargs)


class WeatherIndicesAPI(BaseAPI):
    @classmethod
    def invoke(cls, days, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "indices", days), **kwargs)


class AQINowAPI(BaseAPI):
    @classmethod
    def invoke(cls, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "air", "now"), **kwargs)


class AQIDailyAPI(BaseAPI):
    @classmethod
    def invoke(cls, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "air", "5d"), **kwargs)


class HistoricalWeatherAPI(BaseAPI):
    @classmethod
    def invoke(cls, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "historical", "weather"), **kwargs)


class HistoricalAQIAPI(BaseAPI):
    @classmethod
    def invoke(cls, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "historical", "air"), **kwargs)


class TyphoonForecastAPI(BaseAPI):
    @classmethod
    def invoke(cls, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "tropical", "storm-forecast"), **kwargs)


class TyphoonTrackAPI(BaseAPI):
    @classmethod
    def invoke(cls, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "tropical", "storm-track"), **kwargs)


class TyphoonListAPI(BaseAPI):
    @classmethod
    def invoke(cls, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "tropical", "storm-list"), **kwargs)


class OceanTideAPI(BaseAPI):
    @classmethod
    def invoke(cls, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "ocean", "tide"), **kwargs)


class OceanCurrentsAPI(BaseAPI):
    @classmethod
    def invoke(cls, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "ocean", "currents"), **kwargs)


class SolarRadiationHourAPI(BaseAPI):
    @classmethod
    def invoke(cls, hours, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "solar-radiation", hours), **kwargs)


class AstronomySunAPI(BaseAPI):
    @classmethod
    def invoke(cls, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "astronomy", "sun"), **kwargs)


class AstronomyMoonAPI(BaseAPI):
    @classmethod
    def invoke(cls, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "astronomy", "moon"), **kwargs)


class AstronomySolarElevationAngleAPI(BaseAPI):
    @classmethod
    def invoke(cls, **kwargs):
        kwargs.update(_api_key())
        return get(cls._build_api_url(qweather.weather_api_url, "astronomy", "solar-elevation-angle"), **kwargs)


def _api_key():
        if not qweather.api_key:
            raise Exception("api_key not provided, you could provide it with `shell: export QWEATHER_API_KEY=xxx` or `code: qweather.api_key=xxx`")
        
        return {"key": qweather.api_key}