import discord, sqlite3, asyncio
from discord.ext import commands
from discord_slash import cog_ext, ButtonStyle
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_components import *

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(guild_ids=[736689848626446396], name="card", description="Afficher ta carte", options=[
                create_option(
                name="membre",
                description="Membre de discord",
                option_type=6,
                required=False
                )])
    async def _card(self, ctx, membre: discord.Member = None):
        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()
        if membre == None:
            membre = ctx.author
        if membre.bot == True:
            await ctx.send(f"{ctx.author.mention} Les bots n'ont pas de carte... :wink:")
        if membre.bot == False:
            member_id = (f"{membre.id}",)
            cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
            member_values = cursor.fetchone()
            if member_values == None:
                if membre == ctx.author:
                    await ctx.send("Tu ne peux pas afficher ta carte car tu n'as pas commencé l'aventure ISO land ! (Pour débuter, fait : **/start**)")
                else:
                    await ctx.send("Tu ne peux pas afficher la carte de cette personne car elle ne s'est pas inscrite à l'aventure ISO land...")
            else:
                about_para = member_values[1]
                embed = discord.Embed(title=f"Carte de {membre.name}", description=membre.mention)
                embed.add_field(name="À propos", value=about_para, inline=False)
                if membre != ctx.author:
                    await ctx.send(embed=embed)
                else:
                    buttons = [
                        create_button(
                        style = ButtonStyle.blue,
                        label = "Éditer À propos",
                        custom_id = "edit_apropos"
                        )
                    ]

                    action_row = create_actionrow(*buttons)
                    choice_made = await ctx.send(embed=embed, components=[action_row])

                    def check(m):
                        return m.author_id == ctx.author_id and m.origin_message.id == choice_made.id
                    def check2(msg):
                        return msg.author == ctx.author and msg.channel == ctx.channel

                    button_ctx = await wait_for_component(self.bot, components=action_row, check=check)
                    if button_ctx.custom_id == "edit_apropos":
                        await button_ctx.send(content="**Tu as 30 secondes pour envoyer le nouveau message de la section __à propos__.**", hidden=True)
                        try:
                            msg = await self.bot.wait_for("message", check=check2, timeout=30)
                        except asyncio.TimeoutError:
                            await button_ctx.send(content=f"{ctx.author.mention}, Le temps est écoulé. Réentre la commande pour éditer la section **à propos**.", hidden=True)

                        if len(list(msg.content)) >= 1024:
                            await button_ctx.send(content=f"{ctx.author.mention}, le message envoyé est trop long pour votre section **à propos**, la limite étant de 1024 caractères.", hidden=True)
                        else:
                            updated_user = (f"{msg.content}", f"{ctx.author.id}",)
                            cursor.execute('UPDATE tt_iso_card SET about = ? WHERE user_id = ?', updated_user)
                            connection.commit()

                            await msg.delete()
                            await button_ctx.send(content=f"{ctx.author.mention}, édition confirmée de la section **à propos** :\n\n> {msg.content}", hidden=True)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("card")