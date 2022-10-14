import discord
from discord.ext import commands
from discord.commands import slash_command, Option


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Clear all Command", name="clear")
    async def info(self, ctx: discord.ApplicationContext, number: Option(int, "Amount of messages you want to delete")):
        mgs = []
        async for x in self.bot.logs_from(ctx.message.channel, limit=number):
                  mgs.append(x)
        await self.bot.delete_messages(mgs)

def setup(bot):
    bot.add_cog(Clear(bot))