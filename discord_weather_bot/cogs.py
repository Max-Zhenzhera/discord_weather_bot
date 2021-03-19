"""
Implements cogs (organized code) for bot.

.. class:: Events(discord.ext.commands.Cog)
    Handle simple events
.. class:: CommonCommands(discord.ext.commands.Cog)
    Handle common commands
.. class:: WeatherCommands(discord.ext.commands.Cog)
    Handle weather commands
"""

from typing import (
    Optional
)

import aiohttp
import discord
import loguru
from discord.ext import commands

from . import (
    weather_api,
    embeds
)


class Events(discord.ext.commands.Cog):
    """ Implements cog extension that handle simple events """

    def __init__(self, bot: discord.ext.commands.Bot, logger: loguru.logger):
        self.bot = bot
        self.logger = logger

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.logger.info('BOT IS RUNNING')


class CommonCommands(discord.ext.commands.Cog):
    """ Implements cog extension that handle common commands """

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    @commands.command(
        name='ping',
        aliases=['p'],
        description='Call the command when you want to see the connection latency (and bot connection at all)'
    )
    async def ping(self, ctx: discord.ext.commands.Context):
        """ Check the connection latency """
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

    @commands.command(
        name='echo',
        aliases=['e'],
        description='Call the command when you want to see the echo answer from the bot'
    )
    async def echo(self, ctx: discord.ext.commands.Context):
        """ Echo message """
        await ctx.send(ctx.message.content.split(' ', 1)[1])


