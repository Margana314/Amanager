import discord, random, asyncio
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="roll", description="Lancer un dé.", options=[
                create_option(
                name="nombre_de_faces",
                description="nombre de face du dé à lancer.",
                option_type=4,
                required=False,
                choices=[
                create_choice(
                name="4",
                value="4"
                ),
                create_choice(
                name="6",
                value="6"
                ),
                create_choice(
                name="8",
                value="8"
                ),
                create_choice(
                name="10",
                value="10"
                ),
                create_choice(
                name="12",
                value="12"
                ),
                create_choice(
                name="20",
                value="20"
                )])])
    async def _roll(self, ctx, nombre_de_faces: int):
        bot_message = await ctx.send("J'ai lancé le dé.")
        await asyncio.sleep(1)
        if nombre_de_faces == None: nombre_de_faces = 6
        dice_face = random.randint(1, nombre_de_faces)
        await bot_message.edit(content=f"{ctx.author.mention}, c'est la face numéro **{dice_face}** !\nSur l'intervalle **1** à **{nombre_de_faces}**")

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("roll")