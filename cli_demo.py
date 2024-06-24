from rich.table import Table
import json
from rich import print
from where_sunshine import SunshineFinder as sunshine_finder

SUMMARY_TEMPLATE = """
🎉 {start_date} 至 {end_date} 期间，全国（不包括港澳台）共有 {num_cities} 个城市为 ☀️ 晴或 ⛅ 多云天气。
趁着好天气，来一场说走就走的 ✈️ 旅行吧！
"""

WEATHER_TEXT_TEMPLATE = """{weather_emoji} {weather_text} ({min_temp}~{max_temp} ℃ )"""


def weather_to_emoji(weather):
    emojis = {
        "晴": "☀️",
        "云": "⛅",
        "阴": "☁️",
        "雷": "⛈️",
        "雪": "❄️",
        "雾": "🌫️",
        "霾": "🌫️",
        "雨夹雪": "🌨️",
        "雨": "🌧️",
        "沙": "🌪️",
    }

    for key in emojis:
        if key in weather:
            return emojis[key]
    return ""


def restructure(cities_weather, filepath="data/cities_cn.json"):
    """Restructure cities weather data based on cities mapping."""
    with open(filepath, "r", encoding="utf-8") as f:
        cities_cn = json.load(f)
    structured = {}

    for city, weather_data in cities_weather.items():
        found = False

        for region, provinces in cities_cn.items():
            for province, cities in provinces.items():
                if city in cities:
                    if region not in structured:
                        structured[region] = {}
                    if province not in structured[region]:
                        structured[region][province] = {}
                    structured[region][province][city] = weather_data
                    found = True
                    break
            if found:
                break

    return structured


def format_summary(weather_data: dict) -> str:
    """Format weather summary."""
    num_cities = len(weather_data)
    if num_cities == 0:
        return "😶‍🌫️ emo 了，全国都没晴天！"
    for daily_weather in weather_data.values():
        start_date = daily_weather[0]["date"]
        end_date = daily_weather[-1]["date"]
        return SUMMARY_TEMPLATE.format(
            start_date=start_date, end_date=end_date, num_cities=num_cities
        )


def format_weather_text(day_weather):
    """Format weather text."""
    weather_emoji = weather_to_emoji(day_weather["weather"])
    weather_text = day_weather["weather"]
    min_temp = day_weather["tempMin"]
    max_temp = day_weather["tempMax"]
    return WEATHER_TEXT_TEMPLATE.format(
        weather_emoji=weather_emoji,
        weather_text=weather_text,
        min_temp=min_temp,
        max_temp=max_temp,
    )


def main():
    sunny_cities = sunshine_finder.sunny_cities()
    cloudy_cities = sunshine_finder.cloudy_cities()
    sunny_cities.update(cloudy_cities)
    print(format_summary(sunny_cities))
    
    sunny_cities = restructure(sunny_cities)
    for region, provinces in sunny_cities.items():
        table = Table(title=region)
        table.add_column("省", style="cyan")
        table.add_column("市", style="magenta")
        table.add_column("日期", style="dim")
        table.add_column("天气", style="green")

        pre_province = ""
        for province, cities in provinces.items():
            pre_city = ""
            for city, daily_weather in cities.items():
                for day_weather in daily_weather:
                    table.add_row(
                        "" if pre_province == province else province,
                        "" if pre_city == city else city,
                        day_weather["date"],
                        format_weather_text(day_weather),
                    )
                    pre_city = city
                    pre_province = province
        print(table)

    

if __name__ == "__main__":
    main()