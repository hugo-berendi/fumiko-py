import discord
import numpy
from discord.ext import commands, tasks


class Status(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.status.start()

    @tasks.loop(minutes=2)
    async def status(self):
        stasis = [
            discord.Status.idle,
            discord.Status.dnd,
            discord.Status.online
        ]

        members = []
        for guild in self.bot.guilds:
            for member in guild.members:
                members.append(member)

        activities = [
            discord.Game("by Kamachi"),
            discord.Game(f"mit {len(self.bot.guilds)} servern"),
            discord.Game(f"mit {len(members)} usern")
        ]

        await self.bot.change_presence(status=stasis[numpy.random.randint(0, len(stasis))],
                                       activity=activities[numpy.random.randint(0, len(activities))])

def setup(bot):
    bot.add_cog(Status(bot))
