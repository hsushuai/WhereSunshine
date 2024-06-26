from datetime import datetime, timedelta
from typing import Union, List

import json


def format_date(date: Union[int, str]) -> List[datetime.date]:
    """Format date to a list of datetime.date objects

    Args:
        date (Union[int, str]):
            Date to query weather:
                - Number of days from today (int).
                - Specific date in `YYYYMMDD` format (str).
                - Period in `YYYYMMDD-YYYYMMDD` format (str).

    Returns:
        List[datetime.date]: A list of datetime.date objects.
    """
    result = []

    if isinstance(date, int):
        # Case 1: Input is an integer representing the number of days from today
        start_date = datetime.today().date()
        for i in range(date):
            result.append(start_date + timedelta(days=i))

    elif isinstance(date, str):
        # Case 2: Input is a specific date in YYYYMMDD format or a range YYYYMMDD-YYYYMMDD
        if "-" in date:
            # Range of dates
            start_date_str, end_date_str = date.split("-")
            start_date = datetime.strptime(start_date_str, "%Y%m%d").date()
            end_date = datetime.strptime(end_date_str, "%Y%m%d").date()
            current_date = start_date
            while current_date <= end_date:
                result.append(current_date)
                current_date += timedelta(days=1)
        else:
            # Single date
            target_date = datetime.strptime(date, "%Y%m%d").date()
            result.append(target_date)

    return result


class GeoMap:
    data: dict = None
    region2provinces: dict = None
    province2cities: dict = None

    @classmethod
    def region_to_provinces(cls, region: str) -> list[str]:
        if cls.region2provinces is None:
            cls._load_region2province()
        for key, value in cls.region2provinces.items():
            if region in key:
                return value
        return None

    @classmethod
    def province_to_cities(cls, province: str) -> list[str]:
        if cls.province2cities is None:
            cls._load_province2cities()
        for key, value in cls.province2cities.items():
            if province in key:
                return value
        return None

    @classmethod
    def province_to_region(cls, province: str) -> str:
        query_province = province
        if cls.region2provinces is None:
            cls._load_region2province()
        for region, provinces in cls.region2provinces.items():
            for province in provinces:
                if query_province in province:
                    return region
        return None

    @classmethod
    def city_to_province(cls, city: str) -> str:
        query_city = city
        if cls.province2cities is None:
            cls._load_province2cities()
        for province, cities in cls.province2cities.items():
            for city in cities:
                if query_city in city:
                    return province
        return None

    @classmethod
    def city_to_region(cls, city: str) -> str:
        province = cls.city_to_province(city)
        return cls.province_to_region(province)

    @classmethod
    def region_to_cities(cls, region: str) -> list[str]:
        provinces = cls.region_to_provinces(region)
        cities = []
        for province in provinces:
            cities.extend(cls.province_to_cities(province))
        return cities

    @classmethod
    def all_cities(cls) -> list[str]:
        if cls.data is None:
            cls._load_data()
        cities_list = []
        for region, provinces in cls.data.items():
            for province, cities in provinces.items():
                cities_list.extend(cities)
        return cities_list

    @classmethod
    def all_provinces(cls) -> list[str]:
        if cls.data is None:
            cls._load_data()
        provinces_list = []
        for region, provinces in cls.data.items():
            provinces_list.extend(list(provinces.keys()))
        return provinces_list

    @classmethod
    def all_regions(cls) -> list[str]:
        if cls.data is None:
            cls._load_data()
        regions_list = list(cls.data.keys())
        return regions_list

    @classmethod
    def _load_region2province(cls):
        if cls.data is None:
            cls._load_data()
        cls.region2provinces = {}
        for region, provinces in cls.data.items():
            cls.region2provinces[region] = list(provinces.keys())

    @classmethod
    def _load_province2cities(cls):
        if cls.data is None:
            cls._load_data()
        cls.province2cities = {}
        for region, provinces in cls.data.items():
            for province, cities in provinces.items():
                cls.province2cities[province] = cities

    @classmethod
    def _load_data(cls):
        with open("data/cities_cn.json", "r", encoding="utf-8") as f:
            cls.data = json.load(f)
