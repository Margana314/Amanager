import discord, random, asyncio
from discord.ext import commands
from discord_slash import cog_ext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="coin", description="Lancer une pièce à 2 faces.")
    async def _coin(self, ctx):
        bot_message = await ctx.send("J'ai lancé la pièce.")
        await asyncio.sleep(1)
        if random.randint(1, 1000) == 1:
            await bot_message.edit(content=f"{ctx.author.mention}, vous allez pas me croire... mais c'est tombé sur la tranche !")
        else:
            if random.randint(1, 2) == 1:
                await bot_message.edit(content=f"{ctx.author.mention}, c'est face !")
            else:
                await bot_message.edit(content=f"{ctx.author.mention}, c'est pile !")

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("coin")