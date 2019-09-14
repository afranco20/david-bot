#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Alexander Franco"
__version__ = "0.1.0"
__license__ = "MIT"

import os

from discord import Client, Game
from discord.ext import commands


class MyBot(commands.Bot):
    async def on_ready(self):
        print('Logged on as', self.user)
        await self.change_presence(activity=Game(name='Making a bot 🤖'))

    async def on_message(self, message):
        if message.content == 'ping':
            await message.channel.send('pong')


def run():
    """ Main entry point of the app """
    token = os.environ.get("DISCORD_BOT_SECRET")

    client = MyBot(command_prefix=commands.when_mentioned_or('!'))
    client.run(token)
