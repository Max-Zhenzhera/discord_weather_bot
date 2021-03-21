"""
Contains implementation of the weather bot.

.. class:: DiscordWeatherBot(commands.Bot)
    Implements discord weather bot
"""

import aiohttp
import loguru
import discord
from discord.ext import commands

from . import (
    cogs,
    settings
)


class DiscordWeatherBot(discord.ext.commands.Bot):
    """ Implements Discord Weather Bot """

    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(settings.COMMAND_PREFIX),
            description=settings.DESCRIPTION,
            **settings.OPTIONS
        )

        self.session = aiohttp.ClientSession()

        loguru.logger.add(settings.ERROR_LOG, level='ERROR')
        self.logger = loguru.logger

        self.add_cog(cogs.Events(self, self.logger))
        self.add_cog(cogs.CommonCommands(self))
        self.add_cog(cogs.WeatherCommands(self, self.session, self.logger))

    def run(self):
        """ Run bot (do not require token - it is already passed) """
        super().run(settings.DISCORD_BOT_TOKEN)
