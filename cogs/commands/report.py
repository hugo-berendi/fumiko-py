from discord import ApplicationContext, InputTextStyle
from discord.ext import commands
from discord.commands import slash_command
from discord.ui import View, InputText

class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Report something", name="report")
    async def report(self, ctx: ApplicationContext):
        testinput = InputText(
            style=InputTextStyle.long,
            custom_id="report_secret",
            label="Input your report",
            max_length=2000)

        view = View()

        view.add_item(testinput)

        await ctx.respond(view=view)

def setup(bot):
    bot.add_cog(Report(bot))