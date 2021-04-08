"""
Contains settings.

* Path constants
.. const:: CORE_DIR
.. const:: PROJECT_DIR

* Logging
.. const:: LOGGING_CONFIG_PATH

* Tokens
.. const:: DISCORD_BOT_TOKEN
.. const:: WEATHER_API_TOKEN

* Bot settings
.. const:: COMMAND_PREFIX       | >
.. const:: DESCRIPTION          | > > passed on bot initialization
.. const:: ACTIVITY             | > >
.. const:: OPTIONS              | >
.. const:: EMBEDS_AUTHOR        | > indicated in each embed
"""

import pathlib
import os

import discord
from dotenv import load_dotenv


load_dotenv()


# Project paths
CORE_DIR = pathlib.Path(__file__).parent
PROJECT_DIR = CORE_DIR.parent

# Logging
LOGGING_CONFIG_PATH = CORE_DIR / 'utils' / 'logging_' / 'logging_config.yaml'

# Tokens
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
WEATHER_API_TOKEN = os.getenv('WEATHER_API_TOKEN')

# Bot settings
COMMAND_PREFIX = '.'
DESCRIPTION = ''' Weather bot - brings weather from all world easy and quickly! '''
ACTIVITY = discord.Activity(name='the weather :)', type=discord.ActivityType.watching)
OPTIONS = {
    'activity': ACTIVITY
}
EMBEDS_AUTHOR = 'Your small weather helper :)'
