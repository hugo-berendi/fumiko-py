import matplotlib.pyplot as plt
import numpy as np
import os
import discord
import pymongo
from discord.ext import commands
from discord.commands import OptionChoice, Option


class DnD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    math = discord.SlashCommandGroup(
        'dnd', 'Dungeons & Dragons related commands')

    @math.command(name="create", description="Create your dnd character")
    async def create(self,
                    ctx: discord.ApplicationContext,
                    name: Option(str, "Please input the name of your character."),
                    description: Option(str, 'Please describe your character.'),
                    classs: Option(
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
        client = pymongo.MongoClient(f"mongodb+srv://hugob:{os.environ.get('MONGODB_TOKEN')}@cluster0.21jxy.mongodb.net/?retryWrites=true&w=majority")
        db = client['Fumiko']
        dnd_chars = db['dnd_chars']
        dnd_char = {
            "_id":         ctx.author.id,
            "owner":       ctx.author.display_name,
            "name":        name,
            "description": description,
            "class":       classs
        }

        # cmd actions
        dnd_chars.find_one_and_update(
                {
                    "_id": ctx.author.id
                },
                dnd_char
        )
        ctx.respond('I hope it worked xD')

    def setup(bot):
        bot.add_cog(DnD(bot))
