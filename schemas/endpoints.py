from pydantic import BaseModel
from typing import Optional

class SunsetSunriseEndpoint(BaseModel):
    '''
    This class is intended to represent an API endpoint.
    '''
    url : str = "https://api.sunrise-sunset.org/json"
    lat : float
    lng : float
    date : Optional[str]
    callback : Optional[str]
    formatted : int = 0
