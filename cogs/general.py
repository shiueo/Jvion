import discord

from discord.ext import commands
from discord.ext.commands import Context


class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="명령어", description="봇의 모든 명령어를 알려드립니다.")
    async def help(self, context: Context):
        prefix = self.bot.config["prefix"]
        embed = discord.Embed(
            title="Help",
            description="List of available commands:",
            color=self.bot.color_main,
        )
        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            jeyviz_commands = cog.get_commands()
            data = []
            for command in jeyviz_commands:
                description = command.description.partition("\n")[0]
                data.append(f"{prefix}{command.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(
                name=i.capitalize(), value=f"```{help_text}```", inline=False
            )
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))
