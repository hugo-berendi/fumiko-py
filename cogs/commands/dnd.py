import os
import discord
import pymongo
import random
from discord.ext import commands
from discord.commands import OptionChoice, Option
from dotenv import load_dotenv
from modules import dnd_modules as dndm

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
                             OptionChoice(name='Monk', value='monk'),
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

        def init_dnd_char_group(group):
            if group == 'barbarian':
                hp = 13
                return hp
            elif group == 'bard':
                hp = 9
                return hp
            elif group == 'cleric':
                hp = 9
                return hp
            elif group == 'druid':
                hp = 9
                return hp
            elif group == 'fighter':
                hp = 11
                return hp
            elif group == 'monk':
                hp = 9
                return hp
            elif group == 'paladin':
                hp = 11
                return hp
            elif group == 'ranger':
                hp = 11
                return hp
            elif group == 'rogue':
                hp = 9
                return hp
            elif group == 'sorcerer':
                hp = 7
                return hp
            elif group == 'warlock':
                hp = 9
                return hp
            elif group == 'wizard':
                hp = 7
                return hp

        def init_dnd_char_race(race):
            if race == 'dragonborn':
                stats = {
                    "Strength": 17,
                    "Dexterity": 14,
                    "Constitution": 13,
                    "Intelligence": 12,
                    "Wisdom": 10,
                    "Charisma": 9,
                }
                return stats
            elif race == 'dwarf':
                stats = {
                    "Strength": 15,
                    "Dexterity": 14,
                    "Constitution": 15,
                    "Intelligence": 12,
                    "Wisdom": 10,
                    "Charisma": 8,
                }
                return stats
            elif race == 'elf':
                stats = {
                    "Strength": 15,
                    "Dexterity": 16,
                    "Constitution": 13,
                    "Intelligence": 12,
                    "Wisdom": 10,
                    "Charisma": 8,
                }
                return stats
            elif race == 'gnome':
                stats = {
                    "Strength": 15,
                    "Dexterity": 14,
                    "Constitution": 13,
                    "Intelligence": 14,
                    "Wisdom": 10,
                    "Charisma": 8,
                }
                return stats
            elif race == 'half-elf':
                stats = {
                    "Strength": 15,
                    "Dexterity": 15,
                    "Constitution": 14,
                    "Intelligence": 12,
                    "Wisdom": 10,
                    "Charisma": 10,
                }
                return stats
            elif race == 'halfling':
                stats = {
                    "Strength": 15,
                    "Dexterity": 16,
                    "Constitution": 13,
                    "Intelligence": 12,
                    "Wisdom": 10,
                    "Charisma": 8,
                }
                return stats
            elif race == 'half-orc':
                stats = {
                    "Strength": 17,
                    "Dexterity": 14,
                    "Constitution": 14,
                    "Intelligence": 12,
                    "Wisdom": 10,
                    "Charisma": 8,
                }
                return stats
            elif race == 'human':
                stats = {
                    "Strength": 16,
                    "Dexterity": 15,
                    "Constitution": 14,
                    "Intelligence": 13,
                    "Wisdom": 11,
                    "Charisma": 9,
                }
                return stats
            elif race == 'tiefling':
                stats = {
                    "Strength": 15,
                    "Dexterity": 14,
                    "Constitution": 13,
                    "Intelligence": 13,
                    "Wisdom": 10,
                    "Charisma": 10,
                }
                return stats

        p = dndm.Player(player_id=ctx.author.id,
                        name,
                        background,
                        group=character_class,
                        race=character_race,
                        hp=init_dnd_char_group(character_class),
                        lvl=1,
                        ep=0,
                        stats=init_dnd_char_race(character_race))

        # cmd actions
        dnd_chars.find_one_and_update(
            {
                "_id": ctx.author.id
            },
            {
                "$set": p.export()
            },
            upsert=True
        )

        # create embed named emb
        emb = discord.Embed(
            title=f"{ctx.author.name}'s character sheet",
            description="",
            color=ctx.author.color,
            fields=[
                discord.EmbedField(name="Name", value=p.export()["name"], inline=True),
                discord.EmbedField(name="Class", value=p.export()["group"], inline=True),
                discord.EmbedField(name="Race", value=p.export()["race"], inline=True),
                discord.EmbedField(name="Background", value=p.export()["background"], inline=False),
                discord.EmbedField(name="Level", value=p.export()["lvl"], inline=True),
                discord.EmbedField(name='Stats',
                                   value=f'HP: {p.export()["hp"]}\nStrength: {p.export()["stats"]["strength"]}\nDexterity: {p.export()["stats"]["dexterity"]}\nConstitution: {p.export()["stats"]["constitution"]}\nIntelligence: {p.export()["stats"]["intelligence"]}\nWisdom: {p.export()["stats"]["wisdom"]}\nCharisma: {p.export()["stats"]["charisma"]}',
                                   inline=True)
            ],
            timestamp=discord.utils.utcnow())
        emb.set_footer(text="Bot by: Kamachi#2491")

        await ctx.respond(embed=emb)


def setup(bot):
    bot.add_cog(Dnd(bot))
