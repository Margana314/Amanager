import discord, asyncio, random, string
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="pwd", description="Générer un mot de passe aléatoire personnalisable, facilement et en toute sécurité !", options=[
                create_option(
                name="nombre_de_caractères",
                description="Le nombre de caractères que contiendra le mot de passe (minimum 8 et maximum 128)",
                option_type=4,
                required=True
                ),
                create_option(
                name="nombres_",
                description="Y inclure des nombres ? (répondre oui ou non)",
                option_type=3,
                required=True,
                choices=[
                create_choice(
                name="oui",
                value="oui"
                ),
                create_choice(
                name="non",
                value="non"
                )]
                ),
                create_option(
                name="caractères_spéciaux_",
                description="Y inclure des caractères spéciaux ? (répondre oui ou non)",
                option_type=3,
                required=True,
                choices=[
                create_choice(
                name="oui",
                value="oui"
                ),
                create_choice(
                name="non",
                value="non"
                )]
                )])
    async def _pwd(self, ctx, nombre_de_caractères: int, nombres_: str, caractères_spéciaux_: str):
        espace = " "
        def password_gen(pwd_nb_caracteres, is_numbers, is_caracters):
            pas_espace = ""
            pwd_list = []
            pwd_caracters = [',', ':', ';', '-', '+', '(', ')', '@', '*', '#', '€', '%', '&', '/', '_', '~', '`', '|', '°', '=', '{', '}', '[', ']', '<', '>']
            for i in range(pwd_nb_caracteres):
                random_number = random.randint(1,4)
                if random_number == 1:
                    pwd_list.append(random.choice(list(string.ascii_lowercase)))
                elif random_number == 2:
                    pwd_list.append(random.choice(list(string.ascii_uppercase)))
                elif random_number == 3:
                    if is_numbers.lower() == "oui":
                        pwd_list.append(str(random.randint(0,9)))
                    else:
                        random_number_2 = random.randint(1,2)
                        if random_number_2 == 1:
                            pwd_list.append(random.choice(list(string.ascii_lowercase)))
                        else:
                            pwd_list.append(random.choice(list(string.ascii_uppercase)))
                elif random_number == 4:
                    if is_caracters.lower() == "oui":
                        pwd_list.append(random.choice(pwd_caracters))
                    else:
                        random_number_2 = random.randint(1,2)
                        if random_number_2 == 1:
                            pwd_list.append(random.choice(list(string.ascii_lowercase)))
                        else:
                            pwd_list.append(random.choice(list(string.ascii_uppercase)))
            password = pas_espace.join(pwd_list)
            return password

        min_car, max_car = 8, 256
        if nombre_de_caractères > max_car or nombre_de_caractères < min_car:
            await ctx.send(f"{ctx.author.mention} Le nombre que tu as entré n'est pas valide... (Le minimum étant de {min_car} et le maximum de {max_car} !)")
        else:
            password = password_gen(nombre_de_caractères, nombres_, caractères_spéciaux_)
            pwd_end = await ctx.send(f"{ctx.author.mention} Ton mot de passe a été envoyé en MP !")
            await ctx.author.send(f"Vous aviez demandé un mot de passe :\n\n```{password}```")
            await asyncio.sleep(3)
            await pwd_end.delete()

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("pwd")