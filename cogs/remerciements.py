import discord, json
from discord.ext import commands
from discord_slash import cog_ext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="remerciements", description="Afficher les remerciements liés à ce bot !")
    async def _remerciements(self, ctx):
        a_file = open("no-move.json", "r")
        json_object_nm = json.load(a_file)
        a_file.close()
        msg = json_object_nm['remerciements']
        await ctx.send(msg)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("remerciements")