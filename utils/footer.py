from datetime import datetime

import discord
from discord.ext.commands import Context


def add_standard_footer(context: Context, embed: discord.Embed):
    embed.set_footer(
        text=f"command requested by {context.author.display_name}\nUTC {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}",
        icon_url=context.author.avatar.url,
    )
    return embed
