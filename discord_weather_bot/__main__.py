"""
Entry point.
"""

from __future__ import annotations

# add package to global path -------------------------------------------------------------------------------------------
import sys
import pathlib


sys.path.append(pathlib.Path(__file__).parent.parent.__str__())
# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    from discord_weather_bot import bot

    discord_weather_bot = bot.DiscordWeatherBot()
    discord_weather_bot.run()
