import discord, requests
from discord.ext import commands
from discord_slash import cog_ext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="meme", description="Meme aléatoire de reddit")
    async def _meme(self, ctx):
        await ctx.defer()
        meme_response = requests.get("https://meme-api.herokuapp.com/gimme").json()
        embed = discord.Embed(title=f"Meme", description=meme_response["postLink"])
        embed.add_field(name=f"Meme de {meme_response['author']}", value=f"Subreddit : **r/{meme_response['subreddit']}** | <:reddit_upvote:791346828012552202> {meme_response['ups']}", inline=False)
        embed.set_image(url=meme_response['url'])
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("meme")