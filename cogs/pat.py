import discord, TenGiphPy, json
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="pat", description="Vouloir faire un câlin à quelqu'un !", options=[
                create_option(
                name="membre",
                description="Membre de discord à câliner",
                option_type=6,
                required=False
                )])
    async def _pat(self, ctx, membre: discord.Member = None):
        await ctx.defer()
        a_file = open("no-move.json", "r")
        json_object_nm = json.load(a_file)
        a_file.close()
        tengiphpy_api_key = json_object_nm['token']['tengiphpy']
        embed = discord.Embed()
        rgif = TenGiphPy.Tenor(token=tengiphpy_api_key)
        dance_gif = rgif.random("pat anime")
        if membre == None:
            embed.add_field(name=f"{ctx.author.name} a été câliné(e) !", value=f'{ctx.author.mention}', inline=False)
            embed.set_image(url=dance_gif)
            await ctx.send(embed=embed)
        else:
            if str(membre) == str(ctx.author):
                embed.add_field(name=f"{ctx.author.name} s'est câliné(e) soi-même... !?", value=f"{ctx.author.mention}", inline=False)
                embed.set_image(url=dance_gif)
                await ctx.send(embed=embed)
            else:
                embed.add_field(name=f"{ctx.author.name} a câliné {membre.name} !", value=f'{ctx.author.mention} {membre.mention}', inline=False)
                embed.set_image(url=dance_gif)
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("pat")