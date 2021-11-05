import discord, os, json
from discord.ext import commands
from discord_slash import SlashCommand

def get_token():
    a_file = open("no-move.json", "r")
    json_object_nm = json.load(a_file)
    a_file.close()
    token = str(json_object_nm['token']['bot'])
    return token

bot = commands.Bot(command_prefix="prefix", intents=discord.Intents.all())
slash = SlashCommand(bot, override_type = True, sync_commands=True, sync_on_cog_reload=True)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(get_token())