import requests
import json
import discord
from discord.ext import commands
from discord.commands import OptionChoice, Option


class Nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    nsfw = discord.SlashCommandGroup('nsfw', 'Nsfw related commands')

    @nsfw.command()
    async def hentai(
            self,
            ctx: discord.ApplicationContext,
            type: Option(
                input_type=str,
                description='Choose the type for the hentai',
                choices=[
                    OptionChoice(name='4K', value='4k'),
                    OptionChoice(name='Blowjob', value='bj'),
                    OptionChoice(name='Boobs', value='boobs'),
                    OptionChoice(name='Cum', value='cum'),
                    OptionChoice(name='Feet', value='feet'),
                    OptionChoice(name='Random', value='hentai'),
                    OptionChoice(name='Wallpaper', value='wallpapers'),
                    OptionChoice(name='Butts', value='spank'),
                    OptionChoice(name='Ahegao', value='gasm'),
                    OptionChoice(name='Lesbian', value='lesbian'),
                    OptionChoice(name='Lewd', value='lewd'),
                    OptionChoice(name='😻', value='pussy'),
                ])):

        out_raw = requests.get(f"http://api.nekos.fun:8080/api/{type}/")
        out_raw_json = out_raw.json()
        out = json.loads(out_raw_json)['image']

        # create embed named emb
        emb = discord.Embed(
            title="Hentai",
            description=f"Type: {type}",
            color=discord.Color.blue())

        # add img
        emb.set_image(url=f"{out}")

        # add timestamp to emb
        emb.timestamp = discord.utils.utcnow()

        await ctx.respond(embed=emb)


def setup(bot):
    bot.add_cog(Nsfw(bot))
