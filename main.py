import asyncio
import datetime
import json
import logging
import os
import pathlib
import platform
import random
import sys
import time

import discord as discord

from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context

from utils.fix_twitter import fix_twitter
from utils.utils_logger import LoggingFormatter

if not os.path.isfile("config.json"):
    sys.exit("config.json이 없습니다. 확인해주세요.")
else:
    with open("config.json", encoding="utf8") as f:
        config = json.load(f)

intents = discord.Intents.all()

bot = Bot(
    command_prefix=commands.when_mentioned_or(config["prefix"]),
    intents=intents,
    help_command=None,
)

bot.config = config
bot.abs_path = os.path.dirname(__file__)
bot.prefix = config["prefix"]
bot.bot_description = config["bot_description"]

bot.start_time = time.time()
bot.color_main = int(config["color_main"], 16)
bot.color_thank = int(config["color_thank"], 16)
bot.color_success = int(config["color_success"], 16)
bot.color_cancel = int(config["color_cancel"], 16)
bot.owners = config["owners"]

logger = logging.getLogger("Jvion")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
# File handler

file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)

# Add the handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)
bot.logger = logger

if not os.path.isdir("./database"):
    os.mkdir("./database")


@bot.event
async def on_ready():
    bot.logger.info(f"Logged in as {bot.user.name}")
    bot.logger.info(f"discord.py API version: {discord.__version__}")
    bot.logger.info(f"Python version: {platform.python_version()}")
    bot.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    bot.logger.info("-------------------")
    bot.logger.info("Syncing commands globally...")
    status_task.start()
    """
    bot.tree.copy_global_to(guild=discord.Object(id=1074197704596520971))
    await bot.tree.sync(guild=discord.Object(id=1074197704596520971))
    """
    await bot.tree.sync()


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user or message.author.bot:
        return
    context = await bot.get_context(message)
    await fix_twitter(message, context)
    await bot.process_commands(message)


@bot.event
async def on_command_error(context: Context, error):
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            description=f"이 명령어는 {f'{round(hours)} 시간' if round(hours) > 0 else ''} {f'{round(minutes)} 분' if round(minutes) > 0 else ''} {f'{round(seconds)} 초' if round(seconds) > 0 else ''} 뒤에 다시 사용하실 수 있습니다.",
            color=bot.color_cancel,
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            description="You are missing the permission(s) `"
            + ", ".join(error.missing_permissions)
            + "` to execute this command!",
            color=0xE02B2B,
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(
            description="I am missing the permission(s) `"
            + ", ".join(error.missing_permissions)
            + "` to fully perform this command!",
            color=0xE02B2B,
        )
        await context.send(embed=embed)


@bot.event
async def on_command_completion(context: Context):
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    if context.guild is not None:
        bot.logger.info(
            f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})"
        )
    else:
        bot.logger.info(
            f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs"
        )


@bot.event
async def on_reaction_add(reaction, user):
    if str(reaction.emoji) == "✅" and not user.bot:
        if reaction.message.id in bot.reservations.keys():
            role = reaction.message.guild.get_role(
                bot.reservations[reaction.message.id][1]
            )
            if role:
                await user.add_roles(role)
    if str(reaction.emoji) == "❌" and not user.bot:
        if reaction.message.id in bot.reservations.keys():
            role = reaction.message.guild.get_role(
                bot.reservations[reaction.message.id][2]
            )
            if role in user.roles:
                del bot.reservations[reaction.message.id]
                await reaction.message.delete()


@bot.event
async def on_reaction_remove(reaction, user):
    if str(reaction.emoji) == "✅" and not user.bot:
        if reaction.message.id in bot.reservations.keys():
            role = reaction.message.guild.get_role(
                bot.reservations[reaction.message.id][1]
            )
            if role:
                await user.remove_roles(role)


async def load_cogs():
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                bot.logger.info(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                bot.logger.error(f"Failed to load extension {extension}\n{exception}")


@tasks.loop(minutes=1.0)
async def status_task():
    statuses = [
        "für shiüo",
    ]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))


allowed_mentions = discord.AllowedMentions(roles=True)

asyncio.run(load_cogs())
bot.run(config["token"])
