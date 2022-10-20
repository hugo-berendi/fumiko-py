import discord
from discord.ext import commands
from discord.commands import message_command


class CogName(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @message_command(name="favourite", description="Sends the all the message information to your dm's")
    async def favourite(self, ctx: discord.ApplicationContext, message: discord.Message):
        embed = discord.Embed(
            title="Graph",
            description=f"{message.content}",
            color=discord.Color.yellow(),
            timestamp=discord.utils.utcnow()) # type: ignore
        
        embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
        
        await ctx.author.send(embed=embed)


def setup(bot:commands.Bot):
    bot.add_cog(CogName(bot))