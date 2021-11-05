import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        APOD_channels = [611230647343644682] # apod (project garmana)
        if message and message.channel.id in APOD_channels:
            default_emojis = ["👌", "😍", "🤩"]
            async def react_apod(message):
                for emoji in default_emojis:
                    await message.add_reaction(emoji)
            await react_apod(message)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("automations")