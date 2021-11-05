import discord, json
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="length", description="Compteur de caractères", options=[
                create_option(
                name="message",
                description="Message",
                option_type=3,
                required=True
                )])
    async def _length(self, ctx, message: str):
        embed = discord.Embed(title=f"Compteur de caractères")
        embed.add_field(name="Nombre de caractères", value=len(list(message)), inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("length")