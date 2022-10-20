import discord
import os
from dotenv import load_dotenv

load_dotenv()

# init intents
intents = discord.Intents.all()

# init the bot
bot = discord.Bot(
    intent=intents,
    debug_guilds=[990521467215171594]
)

cog_dirs = [f.path for f in os.scandir("./cogs") if f.is_dir()]

# load cogs #
for cog_dir in cog_dirs:
    for filename in os.listdir(f"{cog_dir}"):
        if filename.endswith(".py"):
            bot.load_extension(
                f"cogs.{cog_dir.split('/')[-1]}.{filename[:-3]}")

# run the bot
bot.run(os.environ.get("TOKEN"))
