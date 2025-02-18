import discord
import asyncio
from discord.ui import View, Select
from log import logger


class RaidManager:
    active_raids = {}  # Dicionário para rastrear raids ativas

    @staticmethod
    async def start_raid(user, channel, bot, raid_name):

        embed = discord.Embed(
            title=f"🚀 {raid_name} RAID INICIADA!",
            description=f"{user.mention} iniciou uma **{raid_name}**!\n"
            f"⏳ **Você tem 5 minutos para entrar na raid!**\n"
            f"Reaja abaixo para participar!",
            color=discord.Color.red())
        embed.add_field(name="🔹 Participantes:",
                        value=f"1️⃣ {user.mention}",
                        inline=False)
        embed.set_footer(
            text="A raid começará automaticamente após 5 minutos.")

        raid_message = await channel.send(content="@raid", embed=embed)
        await raid_message.add_reaction("✅")

        RaidManager.active_raids[raid_message.id] = {
            "leader": user,
            "raid_name": raid_name,
            "participants": [user],
            "message": raid_message
        }

        await asyncio.sleep(300)  # 5 minutos

        final_raid = RaidManager.active_raids.pop(raid_message.id, None)
        if final_raid:
            final_embed = discord.Embed(
                title=f"🚀 {raid_name} RAID FECHADA!",
                description=f"A raid **{raid_name}** foi fechada!\n",
                color=discord.Color.green())

            participantes_texto = "\n".join([
                f"{i+1}️⃣ {p.mention}"
                for i, p in enumerate(final_raid['participants'])
            ])
            final_embed.add_field(name="🔹 Participantes finais:",
                                  value=participantes_texto,
                                  inline=False)

            await raid_message.edit(embed=final_embed)

        # Criar e exibir menu suspenso para o líder
        view = RaidMenuView(ctx.author, raid_callback)
        await ctx.send(
            f"{ctx.author.mention}, escolha a raid que deseja iniciar:",
            view=view,
            delete_after=60)

    @staticmethod
    async def add_player_to_raid(reaction, user):
        if user.bot:
            return

        if reaction.message.id in RaidManager.active_raids:
            logger.info(f"{user} reagiu a raid {reaction.message.id}")
            raid_info = RaidManager.active_raids[reaction.message.id]

            if len(raid_info["participants"]) >= 8:
                await user.send("⚠️ Essa raid já está cheia!")
                return

            if user not in raid_info["participants"]:
                raid_info["participants"].append(user)

                embed = raid_info["message"].embeds[0]
                participantes_texto = "\n".join([
                    f"{i+1}️⃣ {p.mention}"
                    for i, p in enumerate(raid_info['participants'])
                ])
                embed.set_field_at(0,
                                   name="🔹 Participantes:",
                                   value=participantes_texto,
                                   inline=False)

                await raid_info["message"].edit(embed=embed)


# 🔹 Criando a View e o Menu suspenso dentro do mesmo arquivo
class RaidMenuView(View):
    """Cria um menu suspenso para o líder escolher a raid"""

    def __init__(self, leader, callback):
        super().__init__()
        self.leader = leader
        self.callback = callback
        self.add_item(RaidSelectMenu(callback))


class RaidSelectMenu(Select):
    """Cria o menu suspenso com as opções de raids"""

    def __init__(self, callback):
        options = [
            discord.SelectOption(label="Raid 1",
                                 description="Descrição da Raid 1",
                                 emoji="⚔️"),
            discord.SelectOption(label="Raid 2",
                                 description="Descrição da Raid 2",
                                 emoji="🏰"),
            discord.SelectOption(label="Raid 3",
                                 description="Descrição da Raid 3",
                                 emoji="🔥"),
        ]
        super().__init__(placeholder="Escolha a raid...", options=options)
        self.callback_func = callback  # Renomeamos para evitar conflito com o callback do discord.py

    async def callback(self, interaction: discord.Interaction):
        """Quando o líder escolhe uma raid"""
        await self.callback_func(interaction, self.values[0])
