from datetime import datetime

import discord

from discord.ext import commands
from discord.ext.commands import Context

from utils.footer import add_standard_footer


class DiscordUtil(commands.Cog, name="Discord Utils"):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name="discord_utils",
        description="Various tools for Discord.",
    )
    async def discord_util(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Please check the invoked subcommand.",
                color=self.bot.color_cancel,
            )
            await context.send(embed=embed)

    @discord_util.command(name="avatar", description="Get the specified user's profile picture.")
    async def avatar(self, context: Context, member: discord.Member):
        embed = discord.Embed(
            title=f"{member.display_name}'s profile picture", color=self.bot.color_main
        )
        embed.set_image(url=member.avatar.url)
        embed = add_standard_footer(context, embed)
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(DiscordUtil(bot))
