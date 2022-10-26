from os import environ
import discord
import pymongo
import random
from discord.ext import commands
from discord.commands import OptionChoice, Option
from dotenv import load_dotenv

# load .env vars
load_dotenv()


class Player:
    def __init__(self,
                 id: int,
                 name: str,
                 age: int,
                 group: str,
                 attribute: str,
                 description: str,
                 skills: list,
                 stats: dict):
        self.id = id
        self.name = name
        self.age = age
        self.group = group
        self.attribute = attribute
        self.description = description
        self.skills = skills
        self.stats = stats

    def getDmg(self, dmg: int):
        self.stats.health = self.stats.health - dmg
        if self.hp <= 0:
            self.stats.health = 0
            return 'you are dead'
        else:
            hp = self.hp
            return hp

    def export(self):
        dnd_char = {
            '_id': self.id,
            'name': self.name,
            'age': self.age,
            'group': self.group,
            'attribute': self.attribute,
            'description': self.description,
            'skills': self.skills,
            'stats': self.stats
        }
        return dnd_char


class Game:
    def __init__(self, player: Player):
        self.player = player

    def play(self):
        enemies = ['zombie', 'spider']
        enemie_stats = {
            'zombie': {
                'dmg': 1,
                'hp': 2
            },
            'spider': {
                'dmg': 2,
                'hp': 1
            }
        }

        enemie = random.choice(enemies)
        dmg = enemie_stats[str(enemie)]['dmg']
        return self.player.getDmg(int(dmg))


class PlayerInfoEmbed:
    def __init__(self, player: Player):
        self.p = player

    def send(self):
        def skills(player: Player):
            skills = ""
            for skill in player.export()['skills']:
                if skill['lvl'] == None:
                    skills += f"{skill['name']}\n"
                else:
                    skills += f"{skill['name']} Lv. {skill['lvl']}\n"
            return skills

        emb = discord.Embed(
            title="[Character Information]",
            description="",
            color=ctx.author.color,
            fields=[
                discord.EmbedField(name='Name', value=p.export()['name'], inline=True),
                discord.EmbedField(name='Age', value=f"{p.export()['age']} years old.", inline=True),
                discord.EmbedField(name='Group', value=p.export()['group'], inline=True),
                discord.EmbedField(name='Description', value=p.export()['description'], inline=False),
                discord.EmbedField(name='Attribute', value=f"{p.export()['attribute']}", inline=False),
                discord.EmbedField(name='Skills', value=f"{skills(self.p)}", inline=False),
                discord.EmbedField(name='Overall Stats',
                                   value=f"""
                                   Health:         Lv. {p.export()["stats"]["health"]}
                                   Stamina:        Lv. {p.export()["stats"]["stamina"]}
                                   Strength:       Lv. {p.export()["stats"]["strength"]}
                                   Agility:        Lv. {p.export()["stats"]["agility"]}
                                   Magic Power:    Lv. {p.export()["stats"]["magic_power"]}
                                   """,
                                   inline=False)
            ],
            timestamp=discord.utils.utcnow())
        emb.set_footer(text="Bot by: Kamachi#2491")


class Dnd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    dnd = discord.SlashCommandGroup('dnd', 'Death & Dungeons related commands')

    @dnd.command(name="create", description="Create your dnd character")
    async def create(self,
                     ctx: discord.ApplicationContext,
                     name: Option(str, "Please input the name of your character."),
                     age: Option(int, 'Please input the age of your character.'),
                     attribute: Option(str,
                                       'Please input the peronality/attribute of your character. ("Cold hearted (General)")'),
                     description: Option(str, 'Please write a background for your character.'),
                     group: Option(
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
                         ])):
        # init mongodb
        client = pymongo.MongoClient(environ.get('MONGOURI'))
        db = client['Fumiko']
        dnd_chars = db['dnd_chars']

        p = Player(id=ctx.author.id,
                   name=name,
                   age=age,
                   group=group,
                   attribute=attribute,
                   description=description,
                   skills=[
                       {
                           'name': 'You don\'t have any skill right now',
                           'lvl': None
                       },
                       {
                           'name': 'You dont have any skill right now',
                           'lvl': None
                       },
                   ],
                   stats={
                       'health': 100,
                       'stamina': 6,
                       'strength': 6,
                       'agility': 6,
                       'magic_power': 6,
                   })

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

        await ctx.respond(embed=PlayerInfoEmbed(p))

        client.close()

    @dnd.command(name='play', description='Play dnd!')
    async def play(self, ctx: discord.ApplicationContext):
        # init mongodb
        client = pymongo.MongoClient(environ.get('MONGOURI'))
        db = client['Fumiko']
        dnd_chars = db['dnd_chars']

        dnd_char = dnd_chars.find_one(
            {
                "_id": ctx.author.id
            }
        )

        p = Player(id=ctx.author.id,
                   name=dnd_char['name'],
                   age=dnd_char['age'],
                   group=dnd_char['group'],
                   attribute=dnd_char['attribute'],
                   description=dnd_char['description'],
                   skills=dnd_char['skills'],
                   stats=dnd_char['stats'])

        game = Game(player=p)

        play = game.play()

        await ctx.respond(f"{play}")

        dnd_chars.find_one_and_update(
            {
                "_id": ctx.author.id
            },
            {
                "$set": p.export()
            },
            upsert=True
        )

        client.close()


def setup(bot):
    bot.add_cog(Dnd(bot))
