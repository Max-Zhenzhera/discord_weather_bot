"""
Contains settings.

* Path constants
.. const:: CORE_DIR
.. const:: PROJECT_DIR

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


# Project paths
CORE_DIR = pathlib.Path(__file__).parent
PROJECT_DIR = CORE_DIR.parent

# Tokens
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
WEATHER_API_TOKEN = os.getenv('WEATHER_API_TOKEN')

# Bot settings
COMMAND_PREFIX = '.'
DESCRIPTION = ''' Weather bot that fetch needed data quickly, convenient and easy! '''
ACTIVITY = discord.Activity(name='the weather :)', type=discord.ActivityType.watching)
OPTIONS = {
    'activity': ACTIVITY
}
EMBEDS_AUTHOR = 'Your small weather helper :)'
