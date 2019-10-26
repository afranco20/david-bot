"""
Module Docstring
"""

from os import getenv

from discord import Game
from discord.ext import commands

from src.text import Text
from src.weather import Weather


class David(commands.Bot):

    async def on_ready(self):
        print('Logged on as', self.user)
        await self.change_presence(activity=Game(name='Making a bot 🤖'))

    async def on_message(self, message):
        if message.content == 'ping':
            await message.channel.send('pong')

        await self.process_commands(message)


def run():
    """ Main entry point of the app """
    token = getenv("DISCORD_BOT_SECRET")

    client = David(command_prefix=commands.when_mentioned_or('!'))
    client.add_cog(Text(client))
    client.add_cog(Weather(client))

    client.run(token)
