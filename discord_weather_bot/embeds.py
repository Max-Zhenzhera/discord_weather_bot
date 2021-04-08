"""
Implements embeds (organized messages) for bot.

.. class:: WeatherEmbed(discord.Embed)
    Implements base embed for weather
.. class:: CurrentWeatherEmbed(WeatherEmbed)
    Implements embed for current weather
.. class:: DayWeatherForecastEmbed(WeatherEmbed)
    Implements base embed for day weather (today, tomorrow)
.. class:: TodayWeatherForecastEmbed(DayWeatherForecastEmbed)
    Implements embed for today weather
.. class:: TomorrowWeatherForecastEmbed(DayWeatherForecastEmbed)
    Implements embed for tomorrow weather
.. class:: TemperatureWeatherForecast(WeatherEmbed)
"""

import datetime

import discord

from . import (
    settings,
    weather_api
)
from .weather_api import measures


class WeatherEmbed(discord.Embed):
    """ Implements base weather embed """

    section_divider = '- ' * 40

    def __init__(self):
        super().__init__()

        self.set_author(name=settings.EMBEDS_AUTHOR)

    def add_header(self, header: str) -> None:
        """
        Add header of some content section.
        Will set field in `inline=False` way with `section_divider` in value.

        :param header: header of the content section
        :type header: str

        :return: None
        :rtype: None
        """

        self.add_field(name=header, value=self.section_divider, inline=False)

    def add_section(self, header: str, fields: dict) -> None:
        """
        Add section (independent info; contains section header and section fields).

        :param header: header of the content section
        :type header: str
        :param fields: mapping of the pairs {field_name: field_value}
        :type fields: dict

        :return: None
        :rtype: None
        """

        self.add_header(header)
        for field_name, field_value in fields.items():
            self.add_field(name=field_name, value=field_value)

    def add_compact_section(self, header: str, content: str) -> None:
        """
        Add compact section: `inline=False` field with value that ends with section divider.

        Unfortunately, this is Embed limitation for 25 fields. With full sections it is hard to
        control this restrictions.
        So, for big data use this type of sections.

        :param header: header
        :type header: str
        :param content: content
        :type content: str

        :return: None
        :rtype: None
        """

        self.add_field(
            name=header,
            value='\n'.join(
                (
                    self.section_divider,
                    content
                )
            ),
            inline=False
        )


class CurrentWeatherEmbed(WeatherEmbed):
    """ Implements current weather embed """

    def __init__(self, current_weather: weather_api.parsers.CurrentWeatherParser):
        super().__init__()

        self.title = f'Current weather in the {current_weather.city_name}'
        self.description = 'It`s current weather.'

        self.set_thumbnail(url=current_weather.weather.icon_url)

        self.add_section(
            'Shortly',
            {
                 'Status': current_weather.weather.main,
                 'Description': current_weather.weather.description
            }
        )

        self.add_section(
            'Temperature stats',
            {
                'Now': f'{current_weather.weather.temperature:+} {measures.TEMPERATURE}',
                'Feels like': f'{current_weather.weather.temperature_feels_like:+} {measures.TEMPERATURE}',
                'Min/Max': '\n'.join(
                    (
                        f'Min: {current_weather.weather.temperature_min:+} {measures.TEMPERATURE}',
                        f'Max: {current_weather.weather.temperature_max:+} {measures.TEMPERATURE}'
                    )
                )
            }
        )

        self.add_section(
            'Sunrise-Sunset time',
            {
                'Sunrise at [GMT]': current_weather.sunrise_datetime.time().isoformat(),
                'Sunset at [GMT]': current_weather.sunset_datetime.time().isoformat()
            }
        )

        self.add_section(
            'Other weather stats',
            {
                'Pressure': f'{current_weather.weather.pressure} {measures.PRESSURE}',
                'Humidity': f'{current_weather.weather.humidity} {measures.HUMIDITY}',
                'Wind speed': f'{current_weather.weather.wind_speed} {measures.WIND_SPEED}',
                'Clouds': f'{current_weather.weather.clouds} {measures.CLOUDS}'
            }
        )

        self.add_section(
            'City info',
            {
                'City name': current_weather.city_name,
                'Country code': current_weather.country_code,
                'Timezone': f'{current_weather.timezone_in_hours_shift:+}'
            }
        )

        self.set_footer(text=f"Data was computed at {current_weather.data_calculation_datetime.isoformat(' ')} [GMT]")


