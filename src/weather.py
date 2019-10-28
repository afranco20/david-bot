from json import loads
from os import getenv
from urllib import request
from datetime import datetime, timedelta
from time import strftime

from discord import Embed
from discord.ext import commands


class Weather(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api_calls = 0
        self.last_update = datetime.now() - timedelta(minutes=10)

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

    def rateLimit(self):
        delta = datetime.now() - self.last_update
        interval = timedelta(minutes=10)

        if self.api_calls >= 200:
            return False
        if delta < interval:
            return False

        return True

    def getResponse(self, update: bool, query: str):
        response = request.urlopen(query)
        self.api_calls = int(response.getheader('X-Forecast-API-Calls'))
        return response

    def parseResponse(self, response):
        json_data = loads(response.read())

        # f = open('logs.json', 'w')
        # print(json_data, file=f)
        # f.close()

        self.last_update = datetime.fromtimestamp(json_data['currently']['time'])

        properties = ['summary', 'icon', 'apparentTemperature', 'temperature', 'precipProbability']
        data = []

        for x in properties:
            data.append(json_data['currently'][x])

        data.append(self.last_update.strftime(r'%b %d, %I:%M %p'))

        return data

    def colorizer(self, icon: str):
        switch = {
            'clear-day': 0xFFD600,
            'clear-night': 0x90A4AE,
            'rain': 0x2962FF,
            'snow': 0xFFFFFF,
            'sleet': 0xB3E5FC,
            'wind': 0xBDBDBD,
            'fog': 0x9E9E9E,
            'cloudy': 0x757575,
            'partly-cloudy-day': 0xb29400,
            'partly-cloudy-night': 0x647e8b,
            'hail': 0x00B0FF,
            'thunderstorm': 0xFF8F00,
            'tornado': 0x42424
        }

        return switch.get(icon, 0x2ecc71)

    def generateEmbed(self, data):
        summary = data[0]
        color = self.colorizer(data[1])

        weather_embed = Embed(title='Orlando', description=summary, color=color)
        # weather_embed.set_thumbnail(url="...")

        names = ['Feels Like', 'Actual', 'Precipitation Probability']
        fields = list(zip(names, data[2:-1]))

        for n, v in fields:
            weather_embed.add_field(name=n, value=round(v))

        weather_embed.set_footer(text=f"Powered by Dark Sky ◉ Updated: {data[-1]}")

        return weather_embed

    @commands.command()
    async def weather(self, ctx):
        query = self.generateQuery()
        update = self.rateLimit()

        if update:
            response = self.getResponse(update, query)
            self.cache = self.parseResponse(response)

        weather_embed = self.generateEmbed(self.cache)

        await ctx.send(embed=weather_embed)
