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
                     background: Option(str, 'Please write a background for your character.'),
                     character_class: Option(
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
                         ]),
                     character_race: Option(
                             str,
                             description='Choose a race for your character.',
                             choices=[
                                 OptionChoice(name='Dragonborn', value='dragonborn'),
                                 OptionChoice(name='Dwarf', value='dwarf'),
                                 OptionChoice(name='Elf', value='elf'),
                                 OptionChoice(name='Half-Elf', value='half-elf'),
                                 OptionChoice(name='Halfling', value='halfling'),
                                 OptionChoice(name='Half-Orc', value='half-orc'),
                                 OptionChoice(name='Human', value='human'),
                                 OptionChoice(name='Tiefling', value='tiefling'),
                             ])):
        # init mongodb
        client = pymongo.MongoClient(os.environ.get('MONGOURI'))
        db = client['Fumiko']
        dnd_chars = db['dnd_chars']

        dnd_char = {
            "_id": ctx.author.id,
            "player_name": f"{ctx.author.name}#{ctx.author.discriminator}",
            "Name": name,
            "Background": background,
            "Group": character_class,
            "Race": character_race,
            "Level": 1,
            "XP": 0,
            "HP": 9,
            "Strength": 15,
            "Dexterity": 14,
            "Constitution": 13,
            "Intelligence": 12,
            "Wisdom": 10,
            "Charisma": 8,
        }

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
            color=ctx.author.color,
            fields=[
                discord.EmbedField(name="Name", value=dnd_char["Name"], inline=True),
                discord.EmbedField(name="Group", value=dnd_char["Group"], inline=True),
                discord.EmbedField(name="Race", value=dnd_char["Race"], inline=True),
                discord.EmbedField(name="Background", value=dnd_char["Background"], inline=False),
                discord.EmbedField(name="Level", value=dnd_char["Level"], inline=True),
                discord.EmbedField(name="XP", value=dnd_char["XP"], inline=True),
                discord.EmbedField(name="HP", value=dnd_char["HP"], inline=True),
                discord.EmbedField(name="Strength", value=dnd_char["Strength"], inline=True),
                discord.EmbedField(name="Dexterity", value=dnd_char["Dexterity"], inline=True),
                discord.EmbedField(name="Constitution", value=dnd_char["Constitution"], inline=True),
                discord.EmbedField(name="Intelligence", value=dnd_char["Intelligence"], inline=True),
                discord.EmbedField(name="Wisdom", value=dnd_char["Wisdom"], inline=True),
                discord.EmbedField(name="Charisma", value=dnd_char["Charisma"], inline=True),
            ],
            timestamp=discord.utils.utcnow())
        emb.set_footer(text="Bot by: Kamachi#2491")

        await ctx.respond(embed=emb)


def setup(bot):
    bot.add_cog(Dnd(bot))
