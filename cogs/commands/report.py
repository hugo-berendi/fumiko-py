import discord
from discord.ext import commands
from discord.commands import slash_command, Option


class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Report something", name="report")
    async def report(self, ctx: discord.ApplicationContext, message: Option(str, 'Message')):

        class MyModal(discord.ui.Modal):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(
                    discord.ui.InputText(
                        label="Short Input",
                        placeholder="Placeholder Test",
                    ),
                    discord.ui.InputText(
                        label="Longer Input",
                        value="Longer Value\nSuper Long Value",
                        style=discord.InputTextStyle.long,
                    ),
                    *args,
                    **kwargs,
                )

            async def callback(self, interaction: discord.Interaction):
                embed = discord.Embed(
                    title="Your Modal Results",
                    fields=[
                        discord.EmbedField(
                            name="First Input", value=self.children[0].value, inline=False
                        ),
                        discord.EmbedField(
                            name="Second Input", value=self.children[1].value, inline=False
                        ),
                    ],
                    color=discord.Color.random(),
                )
                await interaction.response.send_message(embeds=[embed])

        modal = MyModal(title="Message Command Modal")
        modal.title = f"Modal for Message ID: {message.id}"
        await ctx.send_modal(modal)


def setup(bot):
    bot.add_cog(Report(bot))