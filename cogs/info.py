import os
import platform
import time

import discord

from discord.ext import commands
import datetime
from discord.ext.commands import Context


class Info(commands.Cog, name="info"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(
        name="정보",
        description="봇에 관한 설명이나 개발자의 대한 정보가 포함되어 있습니다.",
    )
    async def info(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="서브 커맨드를 정확히 확인해주세요.",
                color=self.bot.color_cancel,
            )
            await context.send(embed=embed)

    @info.command(name="봇", description="봇에 대한 정보를 알려드립니다.")
    async def info_bot(self, context: Context):
        embed = discord.Embed(
            description="shiüo 전용 봇",
            color=self.bot.color_main,
        )
        embed.set_author(name="Bot Information")
        embed.add_field(
            name="Prefix:", value="``/ (Slash Commands)`` or ``h!``", inline=True
        )
        embed.add_field(
            name="Written in:", value=f"Python {platform.python_version()}", inline=True
        )
        embed.add_field(
            name="Running on:",
            value=f"{platform.system()} {platform.release()} ({os.name})",
            inline=True,
        )
        embed.add_field(
            name="Github Repository",
            value="[Github](https://github.com/shiueo/HoiMP)",
            inline=False,
        )
        embed.add_field(
            name="Invite me!",
            value="[Link](https://discord.com/oauth2/authorize?client_id=1141564889819779153&permissions=535193578577&scope=applications.commands%20bot)",
            inline=False,
        )
        embed.set_footer(text=f"Requested by {context.author}")
        await context.send(embed=embed)

    @info.command(name="개발자", description="개발자에 대한 정보를 알려드립니다.")
    async def info_dev(self, context: Context):
        embed = discord.Embed(
            title="shiüo",
            description="제 여러 소셜 링크들입니다.",
            color=self.bot.color_main,
        )
        embed.set_image(url="https://something.png")
        embed.add_field(
            name="Youtube",
            value="[shiüo](https://www.youtube.com/@shiueo)",
            inline=True,
        )
        embed.add_field(
            name="Twitch",
            value="[shiüo](https://www.twitch.tv/shiueo)",
            inline=True,
        )
        embed.add_field(
            name="Website",
            value="[shiüo.dev](https://shiueo.dev)",
            inline=True,
        )
        embed.set_footer(text=f"Requested by {context.author}")
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Info(bot))
