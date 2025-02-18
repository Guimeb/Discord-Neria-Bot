import discord
from discord.ext import commands
from log import logger

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # 🔵 $help
    @commands.command(name="commands", help="Mostra a lista de comandos disponíveis.")
    async def commands_list(self, ctx):
        """Envia uma mensagem com todos os comandos disponíveis"""
        logger.info(f"Comando $help chamado por {ctx.author}")

        embed = discord.Embed(
            title="📜 Lista de Comandos Disponíveis",
            description="Aqui estão os comandos disponíveis no bot:",
            color=discord.Color.blue()
        )

        for command in self.bot.commands:
            embed.add_field(
                name=f"🔹 {ctx.prefix}{command.name}",
                value=command.help if command.help else "Sem descrição.",
                inline=False
            )

        embed.set_footer(text=f"Use {ctx.prefix}comando para mais detalhes.")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(BotCommands(bot))