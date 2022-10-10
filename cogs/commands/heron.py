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
			return format(new, ".50f")

		# create embed named emb
		emb = discord.Embed(
			title="Graph",
			description="",
			color=discord.Color.blue())

		# add output
		sp.preview(r'$' + heron(n, 0.01) + '§', output="png", filename='out.png', euler=False)
		file = discord.File("out.png")
		emb.set_image(url="attachment://out.png")

		# add timestamp to emb
		emb.timestamp = discord.utils.utcnow()

		await ctx.respond(file=file, embed=emb)

		os.remove("out.png")

def setup(bot):
	bot.add_cog(Heron(bot))