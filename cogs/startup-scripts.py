import discord, asyncio, random, json, humanize, sqlite3
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from discord_slash import cog_ext, ButtonStyle
from discord_slash.utils.manage_components import *

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        def load_json():
            global json_object_nm
            a_file = open("no-move.json", "r")
            json_object_nm = json.load(a_file)
            a_file.close()

        def reset_xp_cooldown(self):
            connection = sqlite3.connect("levels.db")
            cursor = connection.cursor()
            for guild in self.bot.guilds:
                cursor.execute(f'SELECT * FROM _{guild.id}')
                test = cursor.fetchall()
                for user in test:
                    if user[4] == 'yes':
                        updated_user = ('no', user[0],)
                        cursor.execute(f'UPDATE _{guild.id} SET cooldown = ? WHERE user_id = ?', updated_user)
                        connection.commit()
            connection.close()

        global uptime_start
        uptime_start = datetime.now()
        load_json()
        reset_xp_cooldown(self)
        await self.bot.change_presence(activity=discord.Game(name="redémarrage..."))
        await asyncio.sleep(3)
        self.status.start()

    @cog_ext.cog_slash(name="info", description="Afficher la latence et l'uptime du bot !")
    async def _ping(self, ctx):
        def get_servers_and_members(bot):
            guilds = bot.get_guild
            guilds_members_number = [0, 0]
            for guild in bot.guilds:
                guilds_members_number[0] += 1
                for member in guild.members:
                    guilds_members_number[1] += 1
            return guilds_members_number
        
        def getLastVersion():
            versions = []
            for version in json_object_nm['changelogs']:
                versions.append(version)
            return versions[-1]

        bot_latency = round(self.bot.latency * 1000)
        uptime_now = datetime.now()
        t1 = timedelta(days=uptime_start.day, hours=uptime_start.hour, minutes=uptime_start.minute, seconds=uptime_start.second)
        t2 = timedelta(days=uptime_now.day, hours=uptime_now.hour, minutes=uptime_now.minute, seconds=uptime_now.second)
        _t = humanize.i18n.activate("fr_FR")
        uptime = str(humanize.naturaltime(t2 - t1)).replace("il y a", "depuis")
        guilds_members_number = get_servers_and_members(self.bot)
        embed = discord.Embed(colour = discord.Colour.purple(), title="Amanager")
        embed.add_field(name="Créateur", value="Margana#7569", inline=True)
        embed.add_field(name="Language/librairie", value="Python/discord.py", inline=True)
        embed.add_field(name="Version", value=getLastVersion(), inline=True)
        embed.add_field(name="Serveurs", value=guilds_members_number[0], inline=True)
        embed.add_field(name="Membres", value=guilds_members_number[1], inline=True)
        embed.set_footer(text=f"🏓 Ping {bot_latency}ms | 🕓 Uptime {uptime}")

        buttons = [
            create_button(
                style = ButtonStyle.URL,
                label = "Inviter le bot",
                url = "https://iso-land.org/amanager/invite"
            ),
            create_button(
                style = ButtonStyle.URL,
                label = "GitHub",
                url = "https://github.com/Ana-gram/Amanager"
            )
        ]

        action_row = create_actionrow(*buttons)
        choice_made = await ctx.send(embed=embed, components=[action_row])

    @tasks.loop(seconds=600.0)
    async def status(self):
        rdnb = random.randint(1,2)
        if rdnb == 1:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(json_object_nm['status_messages']['watching'])))
        else:
            await self.bot.change_presence(activity=discord.Game(name=random.choice(json_object_nm['status_messages']['gaming'])))

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("startup-scripts")