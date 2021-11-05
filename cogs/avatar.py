import discord
from discord.ext import commands
from discord_slash import cog_ext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="avatar", description="Afficher une photo de profil") 
    async def _avatar(self, ctx, membre: discord.Member = None):
        if membre == None:
            membre = ctx.author
        embed = discord.Embed(colour = discord.Colour.purple(), title=f"Avatar de {membre.name}", description=membre.mention)
        embed.set_image(url=membre.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("avatar")