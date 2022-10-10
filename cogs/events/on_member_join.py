import discord
from discord.ext import commands

class Welcome(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_join(self, member: discord.Member):
		emb = discord.Embed(
				title=f"Hi {member.name}",
				description=f"Willkommen auf {member.guild.name}",
				color=discord.Color.brand_green())

		channel = await self.bot.fetch_channel(990548560284114985)
		await channel.send(embed=emb)

def setup(bot):
	bot.add_cog(Welcome(bot))