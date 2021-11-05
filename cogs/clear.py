import discord, asyncio
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord.ext.commands import has_permissions

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="clear", description="Supprimer un certain nombre de messages rapidement.", options=[
                create_option(
                name="nombre_de_messages",
                description="Nombre de messages à supprimer",
                option_type=4,
                required=True
                )])
    async def _clear(self, ctx, nombre_de_messages: int):
        if ctx.author.guild_permissions.ban_members:
            await ctx.defer()
            await ctx.channel.purge(limit=nombre_de_messages)
            msg = await ctx.send(":white_check_mark:")
            await asyncio.sleep(1)
            await msg.delete()
        else:
            await ctx.send(f"{ctx.author.mention} :no_entry: Tu n'as pas la permission de supprimer des messages.", delete_after=5)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("clear")