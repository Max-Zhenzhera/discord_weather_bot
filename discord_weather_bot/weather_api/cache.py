"""
Implements cache for weather API.

.. decorator:: cache_result(func: Callable = None, *, expiration_time_in_seconds: Optional[int] = None) -> Callable
"""

from typing import (
    Callable,
    Optional
)

import aiohttp
import expiringdict

from . import (
    settings,
    parsers
)


DEFAULT_CACHE_EXPIRATION_TIME_IN_SECONDS = settings.DEFAULT_CACHE_EXPIRATION_TIME_IN_MINUTES * 60


def cache_result(func: Callable = None, *, expiration_time_in_seconds: Optional[int] = None) -> Callable:
    """
    Cache weather API results.

    :param func: weather API coroutine
    :type func: Callable
    :keyword expiration_time_in_seconds: special expiration time (by default used one that indicated in settings)
    :type expiration_time_in_seconds: Optional[int]

    :return: inner function
    :rtype: Callable
    """

    if func is None:
        return lambda func: cache_result(func=func, expiration_time_in_seconds=expiration_time_in_seconds)

    cache = expiringdict.ExpiringDict(
        max_len=1000,
        max_age_seconds=expiration_time_in_seconds if expiration_time_in_seconds
        else DEFAULT_CACHE_EXPIRATION_TIME_IN_SECONDS
    )

    async def inner(session: aiohttp.ClientSession,
                    city_name: str, country_code: Optional[str] = None
                    ) -> parsers.WeatherApiResponseParser:
        """
        Return cached or compute, cache end return result.

        :param session: weather API coroutine argument
        :type session: aiohttp.ClientSession
        :param city_name: weather API coroutine argument
        :type city_name: str
        :param country_code: weather API coroutine argument
        :type country_code: Optional[str]

        :return: weather api response parser
        :rtype: parsers.WeatherApiResponseParser
        """

        cached_by = (city_name, country_code)

        if cached_by in cache:
            return cache[cached_by]

        result = await func(session, city_name, country_code)
        cache[cached_by] = result

        return result

    return inner
