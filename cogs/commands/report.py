import discord
from discord.ext import commands
from discord.commands import slash_command, Option


class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Report something", name="report")
    async def report(self, ctx: discord.ApplicationContext):
        class MyModal(discord.ui.Modal):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)

                self.add_item(discord.ui.InputText(label="Long Input", style=discord.InputTextStyle.long))

            async def callback(self, interaction: discord.Interaction):
                embed = discord.Embed(title="Modal Results")
                embed.add_field(name="Long Input", value=self.children[1].value)
                await interaction.response.send_message(embeds=[embed])

        modal = MyModal(title="Modal via Slash Command")
        await ctx.send_modal(modal)


def setup(bot):
    bot.add_cog(Report(bot))