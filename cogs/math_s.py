import discord

from discord.ext import commands
from discord.ext.commands import Context


class Math(commands.Cog, name="math"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(
        name="math",
        description="봇에 관한 설명이나 개발자의 대한 정보가 포함되어 있습니다.",
    )
    async def math_s(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="서브 커맨드를 정확히 확인해주세요.",
                color=self.bot.color_cancel,
            )
            await context.send(embed=embed)

    @math_s.command(name="add", description="봇에 대한 정보를 알려드립니다.")
    async def addition(self, context: Context, num_1: int, num_2: int):
        await context.send(f"{num_1} + {num_2} = {num_1 + num_2}")


async def setup(bot):
    await bot.add_cog(Math(bot))
