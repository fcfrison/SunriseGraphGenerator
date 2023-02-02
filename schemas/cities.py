from geopy.geocoders import Nominatim
from pydantic import BaseModel, root_validator
from typing import Optional
from errors import *

class City(BaseModel):
    address : str
    latitude : Optional[float]
    longitude : Optional[float]
    
    @root_validator()
    def get_lat_lon(cls,values):
        geolocator = Nominatim(user_agent="city_addr_locator_app")
        location = geolocator.geocode(values['address'])
        if not location:
            raise LocationNotFoundException()
        values['latitude'] = location.latitude
        values['longitude']= location.longitude
        return values
