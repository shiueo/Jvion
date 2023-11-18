import discord
from discord.ext import commands
from discord.ext.commands import Context


def is_valid_twitter_url(url):
    return url.startswith("https://twitter.com/") or url.startswith("https://x.com/")


class Twitter(commands.Cog, name="twitter"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(
        name="twitter",
        description="Commands for using Twitter more conveniently on Discord.",
    )
    async def twitter(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            await context.send("Please check the invoked subcommand.")

    @twitter.command(
        name="fix",
        description="Fixes a Twitter URL by replacing 'twitter.com' or 'x.com' with 'fxtwitter.com'.",
    )
    async def twitter_embed(self, context: Context, twitter_url: str):
        if is_valid_twitter_url(twitter_url):
            modified_url = twitter_url.replace("twitter.com", "fxtwitter.com").replace(
                "x.com", "fxtwitter.com"
            )
            await context.send(modified_url)
        else:
            await context.send(
                "Invalid Twitter URL. Please provide a valid Twitter URL."
            )


async def setup(bot):
    await bot.add_cog(Twitter(bot))
