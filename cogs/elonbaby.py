import discord, random, string
from discord.ext import commands
from discord_slash import cog_ext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="elonbaby", description="Générer un prénom comme celui qu'aurait dû porter le bébé d'Elon Musk !")
    async def _elonbaby(self, ctx):
        lettres_accolees = ["Æ", "Œ"]
        symboles_maths = ["+", "-", "x", "÷"]
        await ctx.send(f"Prénom généré pour le prochain bébé d'Elon Musk\n=> {random.choice(string.ascii_uppercase)} {random.choice(lettres_accolees)} {random.choice(string.ascii_uppercase)} {random.choice(symboles_maths)} {random.randint(11,99)}")   

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("elonbaby")