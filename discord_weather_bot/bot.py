"""
Contains implementation of the weather bot.

.. class:: DiscordWeatherBot(commands.Bot)
    Implements discord weather bot
"""

import aiohttp
import discord
from discord.ext import commands

from . import (
    cogs,
    settings
)
from .utils.logging_ import logging_


logging_.setup_logging(settings.LOGGING_CONFIG_PATH)


class DiscordWeatherBot(discord.ext.commands.Bot):
    """ Implements Discord Weather Bot """

    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(settings.COMMAND_PREFIX),
            description=settings.DESCRIPTION,
            **settings.OPTIONS
        )

        self.session = aiohttp.ClientSession()

        self.add_cog(cogs.Events(self))
        self.add_cog(cogs.CommonCommands(self))
        self.add_cog(cogs.WeatherCommands(self, self.session))

    def run(self):
        """ Run bot (do not require token - it is already passed) """
        super().run(settings.DISCORD_BOT_TOKEN)
