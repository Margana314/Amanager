import discord, requests
from discord.ext import commands
from discord_slash import cog_ext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="dog", description="Afficher une photo aléatoire de chien !")
    async def _dog(self, ctx):
        await ctx.defer()
        animal_images = requests.get("https://random.dog/woof.json").json()
        embed = discord.Embed(title="Un chien sauvage apparaît !", description="Ouaf !")
        embed.set_image(url=animal_images['url'])
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("dog")