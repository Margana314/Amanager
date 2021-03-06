import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="glass", description="Afficher une photo de profil avec un filtre de verre", options=[
                create_option(
                name="membre",
                description="membre discord (discord member)",
                option_type=6,
                required=False
                )])
    async def _glass(self, ctx, membre: discord.Member = None):
        if membre == None:
            membre = ctx.author
        embed = discord.Embed(title=f"{membre.name} est vitreux(se)", description=membre.mention)
        member_avatar_url = str(membre.avatar_url).replace('webp','png').replace('?size=1024','?size=4096')
        embed.set_image(url=f'https://some-random-api.ml/canvas/glass?avatar={member_avatar_url}')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("glass")