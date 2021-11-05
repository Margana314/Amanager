import discord, datetime, pytz
from discord.ext import commands
from datetime import datetime, date
from pytz import timezone

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == False:
###########################
# NEVER GONNA GIVE YOU UP #
###########################
            if message.content.lower() == "never gonna give you up":
                await message.channel.send(":notes: Never gonna let you down !")
###############
# KONAMI CODE #
###############
            konami_codes = ['up up down down left right left right b a', 'uuddlrlrba']
            if message.content.lower() in konami_codes:
                embed = discord.Embed(title=f"Le pouvoir de Konami a été RELACHÉ !!!", color=0xf8e604)
                embed.add_field(name='Le cheat code a bien été activé.', value="** **", inline=False)
                await message.author.send(embed=embed)
                await message.delete()
############
# BOT PING #
############
            bot_mentions = ['<@760171813866700850>', '<@!760171813866700850>']
            if message.content in bot_mentions:
                mention_time = int(datetime.now(pytz.timezone('Europe/Paris')).strftime("%H"))
                mention_date = date.today().strftime("%B %d, %Y")
                if 7 <= mention_time <= 12:
                    mention_time = "Salut ! :wave:"
                elif 13 <= mention_time <= 19:
                    mention_time = "Bon après-midi ! :sunglasses:"
                elif 20 <= mention_time <= 23:
                    mention_time = "Bonsoir ! :yawning_face:"
                elif 0 <= mention_time <= 6:
                    mention_time = "Bonne nuit ! :sleeping:"

                if "december" in mention_date.lower():
                    mention_time = "Oh! oh! oh! " + str(mention_time)
                elif "august" in mention_date.lower():
                    mention_time = "Bonnes vacances d'été ! " + str(mention_time)

                embed = discord.Embed(title=mention_time, description=f"Mon préfixe est **/** | **/help** pour plus d'infos !", color=0xf5900b)
                embed.add_field(name="** **", value="Tu rencontres des bugs, tu as besoin d'aide, tu veux contribuer ou juste discuter ? Tu peux rejoindre le [serveur support](https://iso-land.org/discord) du bot !", inline=False)
                await message.channel.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("triggers")