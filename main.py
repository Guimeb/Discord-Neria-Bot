import json
import os
import sys
import traceback
import asyncio

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context

from logs.log import logger

# 🟢 JSON Configuration
if not os.path.isfile(
        f"{os.path.realpath(os.path.dirname(__file__))}/config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json"
              ) as file:
        config = json.load(file)

# 🟢 Bot Configuration
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config["prefix"], intents=intents)
bot.remove_command("help")

# 🔵 Bot Ready Log
@bot.event
async def on_ready():
    connect_msg = f'✅ Bot connected as {bot.user}'
    logger.info(connect_msg) 
    print(connect_msg)

# 🔴 Bot Disconnected
@bot.event
async def on_disconnect():
    disconnect_msg = '🛑 Bot disconnected'
    logger.info(disconnect_msg)
    print(disconnect_msg)

# 🔴 Bot Error Handling
@bot.event
async def on_error(event, *args, **kwargs):
    error_msg = f"⚠️ Error detected in event '{event}':\n{traceback.format_exc()}"
    logger.error(error_msg)
    print(error_msg)

# 🟢 Load Cogs
async def load_cogs():
    await bot.load_extension("cogs.help")
    await bot.load_extension("cogs.hello")
    await bot.load_extension("cogs.raid")
    await bot.load_extension("cogs.solpov")
    #await bot.load_extension("cogs.commands") 

# 🟢 Bot Startup
async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv('Discord_Key'))

asyncio.run(main())
