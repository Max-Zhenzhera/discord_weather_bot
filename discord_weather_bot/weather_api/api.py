"""
Contains functions that work with weather api.

____________________________________________________________________________________________________________
Important notation: API functions might propagate errors raised on parser instance creation.
____________________________________________________________________________________________________________

.. function:: get_current_weather_by_city_name(session: aiohttp.ClientSession,
        city_name: str, country_code: Optional[str] = None) -> parsers.CurrentWeatherParser:
    Return current weather data by cite name
.. function:: get_weather_forecast_by_city_name(session: aiohttp.ClientSession,
        city_name: str, country_code: Optional[str] = None) -> parsers.WeatherForecastParser:
    Return weather forecast data by cite name
"""

from __future__ import annotations

from typing import (
    Optional
)

import aiocache
import aiohttp

from . import (
    parsers,
    settings,
    utils
)
from .cache import cache_key_builder


@aiocache.cached(ttl=settings.DEFAULT_CACHE_EXPIRATION_TIME_IN_SECONDS, key_builder=cache_key_builder)
async def get_current_weather_by_city_name(session: aiohttp.ClientSession,
                                           city_name: str, country_code: Optional[str] = None
                                           ) -> parsers.CurrentWeatherParser:
    """
    Return current weather data by city name.

    :param session: session (to send http requests)
    :type session: aiohttp.ClientSession
    :param city_name: city name (to get the weather data)
    :type city_name: str
    :param country_code: non-required country code for more accurate searching
    :type country_code: Optional[str]

    :return: current weather data
    :rtype: parsers.CurrentWeatherParser
    """

    location = f'{city_name},{country_code}' if country_code else city_name
    params = dict(q=location, **settings.COMMON_PARAMS)

    current_weather_data = await utils.fetch_json_response(session, settings.CURRENT_WEATHER_API_URL, params)
    current_weather_parser = parsers.CurrentWeatherParser(current_weather_data)

    return current_weather_parser


@aiocache.cached(ttl=settings.DEFAULT_CACHE_EXPIRATION_TIME_IN_SECONDS, key_builder=cache_key_builder)
async def get_weather_forecast_by_city_name(session: aiohttp.ClientSession,
                                            city_name: str, country_code: Optional[str] = None
                                            ) -> parsers.WeatherForecastParser:
    """
    Return weather forecast data by city name.

    :param session: session (to send http requests)
    :type session: aiohttp.ClientSession
    :param city_name: city name (to get the weather data by)
    :type city_name: str
    :param country_code: non-required country code for more accurate searching
    :type country_code: Optional[str]

    :return: weather forecast data
    :rtype: dict
    """

    location = f'{city_name},{country_code}' if country_code else city_name
    params = dict(q=location, **settings.COMMON_PARAMS)

    weather_forecast_data = await utils.fetch_json_response(session, settings.WEATHER_FORECAST_API_URL, params)
    weather_forecast_parser = parsers.WeatherForecastParser(weather_forecast_data)

    return weather_forecast_parser
