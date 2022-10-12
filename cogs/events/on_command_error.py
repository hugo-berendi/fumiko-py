import discord
from discord.ext import commands

class Ready(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_application_command_error(self, ctx, error):
            # create embed named emb
            emb = discord.Embed(
                title="Error",
                description=f"```\n{error}\n```",
                color=discord.Color.red())

            # add timestamp to emb
            emb.timestamp = discord.utils.utcnow()

            await ctx.respond(embed=emb)

def setup(bot):
	bot.add_cog(Ready(bot))