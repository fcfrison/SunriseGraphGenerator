import logging
import pandas as pd
import requests
import time
import threading

from threading import Thread
import concurrent.futures
from datetime import timedelta, datetime, date
import plotly.express as px
import matplotlib.pyplot as plt

from schemas.endpoints import *
from models.sunset_sunrise import SunsetSunriseModel
from errors import *

thread_local: threading.local = threading.local()

class App(Thread):
    def __init__(self, start_dt,end_dt,name_time_zone, lng, lat):
        super().__init__()
        self.start_dt = start_dt
        self.end_dt = end_dt
        self.name_time_zone = name_time_zone
        self.lng = lng
        self.lat = lat
    @property
    def start_dt(self):
        return self._start_dt
    @start_dt.setter
    def start_dt(self,start_dt:str):
        try:
            start_dt = start_dt.replace("/","-")
            start_dt = datetime.strptime(start_dt, '%m-%d-%Y')
            self._start_dt = start_dt.date()
        except Exception:
            raise StartDateFormatException()
    
    @property
    def end_dt(self):
        return self._end_dt
    @end_dt.setter
    def end_dt(self,end_dt:str):
        try:
            end_dt = end_dt.replace("/","-")
            end_dt = datetime.strptime(end_dt, '%m-%d-%Y')
            self._end_dt = end_dt.date()
        except Exception:
            raise EndDateFormatException()

    @property
    def name_time_zone(self):
        return self._name_time_zone
    @name_time_zone.setter
    def name_time_zone(self,name_time_zone:str):
        self._name_time_zone = name_time_zone
    
    @property
    def lng(self):
        return self._lng
    @lng.setter
    def lng(self,lng:float):
        self._lng = lng
    @property
    def lat(self):
        return self._lat
    @lat.setter
    def lat(self,lat:str):
        self._lat = lat

    def get_session(self):
        '''
        Returns a session managed by the variable 'thread_local'.
        '''
        if not hasattr(thread_local, "session"):
            thread_local.session = requests.Session()
        return thread_local.session

    def download_data(self,sunset_endpoint:SunsetSunriseEndpoint)->SunsetSunriseModel:
        '''
        Requests data from a specific endpoint and record it as an object of the class
        'SunsetSunriseModel'.
        '''
        params = sunset_endpoint.dict()
        params.pop('url')
        session = self.get_session()
        with session.get(sunset_endpoint.url, params=params) as sunset_resp:
            sunset_resp.raise_for_status()
            response = sunset_resp.json().get('results')
            logging.info(f'Downloaded data from endpoint: {sunset_endpoint.url}')
        sunset_model = SunsetSunriseModel(
                        lat=sunset_endpoint.lat,
                        lng=sunset_endpoint.lng,
                        utc_sunrise=response.get('sunrise'),
                        utc_sunset=response.get('sunset')
        )
        return sunset_model

    def daterange(self,date_init, date_final)->date:
        '''
        Function that creates a range of dates given an initial date and an final date.
        '''
        for n in range((date_final - date_init).days+1):
            yield date_init + timedelta(n)

    def generate_plotly_graph(self, df_time_and_date:pd.DataFrame)->None:
        '''
        Given a Pandas DataFrame, an line graph is generated using Plotly. 
        '''
        fig = px.line(df_time_and_date, x='day', y="seconds")
        fig.update_yaxes(tickformat="%H:%M:%S")
        fig.show()

    def generate_matplotlib_graph(self, df_time_and_date:pd.DataFrame):
        '''
        Given a Pandas DataFrame, an scatterplot graph is generated using Matplotlib. 
        '''
        plt.plot(df_time_and_date['date'], df_time_and_date['seconds'], 'o')
        plt.title('Date x Hour graph')
        plt.xlabel('Date')
        plt.ylabel('Hour')
        plt.gca().set_yticklabels([time.strftime("%H:%M:%S", time.gmtime(y)) 
                                    for y in plt.gca().get_yticks()])
        plt.show()   
    def run(self)->None:
        sunset_model_list = []
        sunset_sunrise_endpoint_list = []
        for dt in self.daterange(self.start_dt, self.end_dt):
            sunset_sunrise_endpoint_list.append(
                SunsetSunriseEndpoint(
                            lat=self.lat,
                            lng=self.lng,
                            date=dt.strftime("%Y-%m-%d"))
            )
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            sunset_model_list = executor.map(self.download_data, sunset_sunrise_endpoint_list)
        
        fn_convert_time_zone = (lambda my_city : my_city.convert_sunrise_time_zone(
                                                name_time_zone=self.name_time_zone))
        list_converted_time_zone = list(map(fn_convert_time_zone,sunset_model_list))
        
        df_time_and_date = pd.DataFrame(list_converted_time_zone, columns=['date'])
        df_time_and_date['date'] = pd.to_datetime(df_time_and_date['date'])    
        df_time_and_date['day'] = df_time_and_date['date'].dt.date
        df_time_and_date['seconds'] = ( df_time_and_date['date'].dt.hour * 3600 + 
                                        df_time_and_date['date'].dt.minute * 60 + 
                                        df_time_and_date['date'].dt.second)
        self.df_time_and_date = df_time_and_date
    



if __name__=='__main__':
    
    App(
        start_dt = "01-01-2020",
        end_dt = "12-31-2020",
        lng = -51.230000,
        lat = -30.033056,
        name_time_zone = 'America/Sao_Paulo'
    ).run()
    end_dt = date(2021, 12, 31)
    name_time_zone = 'America/Sao_Paulo'
    lng = -51.230000,
    lat = -30.033056
   



    