import discord, requests
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_components import *

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="cat", description="Afficher une photo aléatoire de chat")
    async def _cat(self, ctx):
        await ctx.defer()
        animal_images = requests.get("http://aws.random.cat//meow").json()
        embed = discord.Embed(title="Un chat sauvage apparaît !", description="Miaou !", colour = discord.Colour.purple())
        embed.set_image(url=animal_images['file'])
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("cat")