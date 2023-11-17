from datetime import datetime

import discord

from discord.ext import commands
from discord.ext.commands import Context


class DiscordUtil(commands.Cog, name="Discord Utils"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(
        name="discord_utils",
        description="디스코드 전용 여러 툴들",
    )
    async def discord_util(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="서브 커맨드를 정확히 확인해주세요.",
                color=self.bot.color_cancel,
            )
            await context.send(embed=embed)

    @discord_util.command(name="avatar", description="지정된 유저의 pfp를 가져옵니다.")
    async def avatar(self, context: Context, member: discord.Member):
        embed = discord.Embed(
            title=f"{member.display_name}'s pfp",
            color=self.bot.color_main
        )
        embed.set_image(url=member.avatar.url)
        embed.set_footer(
            text=f"command requested by {context.author.display_name}\n{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}",
            icon_url=context.author.avatar.url
        )
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(DiscordUtil(bot))
