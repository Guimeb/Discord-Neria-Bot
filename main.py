import discord
from discord.ext import commands
import os
import traceback
import asyncio
from log import logger

# 🟢 Bot Config
intents = discord.Intents.default()
intents.message_content = True  # Permite ler mensagens

bot = commands.Bot(command_prefix="$", intents=intents)
bot.remove_command("help")

# 🔵 Bot ready log
@bot.event
async def on_ready():
    connect_msg = f'✅ Bot conectado como {bot.user}'
    logger.info(connect_msg) 
    print(connect_msg)

# 🔴 Bot disconected
@bot.event
async def on_disconnect():
    disconnect_msg = '🛑 Bot desconectado'
    logger.info(disconnect_msg)
    print(disconnect_msg)

# 🔴 Bot error
@bot.event
async def on_error(event, *args, **kwargs):
    error_msg = f"⚠️ Erro detectado no evento '{event}':\n{traceback.format_exc()}"
    logger.error(error_msg)
    print(error_msg)

async def load_cogs():
  await bot.load_extension("commands")  # Carrega a extensão de comandos

# 🟢 Bot Start
async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv('Discord_Key'))

asyncio.run(main())
