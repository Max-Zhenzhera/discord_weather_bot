"""
Contains parsers for weather API.

.. class:: WeatherApiResponsePar
    Implements weatherAPI response (handle response code)
.. class:: WeatherParser
    Implements parser that parse base weather data
.. class:: PeriodWeatherForecastParser(WeatherParser
    Implements parser that parse period weather forecast
.. class:: CurrentWeatherParser(WeatherApiResponseParser
    Implements parser that parse current weather
.. class:: DayWeatherForecastPar
    Implements parser that parse weather forecast by days
.. class:: WeatherForecastParser(WeatherApiResponseParse
    Implements parser that parse weather forecast
"""

import datetime
import itertools
import operator
from urllib.parse import urljoin as urllib_parse_urljoin

from . import (
    errors,
    settings
)


class WeatherApiResponseParser:
    """
    Implements weather API response parser.

    Handles the response code.
    """

    def __init__(self, api_response: dict) -> None:
        """
        Init weather data instance and handle response code of the weather data.

        :param api_response: data that fetched from the weather API
        :type api_response: dict

        Check: `` errors.ERRORS_MAPPING ``
        :raises errors.WeatherApiBadRequestError: raised if response code is 400
        :raises errors.WeatherApiUnauthorizedError: raised if response code is 401
        :raises errors.WeatherApiNotFoundError: raised if response code is 404
        :raises errors.WeatherApiTooManyRequestsError: raised if response code is 420

        :raises errors.WeatherApiError: raised if response code is unhandled concretely

        For more error handling understanding - look at ``errors`` doc.
        """

        self.response_code = int(api_response['cod'])

        if self.response_code != 200:
            message = api_response['message']

            exception = errors.ERRORS_MAPPING.get(self.response_code, errors.WeatherApiError)
            raise exception(f'{self.response_code}: {message}')

        self._data = api_response


class WeatherParser:
    """
    Implements weather data parser.

    Make available and convenient to get weather data by properties that parse the data.
    Used in the other weather-parsers classes in composition way.
    """

    def __init__(self, weather_data: dict) -> None:
        self._data = weather_data

    @property
    def main(self) -> str:
        return self._data['weather'][0]['main']

    @property
    def description(self) -> str:
        return self._data['weather'][0]['description'].capitalize()

    @property
    def _icon_tag(self) -> str:
        return self._data['weather'][0]['icon']

    @property
    def _icon_filename(self) -> str:
        return self._icon_tag + settings.WEATHER_ICONS_EXTENSION

    @property
    def icon_url(self) -> str:
        return urllib_parse_urljoin(settings.WEATHER_ICONS_URL, self._icon_filename)

    @property
    def temperature(self) -> float:
        return self._data['main']['temp']

    @property
    def temperature_feels_like(self) -> float:
        return self._data['main']['feels_like']

    @property
    def temperature_min(self) -> float:
        return self._data['main']['temp_min']

    @property
    def temperature_max(self) -> float:
        return self._data['main']['temp_max']

    @property
    def pressure(self) -> float:
        return self._data['main']['pressure']

    @property
    def humidity(self) -> float:
        return self._data['main']['humidity']

    @property
    def wind_speed(self) -> float:
        return self._data['wind']['speed']

    @property
    def clouds(self) -> float:
        return self._data['clouds']['all']


class PeriodWeatherForecastParser(WeatherParser):
    """
    Implements period weather forecast parser.

    Complements base `WeatherParser` by adding new peculiar properties
    and setting more understandable (narrow) name for further using.
    """

    def __init__(self, period_weather_data: dict) -> None:
        super().__init__(period_weather_data)

    @property
    def data_forecasting_datetime(self) -> datetime.datetime:
        return datetime.datetime.utcfromtimestamp(self._data['dt'])

    @property
    def data_forecasting_date(self) -> datetime.date:
        return self.data_forecasting_datetime.date()


