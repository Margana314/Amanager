import discord, asyncio, sqlite3
from discord.ext import commands
from discord_slash import cog_ext
from discord.ext.commands import has_permissions
from discord_slash.utils.manage_commands import create_option, create_choice

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="ssettings", description="Modifier les paramètres du bot liés à ce serveur ! ⚠️ Nécessite la permission administrateur !", options=[
        create_option(
            name="menu",
            description="Menu",
            option_type=3,
            required=True,
            choices=[
                create_choice(
                name="Afficher les infos",
                value="1"
                ),
                create_choice(
                name="Éditer expériences et niveaux",
                value="2"
                )])])

    async def _ssettings(self, ctx, menu: str):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        if ctx.author.guild_permissions.administrator or ctx.author.id == 307092817942020096:
            settings_edit = await ctx.send("...")
            if menu == "1":
                connection = sqlite3.connect("levels.db")
                cursor = connection.cursor()
                server_id = (f"{ctx.guild.id}",)
                cursor.execute('SELECT * FROM levels WHERE server_id = ?', server_id)
                server_values = cursor.fetchone()
                up_message = str(server_values[1]).replace("$$AUTHOR_MENTION$$", f"{ctx.author.mention}").replace("$$AUTHOR_NAME$$", ctx.author.name).replace("$$N_LEVEL$$", "3").replace("$$A_LEVEL$$", "2")
                is_activated_xp = server_values[2]
                if is_activated_xp == "yes": is_activated_xp = ":white_check_mark:"
                elif is_activated_xp == "no": is_activated_xp = ":x:"
                is_activated_up_message = server_values[3]
                if is_activated_up_message == "no": is_activated_up_message = ":x:"
                elif is_activated_up_message == "yes": is_activated_up_message = ":white_check_mark:"
                up_message_channel = server_values[4]
                if up_message_channel == "$$AUTO$$": up_message_channel = "Salon où le message est envoyé."
                embed = discord.Embed(title="Paramètres du serveur", description=ctx.author.mention)
                embed.add_field(name="Expérience & Niveaux", value=f"Activé ? {is_activated_xp}\nUP message activé ? {is_activated_up_message}\nUP message (exemple) : {up_message}\nSalon de l'up message : {up_message_channel}", inline=False)
                connection.close()
                await settings_edit.edit(embed=embed, content=None)

            elif menu == "2":
                connection = sqlite3.connect("levels.db")
                cursor = connection.cursor()
                server_id = (f"{ctx.guild.id}",)
                cursor.execute('SELECT * FROM levels WHERE server_id = ?', server_id)
                server_values = cursor.fetchone()

                embed = discord.Embed(title=f"Bienvenue dans le menu d'édition du système d'XP !", description=ctx.author.mention)
                embed.add_field(name=f":one: Activer/Désactiver le système d'XP.", value="** **", inline=False)
                embed.add_field(name=f":two: Activer/Désactiver l'up message.", value="** **", inline=False)
                embed.add_field(name=":three: Editer l'up message.", value="** **", inline=False)
                embed.add_field(name=":four: Editer le salon où l'up message sera envoyé.", value="** **", inline=False)
                embed.add_field(name=":x: Sortir du menu d'édition.", value="** **", inline=False)
                embed.set_footer(text="up message = message de passage au niveau supérieur.")
                await settings_edit.edit(embed=embed, content="> Tu as 15 secondes pour répondre.")

                try:
                    msg = await self.bot.wait_for("message", check=check, timeout=15)
                except asyncio.TimeoutError:
                    await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
                await msg.delete()

                choice = msg.content
                if choice.lower() == "x":
                    await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Edition annulée !")

                elif choice == "1":
                    is_activated = server_values[2]
                    if is_activated == "yes":
                        is_activated = "no"
                        actif = "désactivé"
                    else:
                        is_activated = "yes"
                        actif = "activé"
                    updated_server = (f"{is_activated}", f"{ctx.guild.id}",)
                    cursor.execute('UPDATE levels SET is_activated = ? WHERE server_id = ?', updated_server)
                    connection.commit()
                    await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Le système d'XP a bien été {actif} !")

                elif choice == "2":
                    is_activated_up_message = server_values[3]
                    if is_activated_up_message == "yes":
                        is_activated_up_message = "no"
                        actif = "désactivé"
                    else:
                        is_activated_up_message = "yes"
                        actif = "activé"
                    updated_server = (f"{is_activated_up_message}", f"{ctx.guild.id}",)
                    cursor.execute('UPDATE levels SET is_activated_up_message = ? WHERE server_id = ?', updated_server)
                    connection.commit()
                    await settings_edit.edit(embed=None, content=f"{ctx.author.mention} l'up message a bien été {actif} !")

                elif choice == "3":
                    embed = discord.Embed(title="Menu de modification de l'up message.", description=ctx.author.mention)
                    embed.add_field(name="Entre ci-dessous l'up message qui sera envoyé.", value="Entre :x: pour quitter l'édition.", inline=False)
                    embed.add_field(name="** **", value="```$$AUTHOR_MENTION$$ = mention du membre\n$$AUTHOR_NAME$$ = nom du membre\n$$A_LEVEL$$ = ancien niveau\n$$N_LEVEL$$ = nouveau niveau```", inline=False)
                    embed.add_field(name="Ancienne valeur", value=server_values[1], inline=False)
                    await settings_edit.edit(embed=embed, content="> Tu as 1 minute pour répondre.")

                    try:
                        msg = await self.bot.wait_for("message", check=check, timeout=60)
                    except asyncio.TimeoutError:
                        await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
                    await msg.delete()

                    new_up_message = msg.content

                    if new_up_message == "x" or new_up_message == ":x:":
                        await settings_edit.edit(embed=None, content="Edition annulée !")
                    else:
                        updated_server = (f"{new_up_message}", f"{ctx.guild.id}",)
                        cursor.execute('UPDATE levels SET up_message = ? WHERE server_id = ?', updated_server)
                        connection.commit()
                        embed = discord.Embed(description=new_up_message)
                        await settings_edit.edit(embed=embed, content="> L'up message a été mise à jour !")

                elif choice == "4":
                    channel_to_send = server_values[4]
                    if channel_to_send == "$$AUTO$$": channel_to_send = "Salon où le message est envoyé."
                    embed = discord.Embed(title="Menu de modification du salon de l'up message", description=ctx.author.mention)
                    embed.add_field(name="Entre ci-dessous le salon où l'up message sera envoyé.", value="Entre :x: pour quitter l'édition.", inline=False)
                    embed.add_field(name="** **", value="```$$AUTO$$ = salon où le membre parle.```", inline=False)
                    embed.add_field(name="Ancienne valeur", value=channel_to_send, inline=False)
                    await settings_edit.edit(embed=embed, content="> Tu as 1 minute pour répondre.")

                    try:
                        msg = await self.bot.wait_for("message", check=check, timeout=60)
                    except asyncio.TimeoutError:
                        await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
                    await msg.delete()

                    new_channel_up_message = msg.content

                    if new_channel_up_message == "x" or new_channel_up_message == ":x:":
                        await settings_edit.edit(embed=None, content="Edition annulée !")
                    else:
                        updated_server = (f"{new_channel_up_message}", f"{ctx.guild.id}",)
                        cursor.execute('UPDATE levels SET channel_to_send = ? WHERE server_id = ?', updated_server)
                        connection.commit()
                        embed = discord.Embed(description=new_channel_up_message)
                        await settings_edit.edit(embed=embed, content="> Le salon de l'up message a été mis à jour !")
        else:
            await ctx.send(f"{ctx.author.mention} Tu n'as pas la permission de faire cela sur ce serveur :angry:")

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("ssettings")