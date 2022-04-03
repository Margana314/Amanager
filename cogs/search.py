# Recherche DuckDuckGo avec la lib duckduckgo_search
import discord, requests
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_components import *
from duckduckgo_search import ddg # Sorry

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="search", description="Recherche DuckDuckGo", options = [
    	create_option(
    		name="motcle"
    		description="Mots-clés"
    		option_type=3,
    		required=True
    	)
    ])
    async def _search(self, ctx, motcle: str):
        await ctx.defer()
        
        search = ddg(motcle, region='fr-fr', safesearch='Moderate', time='y', max_results=10) # max_results ne prend pas effet, bug?
        
        i = 0 # index
        max_results = 10 # nombre de résultats a fetch max
        
        # À savoir que le nombre de fields dans un embed max = 25 donc max_results <= 25
        
        # Setup l'embed
        embed = discord.Embed(title="Recherche DuckDuckGo",description=f"Résultats pour **{motcle}**")
        
        for item in search:
        	for key in item:
        		if i <= max_results+1: # Je prends tous les fixs pour optimiser ça là
        			embed.add_field(name=search[i][title], value=f"**[Accéder]({search[i][href]})** - {search[i][body]")
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("search")
