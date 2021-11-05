import discord, random
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="rps", description="Jouer au rock scroll scissors !", options=[
                create_option(
                name="joueur",
                description="Pierre, scroll ou scissors ?",
                option_type=3,
                required=True,
                choices=[
                    create_choice(
                    name="pierre",
                    value="rock"
                    ),
                    create_choice(
                    name="papier",
                    value="scroll"
                    ),
                    create_choice(
                    name="ciseaux",
                    value="scissors"
                    )])])
    async def _rps(self, ctx, joueur: str):
        bot_ = ["rock", "scroll", "scissors"]
        bot_ = random.choice(bot_)
        bot_emoji = f":{bot_}:"
        joueur_emoji = f":{joueur}:"

        if joueur == bot_: msg = ":crossed_swords: Égalité !"
        elif joueur == "rock" and bot_ == "scroll": msg = "Tu as perdu..."
        elif joueur == "scroll" and bot_ == "scissors": msg = "Tu as perdu..."
        elif joueur == "scissors" and bot_ == "rock": msg = "Tu as perdu..."
        elif joueur == "rock" and bot_ == "scissors": msg = "Tu as gagné !"
        elif joueur == "scroll" and bot_ == "rock": msg = "Tu as gagné !"
        elif joueur == "scissors" and bot_ == "scroll": msg = "Tu as gagné !"

        bot_ = bot_.replace("rock", "pierre").replace("scroll", "papier").replace("scissors", "ciseaux")
        joueur = joueur.replace("rock", "pierre").replace("scroll", "papier").replace("scissors", "ciseaux")

        embed = discord.Embed(title="Pierre Papier Ciseaux")
        embed.add_field(name="** **", value=f"{joueur_emoji} {ctx.author.mention} : {joueur}\n{bot_emoji} <@760171813866700850> : {bot_}", inline=False)
        embed.add_field(name="** **", value=msg, inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("rps")