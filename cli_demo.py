import qweather
from rich.table import Table
from rich import print
from rich.text import Text
from rich.style import Style
from where_sunshine import sunshine_finder
from where_sunshine.utils import GeoMap as geo_map

import re

SUMMARY_TEMPLATE = """
🎉 {start_date} 至 {end_date} 期间，{location}共有 {num_cities} 个城市为 ☀️ 晴或 ⛅ 多云天气。
趁着好天气，来一场说走就走的 ✈️ 旅行吧！
"""

WEATHER_TEXT_TEMPLATE = """{weather_emoji} {weather_text} ({min_temp}~{max_temp} ℃ )"""


def display_help():
    print("你可以输入 📍 “位置” ☀️ “天气” 🔢 “日期” 的任意组合来查找晴天")
    print("同类型变量可以输入多个，用空格分割；不同类型变量依顺序输入用逗号分割")
    print(Text("注意：你的输入必须包含三个逗号来分割参数", style="red"))
    print("(👉 输入“help”显示此帮助消息或输入“exit”退出)")
    table = Table()
    table.add_column("变量", style="magenta")
    table.add_column("有效输入", style="bright_cyan")
    table.add_column("描述")

    table.add_row("位置", "中国(默认)", "中国所有晴天城市（不包括港澳台）")
    table.add_row("", "华北/东北/华东/华中/华南/西南/西北", "地理大区晴天城市")
    table.add_row("", "河北/山西/...", "省/直辖市/自治区晴天城市")
    table.add_row("", "石家庄/唐山/...", "地级市/地区/自治州/盟晴天城市")
    table.add_row("天气", "晴(默认)", "仅晴天天气")
    table.add_row("", "多云", "仅多云天气")
    table.add_row("日期", "`n`天 (默认 3天)", "最近 n (1<=n<=7) 天，例如 5天")
    table.add_row("", "20240626", "2024/06/26 这一天")
    table.add_row("", "20240626-20240630", "2024/06/26 至 2024/06/30 这五天")

    print(table)
    text = Text()
    text.append("例如：", style="dim")
    text.append("华东 北京，晴，5天", style="code")
    text.append("：输出华东地区和北京市中最近五天有晴天的城市\n      ")
    text.append("华北，，", style="code")
    text.append("：输出华北地区最近三天有晴天的城市\n      ")
    text.append("，晴 多云，20240626-20240702", style="code")
    text.append("：输出全国从 2024/06/26-2024/07/02 有晴天或多云的城市\n")
    print(text)


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


def restructure(cities_weather):
    """Restructure cities weather data based on cities mapping."""
    structured = {}

    for city, weather_data in cities_weather.items():
        region = geo_map.city_to_region(city)
        province = geo_map.city_to_province(city)

        if region not in structured:
            structured[region] = {}
        if province not in structured[region]:
            structured[region][province] = {}

        structured[region][province][city] = weather_data

    return structured


def summary(weather_data: dict, location: str) -> str:
    """Format weather summary."""
    num_cities = len(weather_data)
    location = "、".join(location.split(" "))
    if num_cities == 0:
        return f"😶‍🌫️ emo 了，{location}都没晴天！"
    for daily_weather in weather_data.values():
        start_date = daily_weather["daily"][0]["date"]
        end_date = daily_weather["daily"][-1]["date"]
        return SUMMARY_TEMPLATE.format(
            start_date=start_date, 
            end_date=end_date,
            location=location,
            num_cities=num_cities
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


def display_result(params):
    cities_weather = fetch_weather(params)
    print(summary(cities_weather, params[0]))
    
    cities_weather = restructure(cities_weather)
    for region, provinces in cities_weather.items():
        table = Table(title=region)
        table.add_column("省", style="cyan")
        table.add_column("市", style="magenta")
        table.add_column("日期", style="dim")
        table.add_column("天气", style="green")

        pre_province = ""
        for province, cities in provinces.items():
            pre_city = ""
            for city, daily_weather in cities.items():
                for day_weather in daily_weather["daily"]:
                    table.add_row(
                        "" if pre_province == province else province,
                        "" if pre_city == city else Text(city, style=Style(link=daily_weather["link"])),
                        day_weather["date"],
                        format_weather_text(day_weather),
                    )
                    pre_city = city
                    pre_province = province
        print(table)


def clear_cli():
    print("\033c", end="")


def parse_query(query: str):
    query = re.split(r",|，", query)
    if len(query) != 3:
        return None
    if query[2] == "":
        date = 3
    elif "天" in query[2]:
        date = int(query[2].replace("天", ""))
    else:
        date = query[2]
    return (
        "中国" if query[0] == "" else query[0],
        "晴" if query[1] == "" else query[1],
        date,
    )


def fetch_weather(query):
    location, weather, date = query
    locations = location.split(" ")
    weathers = weather.split(" ")
    result = {}

    for location in locations:
        for weather in weathers:
            if weather == "晴":
                result.update(sunshine_finder.sunny_cities(location, date))
            elif weather == "多云":
                result.update(sunshine_finder.cloudy_cities(location, date))
    return result


def main():
    if qweather.api_key is None:
        qweather.api_key = input("Please set your QWeather API key first: ")
        
    clear_cli()
    print("嗨 👋，在寻找晴天吗？\n")
    display_help()
    while True:
        query = input("WhereSunshine: ")
        if query == "exit":
            break
        elif query == "help":
            display_help()
        else:
            params = parse_query(query)
            if params is None:
                print(f"无效的输入: {query}")
                print(Text("注意：你的输入必须包含三个逗号来分割参数", style="red"))
            else:
                display_result(params)


if __name__ == "__main__":
    main()
