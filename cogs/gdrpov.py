import discord
from discord.ext import commands
from logs.log import logger

class GdrnPovCommand(commands.Cog, name="gdrn"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="gdrn",
        help="Gdrn pov.",
        aliases=["gdr"]
    )
    async def say_hello(self, ctx):
        logger.info(f"Comando $gdrn chamado por {ctx.author}")
        embed = discord.Embed(
              title="É É É É É É",
              description="Gorila de radinho Pov",
              color=discord.Color.blue()
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/941125938274504705/1323919640157622282/330a9c88-74c3-477c-b9f6-5742b3fe13e9.gif?ex=67b8d77f&is=67b785ff&hm=08ef3c372d4d75314545830119a6b26121ca7a6dfb404e45e655eba9a7f9d625&")
        embed.set_footer(
              text="Eu errei - Gdrn."
          )
        
        await ctx.send(embed=embed)

async def setup(bot):
  await bot.add_cog(GdrnPovCommand(bot))