class DayWeatherForecastEmbed(WeatherEmbed):
    """ Implements detailed weather forecast for one day """

    def __init__(self,
                 weather_forecast: weather_api.parsers.WeatherForecastParser,
                 day_weather_forecast: weather_api.parsers.DayWeatherForecastParser
                 ) -> None:
        super().__init__()

        for period_parser in day_weather_forecast.period_parsers:
            self.add_compact_section(
                f"By {period_parser.data_forecasting_datetime.time().isoformat()}",
                '\n'.join(
                    (
                        f'Temperature:  {period_parser.temperature:+} {measures.TEMPERATURE}',
                        f'Feels like:   {period_parser.temperature_feels_like:+} {measures.TEMPERATURE}',
                        f'Humidity:     {period_parser.humidity} {measures.HUMIDITY}',
                        f'Clouds:       {period_parser.temperature_max} {measures.CLOUDS}',
                        f'Pressure:     {period_parser.pressure} {measures.PRESSURE}',
                        f'Wind speed:   {period_parser.wind_speed} {measures.WIND_SPEED}'
                    )
                )
            )

        self.add_section(
            'City info',
            {
                'City name': weather_forecast.city_name,
                'Country code': weather_forecast.country_code,
                'Timezone': f'{weather_forecast.timezone_in_hours_shift:+}'
            }
        )


class TodayWeatherForecastEmbed(DayWeatherForecastEmbed):
    """ Implements detailed weather forecast for today """

    def __init__(self, weather_forecast: weather_api.parsers.WeatherForecastParser):
        super().__init__(weather_forecast, weather_forecast.today_forecast)

        self.title = f'Today weather forecast in the {weather_forecast.city_name}'
        self.description = 'It`s detailed weather forecast for today.'


class TomorrowWeatherForecastEmbed(DayWeatherForecastEmbed):
    """ Implements detailed weather forecast for tomorrow """

    def __init__(self, weather_forecast: weather_api.parsers.WeatherForecastParser):
        super().__init__(weather_forecast, weather_forecast.tomorrow_forecast)

        self.title = f'Tomorrow weather forecast in the {weather_forecast.city_name}'
        self.description = 'It`s detailed weather forecast for tomorrow.'


class TemperatureWeatherForecast(WeatherEmbed):
    """ Implements short (only temperature stats) weather foreacst """

    def __init__(self, weather_forecast: weather_api.parsers.WeatherForecastParser) -> None:
        super().__init__()

        self.title = f'Temperature weather forecast in the {weather_forecast.city_name}'
        self.description = 'It`s short (only temperature stats) weather forecast for 5 days.'

        day_date = datetime.date.today()
        for day_weather_forecast in weather_forecast.all_5_day_forecast:
            self.add_section(
                f'Temperature by {day_date.isoformat()}',
                {
                    ' Min': f'{day_weather_forecast.temperature_min_of_the_day:+} {measures.TEMPERATURE}',
                    ' Max': f'{day_weather_forecast.temperature_max_of_the_day:+} {measures.TEMPERATURE}'
                }
            )

            day_date += datetime.timedelta(days=1)

        self.add_section(
            'City info',
            {
                'City name': weather_forecast.city_name,
                'Country code': weather_forecast.country_code,
                'Timezone': f'{weather_forecast.timezone_in_hours_shift:+}'
            }
        )
