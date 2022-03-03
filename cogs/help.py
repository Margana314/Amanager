import discord
from discord.ext import commands
from discord_slash import cog_ext, ButtonStyle
from discord_slash.utils.manage_components import *

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="help", description="Afficher le menu d'aide !")
    async def _help(self, ctx):

        embed = discord.Embed(title=":information_source: Aide des commandes invoquée.", colour = discord.Colour.purple())

        buttons = [
            create_button(
            style = ButtonStyle.URL,
            label = "Liste des commandes",
            url = "https://github.com/Margana314/Amanager/wiki"
            )
        ]

        action_row = create_actionrow(*buttons)
        choice_made = await ctx.send(embed=embed, components=[action_row])

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("help")