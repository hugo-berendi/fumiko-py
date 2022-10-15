import discord
import requests
from discord.ext import commands
from discord.commands import OptionChoice, Option, slash_command


class Testd2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def testd2(
            self,
            ctx: discord.ApplicationContext):
        api_key = '22b29c4bd9a649bfab415322dcca1ec4'
        headers = {
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        }
        api_url = 'https://www.bungie.net/Platform'
        get_vendor_path = f"/Destiny2/Vendors/"
        r = requests.post(url=(api_url+get_vendor_path), headers=headers)
        await ctx.respond(f"````\n{r.json()}\n```")



def setup(bot):
    bot.add_cog(Testd2(bot))
