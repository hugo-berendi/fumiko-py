import os
import discord
import pymongo
import random
from discord.ext import commands
from discord.commands import OptionChoice, Option
from dotenv import load_dotenv

# load .env vars
load_dotenv()


class Dnd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    dnd = discord.SlashCommandGroup('dnd', 'Dungeons & Dragons related commands')

    @dnd.command(name="create", description="Create your dnd character")
    async def create(self,
                    ctx: discord.ApplicationContext,
                    name: Option(str, "Please input the name of your character."),
                    description: Option(str, 'Please describe your character.'),
                    group: Option(
                        str,
                        description='Choose the class of your character.',
                        choices=[
                            OptionChoice(name='Barbarian', value='barbarian'),
                            OptionChoice(name='Bard', value='bard'),
                            OptionChoice(name='Cleric', value='cleric'),
                            OptionChoice(name='Druid', value='druid'),
                            OptionChoice(name='Fighter', value='fighter'),
                            OptionChoice(name='Paladin', value='paladin'),
                            OptionChoice(name='Ranger', value='ranger'),
                            OptionChoice(name='Rogue', value='rogue'),
                            OptionChoice(name='Sorcerer', value='sorcerer'),
                            OptionChoice(name='Warlock', value='warlock'),
                            OptionChoice(name='Wizard', value='wizard')
                        ])):  # type: ignore
        # init mongodb
        client = pymongo.MongoClient(os.environ.get('MONGOURI'))
        db = client['Fumiko']
        dnd_chars = db['dnd_chars']

        population = ['S', 'A', 'B', 'C', 'D', 'E']
        weights = [0.005, 0.025, 0.07, 0.1, 0.3, 0.5]

        dnd_char = {
            "_id":         ctx.author.id,
            "owner":       f"{ctx.author.name}#{ctx.author.discriminator}",
            "name":        name,
            "description": description,
            "group":       group,
            "HP": random.choices(population=population, weights=weights),
            "STRENGTH": random.choices(population=population, weights=weights),
            "DEXTERITY": random.choices(population=population, weights=weights),
            "CONSTITUTION": random.choices(population=population, weights=weights),
            "INTELLIGENCE": random.choices(population=population, weights=weights),
            "WISDOM": random.choices(population=population, weights=weights),
            "CHARISMA": random.choices(population=population, weights=weights),
        }

        random.choices(population=population, weights=weights)

        # cmd actions
        dnd_chars.find_one_and_update(
                {
                    "_id": ctx.author.id
                },
                {
                    "$set": dnd_char
                },
                upsert=True
        )

        # create embed named emb
        emb = discord.Embed(
                title=f"Infos about {ctx.author.name}'s character",
                description="",
                color=ctx.author.color)

        # add fields to emb
        emb.add_field(name="Name", value=dnd_char["name"], inline=False)
        emb.add_field(name="Description", value=dnd_char["description"], inline=False)
        emb.add_field(name="Group", value=dnd_char["group"], inline=False)
        emb.add_field(name="HP", value=dnd_char["HP"], inline=True)
        emb.add_field(name="STRENGTH", value=dnd_char["STRENGTH"], inline=True)
        emb.add_field(name="DEXTERITY", value=dnd_char["DEXTERITY"], inline=True)
        emb.add_field(name="CONSTITUTION", value=dnd_char["CONSTITUTION"], inline=True)
        emb.add_field(name="INTELLIGENCE", value=dnd_char["INTELLIGENCE"], inline=True)
        emb.add_field(name="WISDOM", value=dnd_char["WISDOM"], inline=True)
        emb.add_field(name="CHARISMA", value=dnd_char["CHARISMA"], inline=True)

        # add footer to emb
        emb.set_footer(text="Bot by: Kamachi#2491")

        # add timestamp to emb
        emb.timestamp = discord.utils.utcnow()

        await ctx.respond(embed=emb)

def setup(bot):
    bot.add_cog(Dnd(bot))
