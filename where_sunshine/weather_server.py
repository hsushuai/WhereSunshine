from typing import Optional, Dict, Union
from .utils import format_date
from datetime import datetime


class WeatherServer:
    r"""Weather forecast server powered by QWeather API.

    To use, you could provide your API key with
    `shell: export QWEATHER_API_KEY=xxx` or
    `code: zhipuai.api_key=xxx` or
    `code: WeatherServer(api_key=xxx)`

    Example: To fetch weather forecast:
        .. code-block:: python
            weather = WeatherServer(api_key=xxx)
            result = weather("北京")
            # result = weather("北京市", date=4)
            # result = weather("beijing", date="20240623")
            # result = weather("朝阳", adm="北京", date="20240623-20240627")
    """

    def __init__(
        self,
        lang: Optional[str] = None,
        unit: Optional[str] = None,
        scope: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        r"""
        Initialize the Weather object.

        Args:
            lang (Optional[str], optional):
                The language of the response content. If not specified, it 
                defaults to the official language of the country or region.
            unit (Optional[str], optional):
                Unit system for data ('m' for metric, 'i' for imperial).
            scope (Optional[str], optional):
                Scope for weather search, using ISO 3166 country codes.
                If this parameter is not set, the search scope will be global.
            api_key (Optional[str], optional):
                The Qweather API key.
        """
        self.daily_weather_client = None  #: QWeather daily weather API client
        self.city_lookup_client = None  #: QWeather city lookup API client

        self.lang = lang
        self.unit = unit
        self.scope = scope
        self.api_key = api_key
        
        try:
            import qweather

            if self.api_key is not None:
                qweather.api_key = self.api_key
            self.daily_weather_client = qweather.daily_weather_api
            self.city_lookup_client = qweather.city_lookup_api
        except ImportError as e:
            raise ImportError(
                "Failed to import qweather module. Make sure it is installed."
            ) from e

    def invoke(
        self,
        location: str,
        adm: Optional[str] = None,
        date: Union[int, str] = 3,
    ) -> Dict:
        r"""Get daily weather forecast.

        Args:
            location (str):
                The name of the region to be queried, which can be in Chinese or
                English. Examples: `location="beijing"`, `location="北京"`.
            adm (Optional[str], optional):
                The higher-level administrative division of a city. You can set
                the search to be limited to a certain administrative division to
                exclude cities with the same name or filter the results.
                Example: `adm="beijing"`.
            date (Union[int, str]):
                Date to query weather:
                - Number of days from today (1-7 for free subscription API, 
                  1-30 for standard and premium subscription API).
                - Specific date in `YYYYMMDD` format (e.g., "20240623").
                - Period in `YYYYMMDD-YYYYMMDD` format (e.g., "20240623-20240627").

        Returns:
            Dict: A dictionary containing weather information.
        """
        location_id, location_name = self._get_city_id_name(location, adm)
        result = self.daily_weather_client.invoke(
            location=location_id, days=f"{normalize_days(date)}d", lang=self.lang, unit=self.unit
        )
        response = {} 
        response["daily"] = [
            {
                "date": item["fxDate"],
                "tempMax": item["tempMax"],
                "tempMin": item["tempMin"],
                "weather": item["textDay"],
            }
            for item in result["daily"]
        ]
        response["link"] = result["fxLink"]
        response["daily"] = extract_days_response(response["daily"], date)
        response.update({"location": location_name})
        return response

    def _get_city_id_name(self, location, adm):
        resp = self.city_lookup_client.invoke(
            location=location, adm=adm, scope=self.scope, lang=self.lang
        )
        return resp["location"][0]["id"], resp["location"][0]["name"]

    def __call__(self, *args, **kwargs):
        return self.invoke(*args, **kwargs)


def normalize_days(date):
    current_date = datetime.now().date()
    date = format_date(date)
    delta_days = (date[-1] - current_date).days + 1

    closest_days = [3, 7, 10, 15, 30]
    for days in closest_days:
        if days >= delta_days:
            return days

    raise ValueError(f"Invalid date: {date}")


def extract_days_response(daily_weather, date):
    dates = format_date(date)
    result = []
    for day_weather in daily_weather:
        date_obj = datetime.strptime(day_weather["date"], "%Y-%m-%d").date()
        if date_obj in dates:
            result.append(day_weather)
    return result
