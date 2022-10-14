import discord
from discord.ext import commands
from discord.commands import slash_command, Option


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Clear all Command", name="clear")
    async def info(self, ctx: discord.ApplicationContext, amount: Option(int, "Amount of messages you want to delete")):
        await ctx.defer()
        z = await ctx.channel.purge(limit=amount)
        await ctx.respond(f"I have deleted {len(z)} messages")

def setup(bot):
    bot.add_cog(Clear(bot))