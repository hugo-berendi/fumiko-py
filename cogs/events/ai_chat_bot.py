import discord
from prsaw import RandomStuff
from discord.ext import commands


class Chatbot(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if self.bot.user == message.author:
            return
        
        if message.channel.id == 991000357842849833:
            api_key = "i2JPF619bGn1"
            rs = RandomStuff(api_key=api_key, async_mode=True)

            input = message.content

            res = await rs.get_ai_response(input)
            await message.reply(res)

            rs.close()


def setup(bot):
    bot.add_cog(Chatbot(bot))
