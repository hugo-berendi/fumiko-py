import matplotlib.pyplot as plt
import numpy as np
import os
import discord
from discord.ext import commands
from discord.commands import slash_command, Option


class Graph(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Calcs a graph", name="graph")
    async def info(self, ctx: discord.ApplicationContext,
                   function: Option(str, "Please enter a function for the Graph (syntax: x**2)")):

        x = np.array(range(1, 101))

        try:
            plt.plot(x, eval(function))
        except:
            await ctx.respond("error")
        else:
            plt.savefig("out.png")

            # create embed named emb
            emb = discord.Embed(
                title="Graph",
                description=f"```python\ny={function}\n```",
                color=discord.Color.blue())

            # add output
            file = discord.File("out.png")
            emb.set_image(url="attachment://out.png")

            # add timestamp to emb
            emb.timestamp = discord.utils.utcnow()

            await ctx.respond(file=file, embed=emb)

            plt.clf()

            os.remove("out.png")


def setup(bot):
    bot.add_cog(Graph(bot))
