import dataclasses

@dataclasses.dataclass
class BaseParams:
    def asdict(self):
        return dataclasses.asdict(self)


@dataclasses.dataclass
class CityLookupParams(BaseParams):
    location: str = None
    adm: str = None
    scope: str = None
    number: int = None
    lang: str = None


@dataclasses.dataclass
class DailyWeatherParams(BaseParams):
    location: str = None
    lang: str = None
    unit: str = None
