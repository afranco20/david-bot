"""
Module Docstring
"""

import os

from discord import Client, Game
from discord.ext import commands

from src.cogs import my_commands


class MyBot(commands.Bot):
    async def on_ready(self):
        print('Logged on as', self.user)
        await self.change_presence(activity=Game(name='Making a bot 🤖'))

    async def on_message(self, message):
        if message.content == 'ping':
            await message.channel.send('pong')
        if message.content == 'testing':
            await message.channel.send('hi :)')

        await self.process_commands(message)


def run():
    """ Main entry point of the app """
    token = os.getenv("DISCORD_BOT_SECRET")

    client = MyBot(command_prefix=commands.when_mentioned_or('!'))

    client.add_cog(my_commands(client))

    client.run(token)
