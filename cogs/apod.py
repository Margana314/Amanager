import discord, requests, json
from discord.ext import commands
from discord_slash import ButtonStyle, cog_ext
from discord_slash.utils.manage_components import *

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="apod", description="Afficher la photo de la NASA du jour")
    async def _apod(self, ctx):
        await ctx.defer()
        a_file = open("no-move.json", "r")
        json_object_nm = json.load(a_file)
        a_file.close()
        apod_api_key = json_object_nm['token']['apod']
        apod_api_response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={apod_api_key}").json()

        buttons = [
            create_button(
                style = ButtonStyle.blue,
                label = "Afficher la description",
                custom_id = "show_desc"
            )
        ]

        embed = discord.Embed(colour = discord.Colour.purple(), title="Astronomy Picture Of the Day — APOD")
        embed.add_field(name=f"{apod_api_response['title']}", value="** **", inline=False)
        try:
            embed.set_image(url=apod_api_response["hdurl"])
        except KeyError:
            embed.add_field(name="** **", value=f"[Vidéo]({apod_api_response['url']})", inline=False)
        
        action_row = create_actionrow(*buttons)
        choice_made = await ctx.send(embed=embed, components=[action_row])

        def check(m):
            return m.author_id == ctx.author_id and m.origin_message.id == choice_made.id

        button_ctx = await wait_for_component(self.bot, components=action_row, check=check)
        if button_ctx.custom_id == "show_desc":
            await button_ctx.send(content=apod_api_response['explanation'], hidden=True)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("apod")