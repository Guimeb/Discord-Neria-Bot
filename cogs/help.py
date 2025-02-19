import discord
from discord.ext import commands
from logs.log import logger

class HelpCommand(commands.Cog, name="help"):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(
    name="help",
    help="Displays the list of available commands.",
    aliases=["commands", "cmds", "assistance","ajuda", "h"]
  )
  async def commands_list(self, ctx):
      logger.info(f"$help command called by {ctx.author}")
  
      embed = discord.Embed(
          title="📜 List of Available Commands",
          description="Here are the commands available in the bot:",
          color=discord.Color.blue()
      )
  
      for command in self.bot.commands:
          embed.add_field(
              name=f"🔹 {ctx.prefix}{command.name}",
              value=command.help if command.help else "No description available.",
              inline=False
          )
  
      embed.set_footer(
          text=f"Use {ctx.prefix}help for more details."
      )

      await ctx.send(embed=embed)

async def setup(bot):
  await bot.add_cog(HelpCommand(bot))