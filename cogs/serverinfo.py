import discord
from discord.ext import commands
from discord_slash import cog_ext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="serverinfo", description="Afficher les informations du serveur sur lequel tu es !")
    async def _serverinfo(self, ctx):
        online_users = int(sum(member.status==discord.Status.online and not member.bot for member in ctx.guild.members)) + int(sum(member.status==discord.Status.idle and not member.bot for member in ctx.guild.members)) + int(sum(member.status==discord.Status.do_not_disturb and not member.bot for member in ctx.guild.members))
        embed = discord.Embed(title=ctx.guild.name, color=0xf5900b)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text=f"ID : {ctx.guild.id}")
        embed.add_field(name="Région du serveur", value=ctx.guild.region, inline=True)
        embed.add_field(name="Propriétaire du serveur", value=ctx.guild.owner.name, inline=True)
        embed.add_field(name="Nombre d'utilisateurs", value=f"{sum(not member.bot for member in ctx.guild.members)} ({online_users} connectés, {sum(member.status==discord.Status.offline and not member.bot for member in ctx.guild.members)} hors lignes)", inline=True)
        embed.add_field(name="Nombre de bots", value=sum(member.bot for member in ctx.guild.members), inline=True)
        embed.add_field(name="Nombre de boosts", value=ctx.guild.premium_subscription_count, inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("serverinfo")