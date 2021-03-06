import discord, random, TenGiphPy, json
from discord.ext import commands
from discord_slash import cog_ext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="karen", description="KAREN ?")
    async def _karen(self, ctx):
        random_karen = random.randint(1, 3)
        if random_karen == 1: # joke
            jokes_karen = ['I want to speak to the manager !', 'I want to speak with the manager !', 'Take the kids out.', 'I have a complaint, i want to speak to the manager', f'{ctx.author.mention} entre en mode Karen !']
            await ctx.send(random.choice(jokes_karen))
        elif random_karen == 2: # meme (image)
            memes_karen = ["https://urlz.fr/hMYG", "https://urlz.fr/hMYH", "https://urlz.fr/hMYI",
            "https://urlz.fr/hMYJ", "https://urlz.fr/hMYK", "https://urlz.fr/hMYL",
            "https://urlz.fr/hMYM", "https://urlz.fr/hMYN", "https://urlz.fr/hMYO", "https://urlz.fr/hMYC"]
            await ctx.send(random.choice(memes_karen))
        elif random_karen == 3: # gif
            a_file = open("no-move.json", "r")
            json_object_nm = json.load(a_file)
            a_file.close()
            tengiphpy_api_key = json_object_nm['token']['tengiphpy']
            rgif = TenGiphPy.Tenor(token=tengiphpy_api_key)
            karen_gif = rgif.random("karen")
            await ctx.send(karen_gif)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("karen")