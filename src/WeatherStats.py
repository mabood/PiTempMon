import requests
from utils import *
from IntervalTimer import IntervalTimer

class WeatherStats():
    def __init__(self):
        self.http_request = self.build_request()
        self.city = None
        self.elevation = None
        self.latitude = None
        self.longitude = None
        self.zip = None
        self.local_epoch = None
        self.local_time = None
        self.local_timezone = None
        self.obs_location = None
        self.precip_1hr_in = None
        self.precip_1hr_metric = None
        self.precip_today_in = None
        self.precip_today_metric = None
        self.pressure_in = None
        self.pressure_mb = None
        self.humidity = None
        self.weather = None
        self.wind_degrees = None
        self.wind_dir = None
        self.wind_gust_mph = None
        self.station_id = None
        self.temp_c = None
        self.temp_f = None

        self.interval = float(get_property('REQUEST_INTERVAL', 'WEATHER'))
        self.update_weather_stats()
        self.call_timer = IntervalTimer(self.interval, self.update_weather_stats)

    def build_request(self):
        http_request = get_property('WU_URL', 'WEATHER')
        http_request += get_property('WU_API_KEY', 'WEATHER')
        http_request += get_property('WU_QUERY', 'WEATHER')
        http_request += get_property('US_CITY', 'WEATHER')
        http_request += '.json'
        return http_request

    def update_weather_stats(self):
        req = requests.get(self.http_request)
        try:
            stats = req.json()['current_observation']

            self.city = stats['display_location']['full']
            self.elevation = float(stats['display_location']['elevation'])
            self.latitude = float(stats['display_location']['latitude'])
            self.longitude = float(stats['display_location']['longitude'])
            self.zip = stats['display_location']['zip']

            self.temp_c = float(stats['temp_c'])
            self.temp_f = float(stats['temp_f'])

            self.local_epoch = stats['local_epoch']
            self.local_time = stats['local_time_rfc822']
            self.local_timezone = stats['local_tz_short']

            self.obs_location = stats['observation_location']['city']

            self.precip_1hr_in = float(stats['precip_1hr_in'])
            self.precip_1hr_metric = float(stats['precip_1hr_metric'])
            self.precip_today_in = float(stats['precip_today_in'])
            self.precip_today_metric = float(stats['precip_today_metric'])

            self.pressure_in = float(stats['pressure_in'])
            self.pressure_mb = float(stats['pressure_mb'])

            self.humidity = stats['relative_humidity']
            self.weather = stats['weather']
            self.wind_degrees = float(stats['wind_degrees'])
            self.wind_dir = stats['wind_dir']
            self.wind_gust_mph = float(stats['wind_gust_mph'])
            self.station_id = stats['station_id']

        except Exception as e:
            logging.error('Error updating weather stats: %s' % e.message)