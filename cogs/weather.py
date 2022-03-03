import discord, requests, json
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="weather", description="Afficher la météo d'une ville !", options=[
                create_option(
                name="ville",
                description="Ville du monde",
                option_type=3,
                required=True
                )])
    async def _weather(self, ctx, ville: str):
        a_file = open("no-move.json", "r")
        json_object_nm = json.load(a_file)
        a_file.close()
        openweathermap_api_key = json_object_nm['token']['openweathermap']
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?appid={openweathermap_api_key}&q={ville}").json()
        if ville.lower() == "antarctique" or ville.lower() == "antarctica":
            await ctx.send("Cet endroit a été mis sur liste noire pour cause de ralentissement. Merci !")
        elif ville.lower() == "soleil":
            embed = discord.Embed(title=f"Météo sur le Soleil", color=0xFFD700)
            embed.add_field(name="Desc.", value="Il fait chaud.", inline=True)
            embed.add_field(name="Localisation", value="<a:sun:790561041532190771> Au centre du système solaire.", inline=True)
            embed.add_field(name="Temp. moyenne", value="5778°K (~5505°C)", inline=True)
            embed.add_field(name="Temp. ressentie", value="Beaucoup de chaleur.", inline=True)
            embed.add_field(name="Temp. interne", value="15.1°MK (~15 099 700°C)", inline=True)
            embed.add_field(name="Humidité", value="0 %", inline=True)
            embed.add_field(name="Pression atmosphérique", value="Beaucoup trop.", inline=True)
            embed.add_field(name="Vitesse du vent", value="217km/s", inline=True)
            embed.set_thumbnail(url="http://openweathermap.org/img/wn/01d@2x.png")
            await ctx.send(embed=embed)
        else:
            if response["cod"] != "404":
                weather_description = response['weather'][0]['description']
                if weather_description == "broken clouds": weather_description, w_color = "nuages brisés", 0xafe1f8
                elif weather_description == "few clouds": weather_description, w_color = "peu nuageux", 0xafe1f8
                elif weather_description == "clear sky": weather_description, w_color = "ciel clair", 0x0181e4
                elif weather_description == "haze": weather_description, w_color = "brumeux", 0xadaeb4
                elif weather_description == "scattered clouds": weather_description, w_color = "nuages éparpillés", 0xafe1f8
                elif weather_description == "overcast clouds": weather_description, w_color = "nuages couverts", 0x939da6
                elif weather_description == "light snow": weather_description, w_color = "neige légère", 0xc3cdda
                elif weather_description == "light rain": weather_description, w_color = "pluie légère", 0xdde2e4
                elif weather_description == "mist": weather_description, w_color = "brumeux", 0xadaeb4
                elif weather_description == "moderate rain": weather_description, w_color = "pluie modérée", 0xdde2e4

                embed = discord.Embed(title=f"Météo à {ville}", description=f"https://openweathermap.org/city/{str(response['id'])}", color=w_color)
                embed.add_field(name="Desc.", value=f"{weather_description}", inline=True)
                embed.add_field(name="Localisation", value=f":flag_{response['sys']['country'].lower()}: {response['sys']['country']}", inline=True)
                embed.add_field(name="Temp. moyenne", value=f"{str(round(response['main']['temp'] - 273.15))}°C", inline=True)
                embed.add_field(name="Temp. ressentie", value=f"{str(round(response['main']['feels_like'] - 273.15))}°C", inline=True)
                embed.add_field(name="Temp. min. | max.", value=f"{str(round(response['main']['temp_min'] - 273.15))}°C | {str(round(response['main']['temp_max'] - 273.15))}°C", inline=True)
                embed.add_field(name="Humidité", value=f"{response['main']['humidity']}%", inline=True)
                embed.add_field(name="Pression atmosphérique", value=f"{response['main']['pressure']}hPa", inline=True)
                embed.add_field(name="Vitesse du vent", value=f"{response['wind']['speed']}m/s", inline=True)
                embed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{response['weather'][0]['icon']}@2x.png")
                await ctx.send(embed=embed)
            else:
                await ctx.send("Ville non trouvée.")

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("weather")