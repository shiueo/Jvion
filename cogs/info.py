import os
import platform
import time

import discord

from discord.ext import commands
import datetime
from discord.ext.commands import Context

from utils.footer import add_standard_footer


class Info(commands.Cog, name="info"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(
        name="info",
        description="Commands to provide information about the bot.",
    )
    async def info(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            await context.send("Please check the invoked subcommand.")

    @commands.command(name="about", description="Information about the bot.")
    async def about(self, context: Context):
        embed = discord.Embed(
            title="Jvion",
            description=f"{self.bot.bot_description}",
            color=self.bot.color_main,
        )
        embed.add_field(
            name="Prefix:",
            value=f"``/ (Slash Commands)`` or ``{self.bot.prefix}``",
            inline=True,
        )
        embed.add_field(
            name="Written in:", value=f"Python {platform.python_version()}", inline=True
        )
        embed.add_field(
            name="Running on:",
            value=f"{platform.system()} {platform.release()} ({os.name})",
            inline=True,
        )
        embed = add_standard_footer(context, embed)

        view = discord.ui.View()
        GithubURLButton = discord.ui.Button(
            label="Github Repository",
            style=discord.ButtonStyle.url,
            url="https://github.com/shiueo/Jvion",
        )
        PatreonURLButton = discord.ui.Button(
            label="shiüo's Patreon",
            style=discord.ButtonStyle.url,
            url="https://www.patreon.com/shiueo",
        )
        SchtarnDiscordURLButton = discord.ui.Button(
            label="Schtarn Discord",
            style=discord.ButtonStyle.url,
            url="https://discord.gg/NXwVfdcygM",
        )

        view.add_item(GithubURLButton)
        view.add_item(PatreonURLButton)
        view.add_item(SchtarnDiscordURLButton)

        await context.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Info(bot))
