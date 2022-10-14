from discord import Status, Game, Bot
import numpy
from discord.ext import commands, tasks


class Status(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.status.start()

    @tasks.loop(seconds=20)
    async def status(self):
        stati = [
            Status.idle,
            Status.dnd,
            Status.online
        ]
        activities = [
            Game("by Kamachi#2491"),
            Game(f"mit {len(self.bot.guilds)} servern")
        ]

        await self.bot.change_presence(status=stati[numpy.random.randint(0, len(stati))],
                                       activity=activities[numpy.random.randint(0, len(activities))])


def setup(bot):
    bot.add_cog(Status(bot))
