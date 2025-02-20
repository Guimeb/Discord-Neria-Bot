import discord
from discord.ext import commands
from discord.ui import View, Select
from logs.log import logger
from datetime import timedelta

class RaidSelectMenu(Select): # Raid Dropdown
    def __init__(self, callback_func):
        options = [
            discord.SelectOption(label="Thaemine", description="Thaemine Raid", emoji="⚔️"),
            discord.SelectOption(label="Behemot", description="Behemot Raid", emoji="🐲"),
            discord.SelectOption(label="Echidna", description="Echidna Raid", emoji="🐍"),
            discord.SelectOption(label="Aegir", description="Aegir Raid", emoji="🧑‍🦯"),
            discord.SelectOption(label="Brel", description="Brel Raid", emoji="☄️"),
        ]
        super().__init__(placeholder="Choose a raid...", options=options)
        self.callback_func = callback_func

    #Callback when user selects an option
    async def callback(self, interaction: discord.Interaction):
        await self.callback_func(interaction, self.values[0], interaction.message)


class RaidMenuView(View): # Raid Dropdown View
    def __init__(self, raid_callback):
        super().__init__()
        self.add_item(RaidSelectMenu(raid_callback))


class RaidCommand(commands.Cog, name="raid"): # Comando Raid
    def __init__(self, bot):
        self.bot = bot

    active_raids = {}  # Stores active raids {message_id: {"leader": user, "raid": name, "players": [], "max_players": int}}

    @commands.command(
        name="raid",
        help="Start a raid.",
        aliases=["dungeon"]
    )
    async def start_raid(self, ctx): # Sent to author private, raid selection menu
        logger.info(f"$raid command called by {ctx.author}")

        embed = discord.Embed( # Raid show embed
            title="⚔️ Choose a raid to start",
            description="Select the raid you want to start from the menu below:",
            color=discord.Color.purple()
        )
        embed.add_field(name="⚔️ Thaemine", value="", inline=False)
        embed.add_field(name="🐲 Behemot", value="", inline=False)
        embed.add_field(name="🐍 Echidna", value="", inline=False)
        embed.add_field(name="🧑‍🦯 Aegir", value="", inline=False)
        embed.add_field(name="☄️ Brel", value="", inline=False)
        embed.set_footer(text="Use the menu below to choose.")

        view = RaidMenuView(self.raid_selected) 

        # Send a DM (private message) to the user
        try:
            user_dm = await ctx.author.send(embed=embed, view=view)
        except discord.Forbidden:
            await ctx.send(f"{ctx.author.mention}, I couldn't send you a private message. Please enable DMs!")
            return

        # Store the original channel to announce the raid later
        self.active_raids[ctx.author.id] = {"channel": ctx.channel, "dm_message": user_dm}

    # Raid show embed
    async def raid_selected(self, interaction: discord.Interaction, raid_name: str, message: discord.Message): 
        await interaction.response.defer()

        # Delete the previous private message
        try:
            await message.delete()
        except discord.NotFound:
            pass  # Ignore if already deleted

        channel_info = self.active_raids.pop(interaction.user.id, None)
        if not channel_info:
            return

        channel = channel_info["channel"]

        # Determine max players for the selected raid
        max_players = 16 if "Behemot" in raid_name else 8

        embed = discord.Embed(
            title=f"🚀 Raid {raid_name} Started!",
            description=f"{interaction.user.mention} has started a **{raid_name}** raid!\n\n"
                        "React with ✅ to join the raid!\n\n"
                        f"**Max Players: {max_players}**",
            color=discord.Color.green()
        )

        embed.set_footer(text="Players can now join by reacting.")

        # Send public message
        raid_message = await channel.send(embed=embed)
        self.bot.loop.create_task(self.close_raid_after_timeout(raid_message.id, 100))

        await raid_message.add_reaction("✅")  # Add reaction for players to join

        # Store raid info in active_raids
        self.active_raids[raid_message.id] = {
            "leader": interaction.user,
            "raid": raid_name,
            "players": [interaction.user],  # Leader is auto-included
            "max_players": max_players,
            "message": raid_message
        }

        logger.info(f"📝 Raid started: {raid_name} by {interaction.user} (Message ID: {raid_message.id})")
        self.log_active_raids()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user): # Add user to raid on reaction
        if user.bot or reaction.emoji != "✅":
            return

        raid_info = self.active_raids.get(reaction.message.id)
        if not raid_info:
            return

        if user in raid_info["players"]:
            return  # User already joined

        if len(raid_info["players"]) >= raid_info["max_players"]:
            try:
                await user.send("⚠️ This raid is already full!")
            except discord.Forbidden:
                pass
            return

        raid_info["players"].append(user)

        self.update_raid_embed(raid_info)
        logger.info(f"✅ {user} joined the raid {raid_info['raid']} (Message ID: {reaction.message.id})")
        self.log_active_raids()

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        logger.info(f"📥 on_raw_reaction_remove triggered: \n {payload}")

        # Ignore bot's own reactions
        if payload.user_id == self.bot.user.id:
            return

        # Get the raid info for this message
        raid_info = self.active_raids.get(payload.message_id)
        if not raid_info:
            return

        # Get the guild and user objects
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            logger.info("⚠️ Guild not found.")
            return

        user = guild.get_member(payload.user_id)
        if not user:
            logger.info("⚠️ User not found.")
            return

        # ✅ Prevent the leader from removing themselves
        if user == raid_info["leader"]:
            logger.info("⚠️ Leader's reaction ignored.")
            return  # Ignore the leader's reaction

        # Only remove if the reaction is the correct one
        if payload.emoji.name != "✅":
            return

        # Check if the user is in the players list
        if user in raid_info["players"]:
            raid_info["players"].remove(user)
            self.update_raid_embed(raid_info)
            logger.info(f"❌ {user} left the raid {raid_info['raid']} (Message ID: {payload.message_id})")
            self.log_active_raids()
        else:
            logger.info("⚠️ User was not in the raid participants list.")

    def update_raid_embed(self, raid_info): # Update raid embed
        participant_list = "\n".join([f"✅ {p.mention}" for p in raid_info["players"]])
        embed = raid_info["message"].embeds[0]
        embed.description = f"{raid_info['leader'].mention} has started a **{raid_info['raid']}** raid!\n\n" \
                            "React with ✅ to join the raid!\n\n" \
                            f"**Max Players: {raid_info['max_players']}**\n\n" \
                            "**Participants:**\n" + participant_list
        self.bot.loop.create_task(raid_info["message"].edit(embed=embed))

    def log_active_raids(self): # Debug Log
        
        logger.info("📌 Current Active Raids:")
        if not self.active_raids:
            logger.info("  - No active raids")
            return
            
        for msg_id, data in self.active_raids.items():
            player_names = ", ".join([player.name for player in data['players']])
            logger.info(f"  - Raid: {data['raid']} | Leader: {data['leader'].name} | Players ({len(data['players'])}): {player_names}")

    async def close_raid_after_timeout(self, message_id, timeout):
        await discord.utils.sleep_until(discord.utils.utcnow() + timedelta(seconds=timeout))

        raid_info = self.active_raids.get(message_id)
        if not raid_info:
            return  # Raid already closed or doesn't exist

        await raid_info["message"].clear_reactions()
        participant_list = "\n".join([f"✅ {p.mention}" for p in raid_info["players"]])
        # Finalize the raid
        embed = raid_info["message"].embeds[0]
        embed.title = f"🔒 Raid {raid_info['raid']} Closed!"
        embed.description = "\n\n🛑 Raid registration is now closed." \
        f"\n**Missing Players: {raid_info['max_players'] - len(raid_info['players'])}**\n\n" \
        "**Participants:**\n" + participant_list
        embed.color = discord.Color.red()
        embed.remove_footer()
        embed.set_footer(text="Raid closed. Leader opened the lobby.")
        await raid_info["message"].edit(embed=embed, view=None)  # Remove the reaction options

        # Log the closure
        logger.info(f"⏰ Raid {raid_info['raid']} closed automatically (Message ID: {message_id})")
        self.log_active_raids()

        # Remove from active_raids
        self.active_raids.pop(message_id, None)

async def setup(bot):
    await bot.add_cog(RaidCommand(bot))