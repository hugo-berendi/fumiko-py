import sympy as sp
import os
import discord
from discord.ext import commands
from discord.commands import slash_command, Option

class Heron(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@slash_command(description="Calcs a root with the heron method", name="heron")
	async def info(self, ctx: discord.ApplicationContext, n: Option(float, "Please enter the number you want the root from"), error: Option(float, "Please enter the error you want to have for the root")):

		def heron(n: float, error: float):
			y = (n + n / n) / 2
			while abs(y - n / y) > error:
				y = (y + n / y) / 2
			return y

		# create embed named emb
		emb = discord.Embed(
			title="Graph",
			description=f"```\n{heron(n, error)}\n```",
			color=discord.Color.blue())

		# add timestamp to emb
		emb.timestamp = discord.utils.utcnow()

		await ctx.respond(embed=emb)

def setup(bot):
	bot.add_cog(Heron(bot))