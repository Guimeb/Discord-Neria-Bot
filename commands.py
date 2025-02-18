import discord
from discord.ext import commands
from log import logger
from raidManager import RaidMenuView, RaidManager


class BotCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def handle_raid_selection(self, interaction: discord.Interaction,
                                    raid_name: str):
        """Callback quando o líder da raid escolhe uma dungeon"""
        await interaction.response.defer()

        user = interaction.user  # Pegamos o usuário que interagiu
        channel = interaction.channel  # Pegamos o canal onde foi enviado

        await RaidManager.start_raid(user, channel, self.bot, raid_name
                                     )  # Passamos corretamente os argumentos

    # 🔵 $help
    @commands.command(name="help",
                      help="Mostra a lista de comandos disponíveis.")
    async def commands_list(self, ctx):
        logger.info(f"Comando $help chamado por {ctx.author}")

        embed = discord.Embed(
            title="📜 Lista de Comandos Disponíveis",
            description="Aqui estão os comandos disponíveis no bot:",
            color=discord.Color.blue())

        for command in self.bot.commands:
            embed.add_field(
                name=f"🔹 {ctx.prefix}{command.name}",
                value=command.help if command.help else "Sem descrição.",
                inline=False)

        embed.set_footer(text=f"Use {ctx.prefix}help para mais detalhes.")
        await ctx.send(embed=embed)

    # 🔵 $hello
    @commands.command(name="hello", help="Diz olá para você.")
    async def hello(self, ctx):
        logger.info(f"Comando $hello chamado por {ctx.author}")
        message = await ctx.send(f"Olá, {ctx.author.mention}!")
        await message.add_reaction("✅")
    
    # 🔵 $raid
    @commands.command(name="raid", help="Comece uma chamada de raid.")
    async def raid_start(self, ctx):

        view = RaidMenuView(ctx.author, self.handle_raid_selection)

        logger.info(f"Comando $raid chamado por {ctx.author}")

        embed = discord.Embed(
            title="📜 Escolha uma raid para iniciar",
            description=
            "Selecione qual raid você deseja iniciar no menu abaixo:",
            color=discord.Color.purple())
        embed.add_field(name="⚔️ Valtan",
                        value="Raid difícil, esteja preparado!",
                        inline=False)
        embed.add_field(name="🏰 Vykas",
                        value="Mecânicas desafiadoras!",
                        inline=False)
        embed.add_field(name="🔥 Kakul-Saydon",
                        value="Luta caótica e divertida!",
                        inline=False)
        embed.set_footer(text="Use o menu abaixo para escolher.")

        # Envia apenas para o líder da raid
        await ctx.send(embed=embed, view=view, delete_after=60)

    # 🔵 $reminder


async def setup(bot):
    await bot.add_cog(BotCommands(bot))
