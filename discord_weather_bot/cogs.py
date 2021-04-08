"""
Implements cogs (organized code) for bot.

.. class:: Events(discord.ext.commands.Cog)
    Handle simple events
.. class:: CommonCommands(discord.ext.commands.Cog)
    Handle common commands
.. class:: WeatherCommands(discord.ext.commands.Cog)
    Handle weather commands
"""

import logging
from typing import (
    Optional
)

import aiohttp
import discord
from discord.ext import commands

from . import (
    embeds,
    weather_api,
    settings
)


logger = logging.getLogger(__name__)


class Events(discord.ext.commands.Cog):
    """ Implements cog extension that handle simple events """

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logger.info('BOT IS RUNNING')

    @commands.Cog.listener()
    async def on_command_error(self,
                               ctx: discord.ext.commands.Context, error: discord.ext.commands.CommandError
                               ) -> None:
        if isinstance(error, discord.ext.commands.UserInputError):
            await ctx.send(str(error))
        elif isinstance(error, discord.ext.commands.CommandNotFound):
            message = 'Oops! It seems like command is not found!'
            message += f'Try to explore right usage with ``` {settings.COMMAND_PREFIX}help ```'
            await ctx.send(message)


class CommonCommands(discord.ext.commands.Cog):
    """ Implements cog extension that handle common commands """

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    @commands.command(
        name='ping',
        aliases=['p', 'P', 'PING'],
        description='Call the command when you want to see the connection latency (and bot connection at all)'
    )
    async def ping(self, ctx: discord.ext.commands.Context):
        """ Check the connection latency """
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

    @commands.command(
        name='echo',
        aliases=['e', 'E', 'ECHO'],
        description='Call the command when you want to see the echo answer from the bot'
    )
    async def echo(self, ctx: discord.ext.commands.Context, *, message: str):
        """ Echo message """
        await ctx.send(message)


class WeatherCommands(discord.ext.commands.Cog):
    """ Implements cog extension that handle weather commands """

    def __init__(self, bot: commands.Bot, session: aiohttp.ClientSession):
        self.bot = bot
        self.session = session

    async def cog_command_error(self,
                                ctx: discord.ext.commands.Context, error: discord.ext.commands.CommandError
                                ) -> None:
        if isinstance(error, discord.ext.commands.CommandInvokeError):
            is_need_to_log = False
            internal_error = error.original

            user_message = 'Oops! It seems like it is my error, sorry, try to use the command later!'

            if isinstance(internal_error, weather_api.errors.WeatherApiError):
                # catch all weather API errors
                if isinstance(internal_error, weather_api.errors.WeatherApiDeveloperError):
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
                # no one weather API error is caught
                is_need_to_log = True

            if is_need_to_log:
                logger.exception(str(internal_error), exc_info=error)

            await ctx.send(user_message)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # !now
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @commands.command(
        name='now',
        aliases=['n', 'N', 'NOW', 'w', 'W', 'weather', 'WEATHER'],
        brief='Show the current weather by the city name',
        description='Call the command when you want to see the current weather in the city',
        help=(
                'Call the command in the above written way. '
                'If it is the city from country that you did not expect to check: '
                'then pass after the city name additional country code argument for more accurate searching.'
                '\nExamples:'
                f'\n\t{settings.COMMAND_PREFIX}now kiev'
                f'\n\t{settings.COMMAND_PREFIX}weather odessa us'
                f'\n\t{settings.COMMAND_PREFIX}w rome it'
        )
    )
    async def get_current_weather(self, ctx: discord.ext.commands.Context,
                                  city_name: str, country_code: Optional[str] = None
                                  ) -> None:
        """
        Send current weather data with embed.

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
        aliases=['td', 'TD', 'TODAY'],
        brief='Show today weather forecast by the city name',
        description='Call the command when you want to see the today weather forecast in the city',
        help=(
                'Call the command in the above written way. '
                'If it is the city from country that you did not expect to check: '
                'then pass after the city name additional country code argument for more accurate searching.'
                '\nExamples:'
                f'\n\t{settings.COMMAND_PREFIX}today kiev'
                f'\n\t{settings.COMMAND_PREFIX}td rome it'
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
        aliases=['tm', 'TM', 'TOMORROW'],
        brief='Show tomorrow weather forecast by the city name',
        description='Call the command when you want to see the tomorrow weather forecast in the city',
        help=(
                'Call the command in the above written way. '
                'If it is the city from country that you did not expect to check: '
                'then pass after the city name additional country code argument for more accurate searching.'
                '\nExamples:'
                f'\n\t{settings.COMMAND_PREFIX}tomorrow kiev'
                f'\n\t{settings.COMMAND_PREFIX}tm rome it'
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
        aliases=['f', 'F', 'FORECAST'],
        brief='Show short weather forecast by the city name',
        description='Call the command when you want to see the temperature weather forecast in the city',
        help=(
                'Call the command in the above written way. '
                'If it is the city from country that you did not expect to check: '
                'then pass after the city name additional country code argument for more accurate searching.'
                '\nExamples:'
                f'\n\t{settings.COMMAND_PREFIX}forecast kiev'
                f'\n\t{settings.COMMAND_PREFIX}f rome it'
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
