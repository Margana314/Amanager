import discord, json
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="changelog", description="Afficher la liste des versions du bot !", options=[
                create_option(
                name="version",
                description="Versions du bot visibles avec /changelog",
                option_type=3,
                required=False
                )])
    async def _changelog(self, ctx, version: str = None):
        a_file = open("no-move.json", "r")
        json_object_nm = json.load(a_file)
        a_file.close()
        changelog_versions = json_object_nm['changelogs']

        espace = "\n"
        if version == None:
            changelog_versions = espace.join(list(changelog_versions))
            embed = discord.Embed(title="Liste des versions de changelogs")
            embed.add_field(name="** **", value=changelog_versions, inline=True)
            await ctx.send(embed=embed)
        else:
            if version.lower() not in changelog_versions:
                await ctx.send(f"La version que tu as entré n'est pas valide. Pour voir la liste des versions : **/changelog**.")
            else:
                cg = changelog_versions[f"{version.lower()}"]
                embed = discord.Embed(title=f"Changelog • {version.lower()}", description=cg['date'], color=0x666666)
                await ctx.send(embed=embed, content=cg['description'])

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("changelog")