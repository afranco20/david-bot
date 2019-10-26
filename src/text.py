"""
Module Docstring
"""

from discord.ext import commands


class Text(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shrug(self, ctx):
        await ctx.send(r'¯\_(ツ)_/¯')
