import pydest
import discord
from discord.ext import commands
from discord.commands import OptionChoice, Option, slash_command


class Testd2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def testd2(
            self,
            ctx: discord.ApplicationContext):
        api_key = '5601a322825c4a75841a3a5f6678'
        destiny = pydest.Pydest(api_key)
        json = await destiny.api.search_destiny_player(1, 'slayer117')
        await ctx.respond(json)
        await destiny.close()

def setup(bot):
    bot.add_cog(Testd2(bot))