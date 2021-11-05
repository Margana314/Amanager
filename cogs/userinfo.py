import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="userinfo", description="Afficher les informations à propos de ton profil, ou d'un utilisateur !...", options=[
                create_option(
                name="membre",
                description="Membre de discord",
                option_type=6,
                required=False
                )])
    async def _userinfo(self, ctx, membre: discord.Member = None):
        if not membre:
            membre = ctx.author

        roles_list, espace = [], " "
        for role in membre.roles:
            if role.name != "@everyone":
                roles_list.append(str(role.mention))
        roles_list = roles_list[::-1]
        print(roles_list)
        embed = discord.Embed(title=str(membre.name) + "#" + str(membre.discriminator), description=membre.mention, color=0xf5900b)
        embed.set_thumbnail(url=str(membre.avatar_url))
        embed.set_footer(text=f"ID : {membre.id}")
        embed.add_field(name="A rejoint le serveur", value=membre.joined_at.strftime("%d/%m/%Y • %H:%M:%S"), inline=True)
        embed.add_field(name="Inscription sur Discord", value=membre.created_at.strftime("%d/%m/%Y • %H:%M:%S"), inline=True)
        if roles_list != None:
            embed.add_field(name="Liste des rôles", value=espace.join(roles_list), inline=True)
        if membre.premium_since != None:
            embed.add_field(name="Abonné à Nitro depuis", value=membre.premium_since.strftime("%d/%m/%Y • %H:%M:%S"), inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("userinfo")