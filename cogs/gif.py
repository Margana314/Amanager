import discord, TenGiphPy, json
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="gif", description="Afficher un gif", options=[
                create_option(
                name="requête",
                description="mots-clefs",
                option_type=3,
                required=True
                )])
    async def _gif(self, ctx, requête: str = None):
        a_file = open("no-move.json", "r")
        json_object_nm = json.load(a_file)
        a_file.close()
        tengiphpy_api_key = json_object_nm['token']['tengiphpy']
        rgif = TenGiphPy.Tenor(token=tengiphpy_api_key)
        msg = rgif.random(requête)
        embed = discord.Embed()
        embed.add_field(name=f"GIF de **{requête}** demandé par {ctx.author.name} !", value=ctx.author.mention, inline=False)
        embed.set_image(url=msg)
        embed.set_footer(text=f"Tenor")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("gif")