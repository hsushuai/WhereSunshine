import qweather
from qweather.weather_api import CityLookupParams, DailyWeatherParams


# your api key
# qweather.api_key = ""


def daily_weather_api_invoke_example():
    params = DailyWeatherParams(location="101010100")
    response = qweather.daily_weather_api.invoke("3d", **params.asdict())
    print(response)


def city_lookup_api_invoke_example():
    params = CityLookupParams(location="New York", number=1)
    response = qweather.city_lookup_api.invoke(**params.asdict())
    print(response)


if __name__ == "__main__":
    daily_weather_api_invoke_example()
    city_lookup_api_invoke_example()
