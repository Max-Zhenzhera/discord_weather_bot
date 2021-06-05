"""
Contains weather api errors.

.. exception:: WeatherApiError(Exception)
    Implements base error that might be raised during the weather api usage
.. exception:: WeatherApiBadRequestError(WeatherApiError)
    400 API error
.. exception:: WeatherApiUnauthorizedError(WeatherApiError)
    401 API error
.. exception:: WeatherApiNotFoundError(WeatherApiError)
    404 API error
.. exception:: WeatherApiTooManyRequestsError(WeatherApiError)
    429 API error

.. const:: ERRORS_MAPPING
    Contains pairs of the response code and corresponding exception class (e.g. ` 400: WeatherApiBadRequestError `)
"""

from __future__ import annotations


class WeatherApiError(Exception):
    """ Implements base error that might be raised during the weather api usage """

    code = None


class WeatherApiBadRequestError(WeatherApiError):
    """
    Implements weather api error with `` 400 `` response status code.

    Link to the error doc - *

    Cause: Developer.

    Shortly:
        * sent request does not correspond weather APIs.
    """

    code = 400


class WeatherApiUnauthorizedError(WeatherApiError):
    """
    Implements weather api error with `` 401 `` response status code.

    Link to the error doc - https://openweathermap.org/faq#error401

    Cause: Developer.

    Shortly:
        * invalid/unactivated API key;
        * trying to get unpaid features.
    """

    code = 401


class WeatherApiNotFoundError(WeatherApiError):
    """
    Implements weather api error with `` 404 `` response status code.

    Link to the error doc - https://openweathermap.org/faq#error404

    Cause: User.

    Shortly:
        * wrong data [city name, country code] (user input mistake).
    """

    code = 404


class WeatherApiTooManyRequestsError(WeatherApiError):
    """
    Implements weather api error with `` 429 `` response status code.

    Link to the error doc - https://openweathermap.org/faq#error429

    Cause: User (but BECAUSE used weather API account is free and capabilities are restricted,
        so it is not really error, it more looks like usage limitation).

    Shortly:
        * permitted requests quantity exceeded for current account.
    """

    code = 429


class WeatherApiDeveloperError(WeatherApiBadRequestError, WeatherApiUnauthorizedError):
    """
    Implements weather api error that might be caused by Developer.
    Obviously, inherits all developer-cause errors.

    Cause: Developer.

    Shortly:
        * Shortcut exception for developer-cause errors catching.
    """


_narrowly_focused_errors = {
    WeatherApiBadRequestError,
    WeatherApiUnauthorizedError,
    WeatherApiNotFoundError,
    WeatherApiTooManyRequestsError
}

ERRORS_MAPPING = {exception.code: exception for exception in _narrowly_focused_errors}
