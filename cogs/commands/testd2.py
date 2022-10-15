import requests
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
        userId = 1
        url = f"https://www.bungie.net/Platform/User/GetBungieNetUserById/{userId}/"
        myobjs = {'X-API-Key': '5601a322825c4a75841a3a5f6678'}
        r1 = requests.post(url, headers=myobjs)
        await ctx.respond(r1.json())



def setup(bot):
    bot.add_cog(Testd2(bot))