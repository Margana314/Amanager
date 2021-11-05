import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="mcstats", description="Afficher les statistiques d'un serveur minecraft", options=[
                create_option(
                name="ip",
                description="IP",
                option_type=3,
                required=True
                )])
    async def _mcstats(self, ctx, ip: str):
        embed = discord.Embed(title="Ping d'un serveur Minecraft")
        embed.add_field(name=f"IP : {ip}", value="** **", inline=False)
        embed.set_image(url=f"http://status.mclive.eu/{ip}/{ip}/25565/banner.png")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("mcstats")