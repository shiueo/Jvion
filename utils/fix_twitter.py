import discord
from discord.ext.commands import Context
import re


def is_valid_twitter_url(url):
    return url.startswith("https://twitter.com/") or url.startswith("https://x.com/")


async def fix_twitter(message: discord.Message, context: Context):
    content = message.content
    urls = re.findall(
        "http[s]?://(?:[a-zA-Z]|[0-9]|[$\-@\.&+:/?=]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        content,
    )

    modified_content = content
    for url in urls:
        if is_valid_twitter_url(url):
            modified_url = url.replace("twitter.com", "fxtwitter.com").replace(
                "x.com", "fxtwitter.com"
            )
            modified_content = modified_content.replace(url, modified_url)

    if modified_content != content:
        try:
            await message.delete()
            await context.send(f"{context.author.mention}: {modified_content}")

        except discord.Forbidden:
            await context.send("FixTwitter - I don't have the permission to delete messages.")
