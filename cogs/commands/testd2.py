import aiobungie
import discord
from discord.ext import commands
from discord.commands import OptionChoice, Option, slash_command


class Testd2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def testd2(
            self,
            ctx: discord.ApplicationContext):
        api_key = '22b29c4bd9a649bfab415322dcca1ec4'
        client = aiobungie.Client(api_key)

        async def main() -> None:
            # Fetch a charatcer with all its components.
            # This includes Equimpents, Inventory, Records, etc.
            async with client.rest:
                my_warlock = await client.fetch_character(
                    1,
                    aiobungie.MembershipType.STEAM,
                    1,
                    components=[aiobungie.Component.ALL_CHARACTERS]
                )

                for activity in my_warlock.activities:
                    # Check if activity is a raid.
                    if activity.current_mode and activity.current_mode is aiobungie.GameMode.RAID:
                        ctx.channel.send(activity.avaliable_activities)  # All raids for this character.

        # You can either run it using the client or just asyncio.run(main())
        await client.run(main())
        await ctx.respond('suc')


def setup(bot):
    bot.add_cog(Testd2(bot))
