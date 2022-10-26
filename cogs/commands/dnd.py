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
        self.player = player

    async def send(self, ctx: discord.ApplicationContext):
        def skills():
            skills = ""
            for skill in self.player.export()['skills']:
                if skill['lvl'] == None:
                    skills += f"{skill['name']}\n"
                else:
                    skills += f"{skill['name']} Lv. {skill['lvl']}\n"
            return skills

        emb = discord.Embed(
            title="[Character Information]",
            description="",
            color=discord.Color.from_rgb(38, 184, 237),
            fields=[
                discord.EmbedField(name='Name', value=self.player.export()['name'], inline=True),
                discord.EmbedField(name='Age', value=f"{self.player.export()['age']} years old.", inline=True),
                discord.EmbedField(name='Group', value=self.player.export()['group'], inline=True),
                discord.EmbedField(name='Description', value=self.player.export()['description'], inline=False),
                discord.EmbedField(name='Attribute', value=f"{self.player.export()['attribute']}", inline=False),
                discord.EmbedField(name='Skills', value=f"{skills()}", inline=False),
                discord.EmbedField(name='Overall Stats',
                                   value=f"""
                                   Health:         {self.player.export()["stats"]["health"]}hp
                                   Stamina:        Lv. {self.player.export()["stats"]["stamina"]}
                                   Strength:       Lv. {self.player.export()["stats"]["strength"]}
                                   Agility:        Lv. {self.player.export()["stats"]["agility"]}
                                   Magic Power:    Lv. {self.player.export()["stats"]["magic_power"]}
                                   """,
                                   inline=False)
            ],
            timestamp=discord.utils.utcnow())
        emb.set_footer(text="Bot by: Kamachi#2491")

        emb_send = await ctx.respond(embed=emb, ephemeral=True)
        return emb_send


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
                                       'Please input the peronality/attribute of your character. ("Cold hearted")'),
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

        player = Player(id=ctx.author.id,
                        name=name,
                        age=age,
                        group=group,
                        attribute=attribute,
                        description=description,
                        skills=[
                            {
                                'name': 'You don\'t have any skill right now',
                                'lvl': None
                            }
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
                "$set": player.export()
            },
            upsert=True
        )

        embed = PlayerInfoEmbed(player)
        await embed.send(ctx)

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

        player = Player(id=ctx.author.id,
                   name=dnd_char['name'],
                   age=dnd_char['age'],
                   group=dnd_char['group'],
                   attribute=dnd_char['attribute'],
                   description=dnd_char['description'],
                   skills=dnd_char['skills'],
                   stats=dnd_char['stats'])

        game = Game(player)

        play = game.play()

        await ctx.respond(f"{play}")

        dnd_chars.find_one_and_update(
            {
                "_id": ctx.author.id
            },
            {
                "$set": player.export()
            },
            upsert=True
        )

        client.close()

    @dnd.command(name='status', description='Shows the status window of you or another user.')
    async def status(self,
                     ctx: discord.ApplicationContext,
                     user: Option(discord.Member, 'The member you want the status from.', default=None)):
        # init mongodb
        client = pymongo.MongoClient(environ.get('MONGOURI'))
        db = client['Fumiko']
        dnd_chars = db['dnd_chars']

        if user is None:
            user = ctx.author

        if user != ctx.author:
            u_char = dnd_chars.find_one({"_id": ctx.author.id})
            has_skill = next((skill for skill in u_char['skills'] if skill['name'] == "status window"), False)
            if has_skill == None:
                embed = discord.Embed(
                    title="Error",
                    description="You need the skill `status window to use this interaction on other player.`",
                    color=discord.Color.red(),
                    timestamp=discord.utils.utcnow())

                await ctx.respond(embed=embed, ephemeral=True)
                return

        dnd_char = dnd_chars.find_one({"_id": user.id})

        if dnd_char == None:
            embed = discord.Embed(
                title="Error",
                description="```This user doesn\'t has a DnD character!```",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow())

            await ctx.respond(embed=embed, ephemeral=True)
            return

        player = Player(id=user.id,
                        name=dnd_char['name'],
                        age=dnd_char['age'],
                        group=dnd_char['group'],
                        attribute=dnd_char['attribute'],
                        description=dnd_char['description'],
                        skills=dnd_char['skills'],
                        stats=dnd_char['stats'])

        embed = PlayerInfoEmbed(player)
        await embed.send(ctx)




def setup(bot):
    bot.add_cog(Dnd(bot))