class CurrentWeatherParser(WeatherApiResponseParser):
    """ Implements current weather parser """

    def __init__(self, current_weather_data: dict) -> None:
        super().__init__(current_weather_data)

        self._weather_data = WeatherParser(current_weather_data)

    @property
    def weather(self) -> WeatherParser:
        return self._weather_data

    @property
    def data_calculation_datetime(self) -> datetime.datetime:
        return datetime.datetime.utcfromtimestamp(self._data['dt'])

    @property
    def data_calculation_date(self) -> datetime.date:
        return self.data_calculation_datetime.date()

    @property
    def city_name(self) -> str:
        return self._data['name']

    @property
    def country_code(self) -> str:
        return self._data['sys']['country']

    @property
    def sunrise_datetime(self) -> datetime.datetime:
        return datetime.datetime.utcfromtimestamp(self._data['sys']['sunrise'])

    @property
    def sunset_datetime(self) -> datetime.datetime:
        return datetime.datetime.utcfromtimestamp(self._data['sys']['sunset'])

    @property
    def timezone_in_hours_shift(self) -> int:
        return self._data['timezone'] / 3600


class DayWeatherForecastParser:
    """
    Implements daily weather forecast parser.

    Gather all `PeriodWeatherForecastParser` instances that contain the same day information
    (but different time-periods).
    Used in the other weather-parsers classes in composition way.
    """

    def __init__(self, period_weather_forecast_parsers: list[PeriodWeatherForecastParser]) -> None:
        self._period_parsers = period_weather_forecast_parsers

    @property
    def period_parsers(self) -> list[PeriodWeatherForecastParser]:
        return self._period_parsers

    @property
    def temperature_min_of_the_day(self) -> float:
        """ Return the min value of the temperature for the day """
        temperature_min_of_the_day = min(
            self._period_parsers,
            key=operator.attrgetter('temperature_min')
        ).temperature_min

        return temperature_min_of_the_day

    @property
    def temperature_max_of_the_day(self) -> float:
        """ Return the max value of the temperature for the day """
        temperature_max_of_the_day = max(
            self._period_parsers,
            key=operator.attrgetter('temperature_max')
        ).temperature_max

        return temperature_max_of_the_day


class WeatherForecastParser(WeatherApiResponseParser):
    """
    Implements weather forecast parser.

    Contains convenient properties to get weather forecast info (for: today, tomorrow, all 5-day forecast).
    """

    def __init__(self, weather_forecast_data: dict) -> None:
        super().__init__(weather_forecast_data)

        self._forecast_periods_parsers = [
            PeriodWeatherForecastParser(period_weather_data) for period_weather_data in weather_forecast_data['list']
        ]
        self._daily_forecast_parsers: list[DayWeatherForecastParser] = self._produce_daily_forecast()

    @property
    def city_name(self) -> str:
        return self._data['city']['name']

    @property
    def country_code(self) -> str:
        return self._data['city']['country']

    @property
    def sunrise_datetime(self) -> datetime.datetime:
        return datetime.datetime.utcfromtimestamp(self._data['city']['sunrise'])

    @property
    def sunset_datetime(self) -> datetime.datetime:
        return datetime.datetime.utcfromtimestamp(self._data['city']['sunset'])

    @property
    def timezone_in_hours_shift(self) -> float:
        return self._data['city']['timezone'] / 3600

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # weather forecast properties

    @property
    def today_forecast(self) -> DayWeatherForecastParser:
        return self._get_one_day_forecast(0)

    @property
    def tomorrow_forecast(self) -> DayWeatherForecastParser:
        return self._get_one_day_forecast(1)

    @property
    def all_5_day_forecast(self) -> list[DayWeatherForecastParser]:
        return self._daily_forecast_parsers

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def _produce_daily_forecast(self) -> list[DayWeatherForecastParser]:
        """
        Return the daily forecast.

        :return: daily forecast
        :rtype: list[DayWeatherForecastParser]
        """

        daily_forecast_parsers = [
            DayWeatherForecastParser(list(day)) for _, day in itertools.groupby(
                self._forecast_periods_parsers,
                key=operator.attrgetter('data_forecasting_date')
            )
        ]

        return daily_forecast_parsers

    def _get_one_day_forecast(self, day_shift: int) -> DayWeatherForecastParser:
        """
        Return one day forecast.

        Note:
            * it is 5-day weather forecast
            * so, daily weather forecast list has length 5
            * consider that start index in list is [0]
            * range of `day_shift` argument is [0,...,4]

        :param day_shift: index of the 5-length daily weather forecast list
        :type day_shift: int

        :return: weather forecast for concrete day
        :rtype: DayWeatherForecastParser
        """

        if day_shift not in range(0, 5):
            message = 'unexpected `day_shift` value - it must be in the range between 0 and 4 - [0,...,4]! '
            message += 'Since weather forecast has data only for 5 days - there is cause of this limitation'
            raise ValueError(message)

        return self._daily_forecast_parsers[day_shift]
