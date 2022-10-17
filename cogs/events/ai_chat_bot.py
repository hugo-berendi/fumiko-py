import discord
from prsaw import RandomStuff
from discord.ext import commands


class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id != 991000357842849833:
            return

        api_key = 'i2JPF619bGn1'
        rs = RandomStuff(api_key=api_key)
        input = message.content
        res = rs.get_ai_response(input)

        await message.channel.send(res)

        rs.close()


def setup(bot):
    bot.add_cog(Ready(bot))