class WeatherCommands(discord.ext.commands.Cog):
    """ Implements cog extension that handle weather commands """

    def __init__(self, bot: commands.Bot, session: aiohttp.ClientSession, logger: loguru.logger):
        self.bot = bot
        self.session = session
        self.logger = logger

    async def cog_command_error(self,
                                ctx: discord.ext.commands.Context, error: discord.ext.commands.CommandInvokeError
                                ) -> None:
        is_need_to_log = False

        internal_error = error.original

        if isinstance(internal_error, weather_api.errors.WeatherApiDeveloperError):
            user_message = 'Oops! It seems like it is my error, sorry, try to use the command later!'

            is_need_to_log = True
        elif isinstance(internal_error, weather_api.errors.WeatherApiNotFoundError):
            user_message = 'Hmm... It seems like you sent me wrong data: e.g. it might be incorrect city name. '
            user_message += 'Please, be sure in your input data and try to use the command again!'
        elif isinstance(internal_error, weather_api.errors.WeatherApiTooManyRequestsError):
            user_message = 'Oops! It seems like pure bot is overloaded.'
            user_message += 'Please, give bot some time for relax and try to use the command again!'
        elif isinstance(internal_error, weather_api.errors.WeatherApiError):
            user_message = 'Oops! It seems like it is my error, sorry, try to use the command later!'

            is_need_to_log = True
        else:
            # no one weather api error caught -> there is not `weather_api.errors.WeatherApiError`
            raise internal_error

        if is_need_to_log:
            self.logger.exception(error)

        await ctx.send(user_message)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # !now
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @commands.command(
        name='now',
        aliases=['n', 'w', 'weather'],
        brief='Show the current weather by the city name',
        description='Call the command when you want to see the current weather in the city',
        help=(
                'Call the command in the above written way. '
                'If it is the city from country that you did not expect to check: '
                'then pass after the city name additional country code argument for more accurate searching.'
                '\nExamples:\n\t!now kiev\n\t!weather odessa us\n\t!w rome it'
        )
    )
    async def get_current_weather(self, ctx: discord.ext.commands.Context,
                                  city_name: str, country_code: Optional[str] = None
                                  ) -> None:
        """
        Send tomorrow weather data with embed.

        :param ctx: context
        :type ctx: discord.ext.commands.Context
        :param city_name: city name (to get weather data)
        :type city_name: str
        :param country_code: non-required country code for more accurate searching
        :type country_code: Optional[str]

        :return: None
        :rtype: None
        """

        current_weather = await weather_api.api.get_current_weather_by_city_name(self.session, city_name, country_code)
        current_weather_embed = embeds.CurrentWeatherEmbed(current_weather)

        await ctx.send(embed=current_weather_embed)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # !today
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @commands.command(
        name='today',
        aliases=['td'],
        brief='Show today weather forecast by the city name',
        description='Call the command when you want to see the today weather forecast in the city',
        help=(
                'Call the command in the above written way. '
                'If it is the city from country that you did not expect to check: '
                'then pass after the city name additional country code argument for more accurate searching.'
                '\nExamples:\n\t!today kiev\n\t!td rome it'
        )
    )
    async def get_today_weather_forecast(self, ctx: discord.ext.commands.Context,
                                         city_name: str, country_code: Optional[str] = None
                                         ) -> None:
        """
        Send today weather forecast with embed.

        :param ctx: context
        :type ctx: discord.ext.commands.Context
        :param city_name: city name (to get weather data)
        :type city_name: str
        :param country_code: non-required country code for more accurate searching
        :type country_code: Optional[str]

        :return: None
        :rtype: None
        """

        weather_forecast = await weather_api.api.get_weather_forecast_by_city_name(
            self.session, city_name, country_code
        )
        today_weather_forecast_embed = embeds.TodayWeatherForecastEmbed(weather_forecast)

        await ctx.send(embed=today_weather_forecast_embed)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # !tomorrow
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @commands.command(
        name='tomorrow',
        aliases=['tm', 'tmr'],
        brief='Show tomorrow weather forecast by the city name',
        description='Call the command when you want to see the tomorrow weather forecast in the city',
        help=(
                'Call the command in the above written way. '
                'If it is the city from country that you did not expect to check: '
                'then pass after the city name additional country code argument for more accurate searching.'
                '\nExamples:\n\t!tomorrow kiev\n\t!tm rome it'
        )
    )
    async def get_tomorrow_weather(self, ctx: discord.ext.commands.Context,
                                   city_name: str, country_code: Optional[str] = None
                                   ) -> None:
        """
        Send tomorrow weather forecast with embed.

        :param ctx: context
        :type ctx: discord.ext.commands.Context
        :param city_name: city name (to get weather data)
        :type city_name: str
        :param country_code: non-required country code for more accurate searching
        :type country_code: Optional[str]

        :return: None
        :rtype: None
        """

        weather_forecast = await weather_api.api.get_weather_forecast_by_city_name(
            self.session, city_name, country_code
        )
        tomorrow_weather_forecast_embed = embeds.TomorrowWeatherForecastEmbed(weather_forecast)

        await ctx.send(embed=tomorrow_weather_forecast_embed)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # !forecast
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @commands.command(
        name='forecast',
        aliases=['f', 'fr', 'frc', 'frcst'],
        brief='Show short weather forecast by the city name',
        description='Call the command when you want to see the temperature weather forecast in the city',
        help=(
                'Call the command in the above written way. '
                'If it is the city from country that you did not expect to check: '
                'then pass after the city name additional country code argument for more accurate searching.'
                '\nExamples:\n\t!forecast kiev\n\t!f rome it'
        )
    )
    async def get_temperature_weather_forecast(self, ctx: discord.ext.commands.Context,
                                               city_name: str, country_code: Optional[str] = None
                                               ) -> None:
        """
        Send temperature weather forecast with embed.

        :param ctx: context
        :type ctx: discord.ext.commands.Context
        :param city_name: city name (to get weather data)
        :type city_name: str
        :param country_code: non-required country code for more accurate searching
        :type country_code: Optional[str]

        :return: None
        :rtype: None
        """

        weather_forecast = await weather_api.api.get_weather_forecast_by_city_name(
            self.session, city_name, country_code
        )
        temperature_weather_forecast_embed = embeds.TemperatureWeatherForecast(weather_forecast)

        await ctx.send(embed=temperature_weather_forecast_embed)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
