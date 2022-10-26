import matplotlib.pyplot as plt
import numpy as np
import os
import discord
from discord.ext import commands
from discord.commands import OptionChoice, Option

class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    math = discord.SlashCommandGroup('math', 'Mathmatics related commands')

    @math.command(description="Calcs a graph", name="graph")
    async def graph(self, ctx: discord.ApplicationContext, function: Option(str, "Please enter a function for the Graph (syntax: x**2)")):  # type: ignore

        x = np.array(range(float(-50), float(50)))

        try:
            plt.plot(x, eval(function))
        except:
            await ctx.respond("error")
        else:
            plt.savefig("out.png")

            # create embed named emb
            emb = discord.Embed(
                title="Graph",
                description=f"```python\nf(x)={function}\n```",
                color=discord.Color.blue())

            # add output
            file = discord.File("out.png")
            emb.set_image(url="attachment://out.png")

            # add timestamp to emb
            emb.timestamp = discord.utils.utcnow()  # type: ignore

            await ctx.respond(file=file, embed=emb)

            plt.clf()

            os.remove("out.png")

    @math.command(description="Calcs a root with the heron method", name="heron")
    async def heron(self, ctx: discord.ApplicationContext,
                    n: Option(int, "Please enter the number you want the root from"),  # type: ignore
                    error: Option(int, "Please enter the error you want to have for the root")):  # type: ignore
        def heron(n: float, error: float):
            y = (n + n / n) / 2
            while abs(y - n / y) > error:
                y = (y + n / y) / 2
            return y

        # create embed named emb
        emb = discord.Embed(
            title="Root with heron method",
            description=f"```\n{heron(n, error)}\n```",
            color=discord.Color.blue())

        # add timestamp to emb
        emb.timestamp = discord.utils.utcnow()  # type: ignore

        await ctx.respond(embed=emb)


def setup(bot):
    bot.add_cog(Math(bot))
