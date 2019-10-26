from json import loads
from os import getenv
from urllib import request
from datetime import datetime
from time import strftime

from discord import Embed
from discord.ext import commands


class Weather(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api_calls = 0

    def generateQuery(self):
        # define query parameters
        api_url = 'https://api.darksky.net/forecast/'
        key = getenv('DARK_SKY_SECRET')
        latitude = '28.4196'
        longitude = '-81.2937'
        exclude = 'minutely,hourly,daily,flags'
        language = 'en'

        # generate query string
        query = f'{api_url}{key}/{latitude},{longitude}?exclude={exclude}&lang={language}'

        return query

    def rateLimit(self, query):
        if self.api_calls >= 500:
            return
        else:
            response = request.urlopen(query)
            self.api_calls = int(response.getheader('X-Forecast-API-Calls'))
            return response

    def parseResponse(self, response):
        json_data = loads(response.read())

        # f = open('logs.json', 'w')
        # print(json_data, file=f)
        # f.close()

        self.last_update = datetime.fromtimestamp(json_data['currently']['time'])
        self.last_update = self.last_update.strftime(r'%b %d, %I:%M:%S %p')

        properties = ['summary', 'icon', 'apparentTemperature', 'temperature', 'precipProbability']
        data = []

        for x in properties:
            data.append(json_data['currently'][x])

        return data

    def generateEmbed(self, data):
        summary = data[0]
        # icon = data[1]

        weather_embed = Embed(title='Orlando', description=summary, color=0x0091ea)
        # weather_embed.set_thumbnail(url="...")

        names = ['Feels Like', 'Actual', 'Precipitation Probability']
        fields = list(zip(names, data[2:]))

        for x in fields:
            weather_embed.add_field(name=x[0], value=round(x[1]))

        weather_embed.set_footer(text=f"Powered by Dark Sky ◉ Updated: {self.last_update}")

        return weather_embed

    @commands.command()
    async def weather(self, ctx):
        query = self.generateQuery()
        response = self.rateLimit(query)
        data = self.parseResponse(response)
        weather_embed = self.generateEmbed(data)

        await ctx.send(embed=weather_embed)
