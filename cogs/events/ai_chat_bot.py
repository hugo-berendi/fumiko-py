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
            try:
                api_key = "i2JPF619bGn1"
                rs = RandomStuff(api_key=api_key, async_mode=True, dev_name="Kamachi", bot_name="Fumiko")

                res = await rs.get_ai_response(message.content)
                await message.reply(res)

                rs.close()
            except Exception as error:
                # create embed named emb
                emb = discord.Embed(
                    title="Error",
                    description=f"```\n{error}\n```",
                    color=discord.Color.red())

                # add timestamp to emb
                emb.timestamp = discord.utils.utcnow()

                await message.reply(embed=emb)


def setup(bot):
    bot.add_cog(Chatbot(bot))
