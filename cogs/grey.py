import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="grey", description="Afficher une photo de profil avec un filtre gris", options=[
                create_option(
                name="membre",
                description="membre discord",
                option_type=6,
                required=False
                )])
    async def _grey(self, ctx, membre: discord.Member = None):
        if membre == None:
            membre = ctx.author
        embed = discord.Embed(title=f"{membre.name} est gris(e)", description=membre.mention)
        member_avatar_url = str(membre.avatar_url).replace('webp','png').replace('?size=1024','?size=4096')
        embed.set_image(url=f'https://some-random-api.ml/canvas/greyscale?avatar={member_avatar_url}')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("grey")