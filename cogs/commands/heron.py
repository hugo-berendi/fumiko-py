import sympy as sp
import os
import discord
from discord.ext import commands
from discord.commands import slash_command, Option

class Heron(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@slash_command(description="Calcs a root with the heron method", name="heron")
	async def info(self, ctx: discord.ApplicationContext, n: Option(str, "Please enter the number you want the root from")):

		def heron(n: float, error: float):
			prev = 1.0
			new = (1+n)/2
			while abs(new-prev) > error:
				prev = new
				new = (new+n/new)/2
			return new

		# create embed named emb
		emb = discord.Embed(
			title="Graph",
			description=f"{heron(n, 0.01)}",
			color=discord.Color.blue())

		# add timestamp to emb
		emb.timestamp = discord.utils.utcnow()

		await ctx.respond(embed=emb)

def setup(bot):
	bot.add_cog(Heron(bot))