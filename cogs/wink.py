import discord, TenGiphPy, json
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="wink", description="Faire un clin d'œil à quelqu'un avec un GIF d'anime !", options=[
                create_option(
                name="membre",
                description="Membre de discord à qui faire un clin d'œil",
                option_type=6,
                required=False
                )])
    async def _wink(self, ctx, membre: discord.Member = None):
        await ctx.defer()
        a_file = open("no-move.json", "r")
        json_object_nm = json.load(a_file)
        a_file.close()
        tengiphpy_api_key = json_object_nm['token']['tengiphpy']
        embed = discord.Embed()
        rgif = TenGiphPy.Tenor(token=tengiphpy_api_key)
        dance_gif = rgif.random("wink anime")
        if membre == None:
            embed.add_field(name=f"{ctx.author.name} a fait un clin d'œil !", value=f'{ctx.author.mention}', inline=False)
            embed.set_image(url=dance_gif)
            await ctx.send(embed=embed)
        else:
            if str(membre) == str(ctx.author):
                embed.add_field(name=f"{ctx.author.name} s'est fait un clin d'œil... !?", value=f"{ctx.author.mention}", inline=False)
                embed.set_image(url=dance_gif)
                await ctx.send(embed=embed)
            else:
                embed.add_field(name=f"{ctx.author.name} a fait un clin d'œil à {membre.name} !", value=f'{ctx.author.mention} {membre.mention}', inline=False)
                embed.set_image(url=dance_gif)
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("wink")