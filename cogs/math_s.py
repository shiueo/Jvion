import discord

from discord.ext import commands
from discord.ext.commands import Context


class Math(commands.Cog, name="math"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(
        name="math",
        description="Contains commands related to math operations.",
    )
    async def math_s(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            await context.send("Please check the invoked subcommand.")

    @math_s.command(name="add", description="Perform addition with two numbers.")
    async def addition(self, context: Context, num_1: int, num_2: int):
        await context.send(f"{num_1} + {num_2} = {num_1 + num_2}")


async def setup(bot):
    await bot.add_cog(Math(bot))
