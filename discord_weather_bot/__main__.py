"""
Entry point
"""

from discord_weather_bot import bot


if __name__ == '__main__':
    discord_weather_bot = bot.DiscordWeatherBot()
    discord_weather_bot.run()
