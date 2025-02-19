import discord
from discord.ext import commands
from logs.log import logger

class HelloCommand(commands.Cog, name="hello"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="hello",
        help="Diz olá para você.",
        aliases=["oi"]
    )
    async def say_hello(self, ctx):
        logger.info(f"Comando $hello chamado por {ctx.author}")
        await ctx.send(f"Olá, {ctx.author.mention}!")

async def setup(bot):
  await bot.add_cog(HelloCommand(bot))