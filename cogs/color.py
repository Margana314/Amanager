import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="color", description="Afficher la couleur d'un code héxadécimal", options=[
                create_option(
                name="hexa",
                description="code héxadécimal",
                option_type=3,
                required=True
                )])
    async def _color(self, ctx, hexa: str):
        hexa = hexa.replace("#",'').upper()
        embed = discord.Embed(title=f"Couleur recherchée : **#{hexa}**")
        embed.set_image(url=f"https://www.colorhexa.com/{hexa}.png")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("color")