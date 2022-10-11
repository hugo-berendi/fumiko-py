import discord
import os
from dotenv import load_dotenv

load_dotenv() 

# init intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# init the bot
bot = discord.Bot(
		intent=intents,
		debug_guilds=[990521467215171594]
)

# load events
for filename in os.listdir("./cogs/events"):
	if filename.endswith(".py"):
		bot.load_extension(f"cogs.events.{filename[:-3]}")

# load commands
for filename in os.listdir("./cogs/commands"):
	if filename.endswith(".py"):
		bot.load_extension(f"cogs.commands.{filename[:-3]}")

# run the bot
bot.run(os.environ.get("TOKEN"))
