import discord, random
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="rng", description="Générer un nombre aléatoire !", options=[
                create_option(
                name="nombre1",
                description="Nombre 1",
                option_type=4,
                required=True
                ),
                create_option(
                name="nombre2",
                description="Nombre 2",
                option_type=4,
                required=True
                )])
    async def _rng(self, ctx, nombre1: int, nombre2: int):
        n_min, n_max = -4294967296, 4294967296
        if nombre1 > nombre2:
            await ctx.send(f"{ctx.author.mention} Le nombre 1 est plus grand que le nombre 2... relance la commande en faisant en sorte que le nombre 1 soit **plus petit** que le nombre 2.")
        elif nombre1 < n_min or nombre2 > n_max:
            await ctx.send(f"{ctx.author.mention} L'intervalle entrée est hors champ, la limite est de [{n_min} ; {n_max}] !")
        else:
            random_nb = random.randint(nombre1, nombre2)
            embed = discord.Embed(title=f"Générateur de nombres aléatoires")
            embed.add_field(name=f"Nombre généré : {random_nb}", value=f"Intervalle de valeurs : {nombre1} et {nombre2}")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("rng")