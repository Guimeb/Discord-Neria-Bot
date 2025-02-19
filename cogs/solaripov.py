import discord
from discord.ext import commands
from logs.log import logger

class SolariPovCommand(commands.Cog, name="solpov"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="solari",
        help="Solari pov.",
        aliases=["illbeback"]
    )
    async def say_hello(self, ctx):
        logger.info(f"Comando $solpov chamado por {ctx.author}")
        embed = discord.Embed(
              title="🟣I'LL BE BACK",
              description="Solari Pov",
              color=discord.Color.blue()
        )
        embed.set_image(url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ2txbnl3MXp4ZGFzaHMzbjJ3ZWRsYWgxZWkyNmN6MTJzbzNycnF1bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l7ZFSdEdcDuiUxTgSy/giphy.gif")

        embed.set_footer(
              text="- Solari."
          )
        
        await ctx.send(embed=embed)

async def setup(bot):
  await bot.add_cog(SolariPovCommand(bot))