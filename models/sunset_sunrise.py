import pytz
from pydantic import BaseModel
from datetime import datetime

class SunsetSunriseModel(BaseModel):
    lat : float
    lng : float
    utc_sunrise : datetime
    utc_sunset : datetime

    def convert_sunrise_time_zone(self,name_time_zone:str):
        timezone = pytz.timezone(name_time_zone)
        return self.utc_sunrise.astimezone(timezone)
    def convert_sunset_time_zone(self,name_time_zone:str):
        timezone = pytz.timezone(name_time_zone)
        return self.utc_sunset.astimezone(timezone)
    def __repr__(self) -> str:
        return f'lat = {self.lat}, lng = {self.lng}\n'
    def __str__(self) -> str:
        return f'lat = {self.lat}, lng = {self.lng}\n'