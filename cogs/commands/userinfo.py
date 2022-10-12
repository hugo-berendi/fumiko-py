import discord
from discord.ext import commands
from discord.commands import slash_command, Option


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Info Command", name="userinfo")
    async def info(self, ctx: discord.ApplicationContext, user: Option(discord.User, "User", default=None)):
        # test if a user was given
        if user is None:
            user = ctx.author

        # create embed named emb
        emb = discord.Embed(
            title=f"Infos über {user.name}",
            description=f"Hier siehst du alle Infos über {user.mention}",
            color=user.color)

        # add fields to emb
        time = discord.utils.format_dt(user.created_at, style="R")
        emb.add_field(name="Created at", value=time, inline=False)
        emb.add_field(name="ID", value=f"{user.id}", inline=False)
        # add thumbnail to emb
        emb.set_thumbnail(url=user.display_avatar.url)
        # add footer to emb
        emb.set_footer(text="Bot by: Kamachi#2491")
        # add timestamp to emb
        emb.timestamp = discord.utils.utcnow()

        await ctx.respond(embed=emb)


def setup(bot):
    bot.add_cog(Info(bot))
