"""
Contains settings for weather api package.

Cache settings
.. const:: DEFAULT_CACHE_EXPIRATION_TIME_IN_MINUTES
.. const:: DEFAULT_CACHE_EXPIRATION_TIME_IN_SECONDS

Weather API
.. const:: CURRENT_WEATHER_API_URL
.. const:: WEATHER_FORECAST_API_URL
.. const:: WEATHER_ICONS_URL
.. const:: WEATHER_ICONS_EXTENSION

Common params
.. const:: COMMON_PARAMS
"""

from ..settings import WEATHER_API_TOKEN


# -------------------- CACHE SETTINGS ----------------------

# cache expiration time in minutes for weather api results
DEFAULT_CACHE_EXPIRATION_TIME_IN_MINUTES = 10
# 10 minutes - recommended time for the same requests to weather API
DEFAULT_CACHE_EXPIRATION_TIME_IN_SECONDS = DEFAULT_CACHE_EXPIRATION_TIME_IN_MINUTES * 60
# see https://openweathermap.org/appid#apicare

# ----------------------------------------------------------


# -------------------- WEATHER API -------------------------

CURRENT_WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'
# api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}

WEATHER_FORECAST_API_URL = 'http://api.openweathermap.org/data/2.5/forecast'
# api.openweathermap.org/data/2.5/forecast?q={city name}&appid={API key}

WEATHER_ICONS_URL = 'https://openweathermap.org/themes/openweathermap/assets/vendor/owm/img/widgets/'
# https://openweathermap.org/themes/openweathermap/assets/vendor/owm/img/widgets/03d.png

WEATHER_ICONS_EXTENSION = '.png'

# ----------------------------------------------------------


# -------------------- COMMON PARAMS -----------------------

# additional GET params that used in each request
COMMON_PARAMS = {
    # api key - access to the weather api
    'appid': WEATHER_API_TOKEN,
    # units of the measure - set to the `metric` (Celsius)
    'units': 'metric'
}

# ----------------------------------------------------------
