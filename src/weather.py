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

    def colorizer(self, icon):
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

        print(icon)
        return switch.get(icon, 0x2ecc71)

    def generateEmbed(self, data):
        summary = data[0]
        color = self.colorizer(data[1])

        weather_embed = Embed(title='Orlando', description=summary, color=color)
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
