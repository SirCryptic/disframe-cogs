import discord
from discord.ext import commands
import config
from config import BOT_PREFIX
import random
import datetime
from discord.ui import Button, View, Select
import os
import json
import base64
import asyncio
from PIL import Image, ImageDraw, ImageFont
import io

class SpaceMiner(commands.Cog):
    """An expansive guild-only space mining adventure with planets, crew, and trading."""

    def __init__(self, bot):
        self.bot = bot
        self.data_dir = os.path.join("data", "games", "spaceminer")
        self.image_path = os.path.join("assets", "images", "spaceminer_base.jpg")
        self.font_path = os.path.join("assets", "fonts", "impact.ttf")
        os.makedirs(self.data_dir, exist_ok=True)
        self.shop_items = {
            "Drill Bit": {"cost": {"credits": 100}, "effect": "mine_boost", "value": 0.1, "sell_price": 75, "desc": "Boosts credit yield by 10%"},
            "Fuel Tank": {"cost": {"credits": 150}, "effect": "fuel_efficiency", "value": 5, "sell_price": 100, "desc": "Increases fuel per mine by 5"},
            "Cargo Hold": {"cost": {"credits": 200}, "effect": "cargo_capacity", "value": 10, "sell_price": 150, "desc": "Increases ore capacity by 10"},
            "Quantum Scanner": {"cost": {"credits": 500, "ore": 50}, "effect": "mine_boost", "value": 0.25, "sell_price": 375, "desc": "Boosts credit yield by 25%"},
            "Shield Generator": {"cost": {"credits": 300, "ore": 20}, "effect": "shield", "value": 20, "sell_price": 225, "desc": "Adds 20 shield strength"},
            "Plasma Cutter": {"cost": {"credits": 800, "ore": 100}, "effect": "mine_boost", "value": 0.5, "sell_price": 600, "desc": "Boosts credit yield by 50%"},
            "Hyperdrive": {"cost": {"credits": 1000, "fuel": 50}, "effect": "speed", "value": 10, "sell_price": 750, "desc": "Increases mining speed by 10%"},
            "Miner Bot": {"cost": {"credits": 400}, "effect": "mine_bonus", "value": 5, "sell_price": 300, "desc": "Adds 5 credits per mine"},
            "Engineer": {"cost": {"credits": 600, "ore": 30}, "effect": "durability_regen", "value": 2, "sell_price": 450, "desc": "Regens 2 durability per mine"},
            "Navigator": {"cost": {"credits": 700, "fuel": 20}, "effect": "mission_boost", "value": 0.1, "sell_price": 525, "desc": "Increases mission success by 10%"},
            "Quantum Stabilizer": {"cost": {"credits": 900, "ore": 80}, "effect": "mission_risk", "value": -0.15, "sell_price": 675, "desc": "Reduces mission risk by 15%"},
            "Ion Thruster": {"cost": {"credits": 1200, "fuel": 60}, "effect": "speed_fuel", "value": {"speed": 15, "fuel": 5}, "sell_price": 900, "desc": "Boosts speed by 15%, +5 fuel per mine"},
            "Thermal Plating": {"cost": {"credits": 1000, "ore": 100}, "effect": "durability_protect", "value": 3, "sell_price": 750, "desc": "Reduces durability damage by 3 per mine"}
        }
        self.craftable_items = {
            "Repair Kit": {"cost": {"ore": 30, "fuel": 10}, "effect": "repair", "value": 50, "desc": "Restores 50 durability"},
            "Ore Refiner": {"cost": {"ore": 50, "credits": 200}, "effect": "ore_boost", "value": 15, "desc": "Increases ore per mine by 15"},
            "Distress Signal": {"cost": {"credits": 100, "ore": 50, "fuel": 25}, "effect": "signal", "value": 28, "desc": "Sends a signal into the void..."},
            "Shield Capacitor": {"cost": {"credits": 250, "ore": 40}, "effect": "shield_boost", "value": 30, "desc": "Restores 30 shield points"},
            "Fuel Cell": {"cost": {"credits": 300, "ore": 20, "fuel": 10}, "effect": "fuel_boost", "value": 50, "desc": "Adds 50 fuel (30-min cooldown)"}
        }
        self.planets = {
            "Asteria": {"credits": (15, 60), "ore": (10, 25), "fuel": (5, 15), "risk": 0.2, "travel_cost": 10, "desc": "Rich in credits, moderate risk"},
            "Ferron": {"credits": (5, 30), "ore": (15, 40), "fuel": (5, 10), "risk": 0.1, "travel_cost": 5, "desc": "Ore-heavy, low risk"},
            "Vortex": {"credits": (10, 50), "ore": (5, 20), "fuel": (10, 30), "risk": 0.3, "travel_cost": 15, "desc": "Fuel-rich, high risk"},
            "Cryptara": {"credits": (10, 40), "ore": (10, 30), "fuel": (5, 20), "risk": 0.15, "travel_cost": 10, "desc": "Balanced, whispers of lost signals..."},
            "Nebulon": {"credits": (20, 80), "ore": (15, 35), "fuel": (10, 25), "risk": 0.4, "travel_cost": 20, "desc": "High rewards, extreme risk, rare artifacts"},
            "Zentara": {"credits": (15, 50), "ore": (10, 30), "fuel": (10, 20), "risk": 0.25, "travel_cost": 15, "desc": "Balanced, potential shield energy surges"},
            "Drakon": {"credits": (10, 40), "ore": (20, 50), "fuel": (5, 15), "risk": 0.35, "travel_cost": 20, "desc": "Ore-rich, fiery surface damages hull"}
        }
        self.missions = [
            {"name": "Pirate Ambush", "chance": 0.15, "desc": "Pirates attack! Lose 20% credits or 15 durability.", "credits_loss": 0.2, "durability_loss": 15},
            {"name": "Rare Asteroid", "chance": 0.1, "desc": "Found a rare asteroid! +150 credits, +75 ore.", "credits_gain": 150, "ore_gain": 75},
            {"name": "Fuel Leak", "chance": 0.2, "desc": "Fuel leak detected! Lose 15 fuel.", "fuel_loss": 15},
            {"name": "Meteor Shower", "chance": 0.1, "desc": "Shields hold! -10 shield or 20 durability.", "shield_loss": 10, "durability_loss": 20},
            {"name": "Trader Encounter", "chance": 0.05, "desc": "A trader offers a deal! +100 credits.", "credits_gain": 100},
            {"name": "Artifact Discovery", "chance": 0.03, "desc": "Unearthed an ancient relic! +500 credits.", "credits_gain": 500},
            {"name": "Cosmic Storm", "chance": 0.08, "desc": "Caught in a storm! Lose 20 shield or gain 50 fuel.", "shield_loss": 20, "fuel_gain": 50},
            {"name": "Solar Flare", "chance": 0.07, "desc": "Solar flare hits! Lose 10 durability or gain 200 credits.", "durability_loss": 10, "credits_gain": 200}
        ]
        self.achievements = {
            "First Haul": {"condition": lambda data: data["credits"] >= 100, "title": "Rookie Miner"},
            "Ore Hoarder": {"condition": lambda data: data["ore"] >= 500, "title": "Ore Baron"},
            "Fuel Master": {"condition": lambda data: data["fuel"] >= 300, "title": "Fuel Tycoon"},
            "Veteran": {"condition": lambda data: len(data["upgrades"]) >= 5, "title": "Asteroid Ace"},
            "Planet Hopper": {"condition": lambda data: len(data.get("visited_planets", [])) >= 3, "title": "Galactic Explorer"},
            "Nebulon Survivor": {"condition": lambda data: "Nebulon" in data.get("visited_planets", []) and data["credits"] >= 1000, "title": "Void Conqueror"},
            "Shieldmaster": {"condition": lambda data: data["shield"] >= 100, "title": "Shieldmaster"},
            "Fuel Runner": {"condition": lambda data: len(data.get("visited_planets", [])) >= len(self.planets) and data["fuel"] >= 500, "title": "Fuel Runner"}
        }
        self.easter_egg_encoded = "Q3VzdG9tIGdhbWUgYnkgU2lyQ3J5cHRpYyA8MyByandseTRldmUgLSBHaXRIdWI6IGdpdGh1Yi5jb20vU2lyQ3J5cHRpYyAtIEJ1aWx0IHdpdGggRGlzRnJhbWVzIENvcmUgLSA0MiBpcyB0aGUgYW5zd2VyIQ=="
        self.explorer_role_name = "🚀Galactic Explorer"

    def get_guild_data(self, guild_id):
        guild_file = os.path.join(self.data_dir, f"{guild_id}.json")
        try:
            if os.path.exists(guild_file):
                with open(guild_file, "r") as f:
                    return json.load(f)
            else:
                data = {}
                self.save_guild_data(guild_id, data)
                return data
        except Exception:
            return {}

    def save_guild_data(self, guild_id, data):
        guild_file = os.path.join(self.data_dir, f"{guild_id}.json")
        try:
            with open(guild_file, "w") as f:
                json.dump(data, f)
        except Exception:
            pass

    def migrate_user_data(self, user_data):
        default_data = {
            "credits": 0,
            "ore": 0,
            "fuel": 0,
            "durability": 100,
            "shield": 0,
            "speed": 100,
            "upgrades": [],
            "crafted": [],
            "last_mine": 0,
            "last_fuel_cell": 0,
            "last_attack": 0,
            "current_planet": "Asteria",
            "visited_planets": ["Asteria"],
            "achievements": [],
            "total_mines": 0,
            "successful_attacks": 0
        }
        for key, value in default_data.items():
            if key not in user_data:
                user_data[key] = value
        return user_data

    def create_embed(self, title, description, color=discord.Color.blue(), image_bytes=None):
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.datetime.utcnow()
        )
        if image_bytes:
            file = discord.File(image_bytes, filename="image.png")
            embed.set_image(url="attachment://image.png")
            return embed, file
        embed.set_footer(
            text=f"{config.BOT_NAME} v{config.BOT_VERSION} - Space Miner",
            icon_url=self.bot.user.avatar.url if self.bot.user.avatar else None
        )
        return embed, None

    async def generate_image(self, message):
        try:
            img = Image.open(self.image_path).convert("RGBA") if os.path.exists(self.image_path) else Image.new("RGBA", (600, 400), (50, 50, 100, 255))
            draw = ImageDraw.Draw(img)
            font_size = 60
            font = ImageFont.truetype(self.font_path, font_size) if os.path.exists(self.font_path) else ImageFont.load_default()

            text_color = (255, 255, 255)
            outline_color = (0, 0, 0)
            lines = message.split('\n')
            total_height = len(lines) * font_size
            start_y = (img.height - total_height) // 2

            for i, line in enumerate(lines):
                text_bbox = draw.textbbox((0, 0), line, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_x = (img.width - text_width) // 2
                text_y = start_y + i * font_size

                for dx, dy in [(-2, -2), (2, 2), (-2, 2), (2, -2)]:
                    draw.text((text_x + dx, text_y + dy), line, font=font, fill=outline_color)
                draw.text((text_x, text_y), line, font=font, fill=text_color)

            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            return buffer
        except Exception:
            return None

    async def assign_explorer_role(self, member):
        guild = member.guild
        user_id = str(member.id)
        guild_id = str(guild.id)
        guild_data = self.get_guild_data(guild_id)
        
        if user_id not in guild_data or len(guild_data[user_id].get("achievements", [])) != len(self.achievements):
            return

        role = discord.utils.get(guild.roles, name=self.explorer_role_name)
        if role and role not in member.roles:
            try:
                await member.add_roles(role)
            except discord.errors.Forbidden:
                pass
        elif not role and guild.me.guild_permissions.manage_roles:
            role = await guild.create_role(
                name=self.explorer_role_name,
                color=discord.Color.purple(),
                reason="Space Miner Galactic Explorer achievement"
            )
            await member.add_roles(role)

    def check_achievements(self, user_data):
        unlocked = []
        for ach_name, ach_data in self.achievements.items():
            if ach_name not in user_data.get("achievements", []) and ach_data["condition"](user_data):
                unlocked.append(ach_name)
                user_data.setdefault("achievements", []).append(ach_name)
        return unlocked

    @commands.command(name="spacehelp")
    async def space_help(self, ctx):
        if not ctx.guild:
            embed, _ = self.create_embed("❌ Guild-Only Game", f"{ctx.author.mention}, Space Miner is guild-only!")
            await ctx.send(embed=embed, delete_after=5)
            return

        help_text = (
            "🌌 **Space Miner Commands** 🌌\n"
            f"- `{BOT_PREFIX}space` - Launch your mining rig.\n"
            f"- `{BOT_PREFIX}spacebalance` - Check ship status.\n"
            f"- `{BOT_PREFIX}spaceleader` - Top miners leaderboard.\n"
            f"- `{BOT_PREFIX}spacesetup` - Setup Galactic Explorer role.\n"
            f"- `{BOT_PREFIX}spacehelp` - This menu.\n\n"
            "🚀 **How to Play** 🚀\n"
            "- Mine planets for credits, ore, and fuel—watch for missions!\n"
            "- Travel (costs fuel), upgrade your ship, craft items, trade, or attack!\n"
            "- Earn all achievements for 🚀Galactic Explorer role!"
        )
        embed, _ = self.create_embed("Space Miner Help", help_text)
        await ctx.send(embed=embed)

    @commands.command(name="spacesetup")
    async def space_setup(self, ctx):
        if not ctx.guild:
            embed, _ = self.create_embed("❌ Guild-Only Command", f"{ctx.author.mention}, run this in a server!")
            await ctx.send(embed=embed, delete_after=5)
            return

        if not ctx.author.guild_permissions.manage_roles:
            embed, _ = self.create_embed("❌ No Permission", f"{ctx.author.mention}, you need 'Manage Roles' permission!")
            await ctx.send(embed=embed, delete_after=5)
            return

        if not ctx.guild.me.guild_permissions.manage_roles:
            embed, _ = self.create_embed("❌ Bot Lacks Permission", f"I need 'Manage Roles' permission to create '{self.explorer_role_name}'!")
            await ctx.send(embed=embed, delete_after=5)
            return

        role = discord.utils.get(ctx.guild.roles, name=self.explorer_role_name)
        if role:
            embed, _ = self.create_embed("✅ Role Exists", f"'{self.explorer_role_name}' already exists!")
            await ctx.send(embed=embed, delete_after=5)
            return

        await ctx.guild.create_role(
            name=self.explorer_role_name,
            color=discord.Color.purple(),
            reason=f"Setup by {ctx.author}"
        )
        embed, _ = self.create_embed("✅ Role Created", f"Created '{self.explorer_role_name}'!")
        await ctx.send(embed=embed, delete_after=5)

    @commands.command(name="spacebalance")
    async def space_balance(self, ctx):
        if not ctx.guild:
            embed, _ = self.create_embed("❌ Guild-Only Game", f"{ctx.author.mention}, Space Miner is guild-only!")
            await ctx.send(embed=embed, delete_after=5)
            return

        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        guild_data = self.get_guild_data(guild_id)
        user_data = guild_data.setdefault(user_id, self.migrate_user_data({}))
        upgrades = ", ".join(user_data["upgrades"]) if user_data["upgrades"] else "None"
        achievements = ", ".join([self.achievements[ach]["title"] for ach in user_data["achievements"]]) if user_data["achievements"] else "None"
        balance_text = (
            f"🪐 **Ship Status** 🪐\n"
            f"Location: {user_data['current_planet']}\n"
            f"Credits: {user_data['credits']}\n"
            f"Ore: {user_data['ore']}\n"
            f"Fuel: {user_data['fuel']}\n"
            f"Durability: {user_data['durability']}/100\n"
            f"Shield: {user_data['shield']}/100\n"
            f"Speed: {user_data['speed']}%\n"
            f"Upgrades: {upgrades}\n"
            f"Achievements: {achievements}\n"
            f"Total Mines: {user_data['total_mines']}\n"
            f"Successful Attacks: {user_data['successful_attacks']}"
        )
        embed, _ = self.create_embed(f"{ctx.author.name}'s Status", balance_text, discord.Color.gold())
        await ctx.send(embed=embed)

    @commands.command(name="spaceleader")
    async def space_leaderboard(self, ctx):
        if not ctx.guild:
            embed, _ = self.create_embed("❌ Guild-Only Game", f"{ctx.author.mention}, Space Miner is guild-only!")
            await ctx.send(embed=embed, delete_after=5)
            return

        guild_id = str(ctx.guild.id)
        guild_data = self.get_guild_data(guild_id)
        if not guild_data:
            embed, _ = self.create_embed(f"🌟 Leaderboard - {ctx.guild.name}", "No miners yet!")
            await ctx.send(embed=embed)
            return

        class LeaderboardView(View):
            def __init__(self, cog, guild, guild_data, page=0):
                super().__init__(timeout=60)
                self.cog = cog
                self.guild = guild
                self.guild_data = guild_data
                self.page = page
                self.per_page = 5
                self.message = None
                self.add_items()

            def get_sorted_players(self):
                return sorted(self.guild_data.items(), key=lambda x: x[1]["credits"] + x[1]["ore"] + x[1]["fuel"], reverse=True)

            def format_leaderboard(self):
                sorted_players = self.get_sorted_players()
                total_pages = (len(sorted_players) + self.per_page - 1) // self.per_page
                start = self.page * self.per_page
                end = min(start + self.per_page, len(sorted_players))
                leaderboard_text = "🌌 Rank | Miner         | Cr   | Ore | Fuel | Hauls\n" + "-"*40 + "\n"
                for i, (uid, data) in enumerate(sorted_players[start:end], start=start):
                    member = self.guild.get_member(int(uid))
                    name = member.display_name if member else f"Unknown ({uid})"
                    total_hauls = data["credits"] + data["ore"] + data["fuel"]
                    leaderboard_text += f"{i+1:<5} | {name:<13} | {data['credits']:<4} | {data['ore']:<3} | {data['fuel']:<4} | {total_hauls:<5}\n"
                leaderboard_text += f"\nPage {self.page + 1}/{total_pages}"
                return leaderboard_text

            def add_items(self):
                self.clear_items()
                sorted_players = self.get_sorted_players()
                total_pages = (len(sorted_players) + self.per_page - 1) // self.per_page
                self.add_item(Button(label="◀", style=discord.ButtonStyle.grey, custom_id="prev_page", disabled=self.page == 0))
                self.add_item(Button(label="▶", style=discord.ButtonStyle.grey, custom_id="next_page", disabled=self.page >= total_pages - 1))

            async def update_view(self):
                embed, _ = self.cog.create_embed(f"🌟 Leaderboard - {self.guild.name}", self.format_leaderboard())
                self.add_items()
                await self.message.edit(embed=embed, view=self)

            @discord.ui.button(custom_id="prev_page")
            async def prev_page(self, interaction: discord.Interaction, button: Button):
                self.page -= 1
                await self.update_view()
                await interaction.response.defer()

            @discord.ui.button(custom_id="next_page")
            async def next_page(self, interaction: discord.Interaction, button: Button):
                self.page += 1
                await self.update_view()
                await interaction.response.defer()

        view = LeaderboardView(self, ctx.guild, guild_data)
        embed, _ = self.create_embed(f"🌟 Leaderboard - {ctx.guild.name}", view.format_leaderboard())
        message = await ctx.send(embed=embed, view=view)
        view.message = message

    @commands.command(name="space")
    async def space_game(self, ctx):
        if not ctx.guild:
            embed, _ = self.create_embed("❌ Guild-Only Game", f"{ctx.author.mention}, Space Miner is guild-only!")
            await ctx.send(embed=embed, delete_after=5)
            return

        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        guild_data = self.get_guild_data(guild_id)
        user_data = guild_data.setdefault(user_id, self.migrate_user_data({}))
        self.save_guild_data(guild_id, guild_data)
        welcome_message = "Welcome back, captain!" if user_data["credits"] > 0 else "Welcome aboard, rookie!"

        class SpaceMinerView(View):
            def __init__(self, cog, user, guild_id):
                super().__init__(timeout=None)
                self.cog = cog
                self.user = user
                self.guild_id = guild_id
                self.message = None
                self.shop_message = None
                self.shop_open = False

            async def interaction_check(self, interaction: discord.Interaction) -> bool:
                if interaction.user.id != self.user.id:
                    await interaction.response.send_message("This rig’s not yours!", ephemeral=True)
                    return False
                return True

            async def notify_achievements(self, new_unlocks):
                if new_unlocks:
                    ach_text = "\n".join([f"🏆 **{self.cog.achievements[ach]['title']}**" for ach in new_unlocks])
                    embed, _ = self.cog.create_embed("Achievement Unlocked!", f"{self.user.mention}\n{ach_text}")
                    msg = await self.message.channel.send(embed=embed, ephemeral=True)
                    if msg:
                        await asyncio.sleep(6)
                        await msg.delete()

            @discord.ui.button(label="Mine", style=discord.ButtonStyle.green, emoji="⛏️")
            async def mine_button(self, interaction: discord.Interaction, button: Button):
                user_id = str(self.user.id)
                guild_data = self.cog.get_guild_data(self.guild_id)
                now = datetime.datetime.utcnow().timestamp()
                last_mine = guild_data[user_id]["last_mine"]
                base_cooldown = 600
                speed_modifier = guild_data[user_id]["speed"] / 100
                cooldown = base_cooldown / speed_modifier
                if now - last_mine < cooldown:
                    remaining = int(cooldown - (now - last_mine))
                    minutes = remaining // 60
                    await interaction.response.send_message(f"Hyperdrive charging! Mine in {minutes}m!", ephemeral=True)
                    return

                if guild_data[user_id]["durability"] <= 0:
                    await interaction.response.send_message("Ship’s wrecked! Craft a Repair Kit.", ephemeral=True)
                    return

                planet = guild_data[user_id]["current_planet"]
                planet_data = self.cog.planets[planet]
                base_credits = random.randint(*planet_data["credits"])
                base_ore = random.randint(*planet_data["ore"])
                base_fuel = random.randint(*planet_data["fuel"])
                credits_boost = 1.0
                ore_boost = 0
                fuel_boost = 0
                mission_chance_boost = 0
                mission_risk_reduction = 0
                durability_protection = 0

                for upgrade in guild_data[user_id]["upgrades"]:
                    effect = self.cog.shop_items[upgrade]["effect"]
                    if effect == "mine_boost":
                        credits_boost += self.cog.shop_items[upgrade]["value"]
                    elif effect == "cargo_capacity":
                        ore_boost += self.cog.shop_items[upgrade]["value"]
                    elif effect == "fuel_efficiency":
                        fuel_boost += self.cog.shop_items[upgrade]["value"]
                    elif effect == "shield":
                        guild_data[user_id]["shield"] = min(100, guild_data[user_id]["shield"] + self.cog.shop_items[upgrade]["value"])
                    elif effect == "speed":
                        guild_data[user_id]["speed"] = min(150, guild_data[user_id]["speed"] + self.cog.shop_items[upgrade]["value"])
                    elif effect == "speed_fuel":
                        guild_data[user_id]["speed"] = min(150, guild_data[user_id]["speed"] + self.cog.shop_items[upgrade]["value"]["speed"])
                        fuel_boost += self.cog.shop_items[upgrade]["value"]["fuel"]
                    elif effect == "mine_bonus":
                        base_credits += self.cog.shop_items[upgrade]["value"]
                    elif effect == "durability_regen":
                        guild_data[user_id]["durability"] = min(100, guild_data[user_id]["durability"] + self.cog.shop_items[upgrade]["value"])
                    elif effect == "mission_boost":
                        mission_chance_boost += self.cog.shop_items[upgrade]["value"]
                    elif effect == "mission_risk":
                        mission_risk_reduction += self.cog.shop_items[upgrade]["value"]
                    elif effect == "durability_protect":
                        durability_protection += self.cog.shop_items[upgrade]["value"]
                    elif effect == "ore_boost":
                        ore_boost += self.cog.craftable_items[upgrade]["value"]

                credits = int(base_credits * credits_boost)
                ore = base_ore + ore_boost
                fuel = base_fuel + fuel_boost
                base_durability_loss = 5 if planet != "Drakon" else 10
                durability_loss = max(1, base_durability_loss - durability_protection)
                mission_log = ""

                for mission in self.cog.missions:
                    adjusted_risk = max(0, planet_data["risk"] + mission_risk_reduction)
                    if random.random() < (mission["chance"] + mission_chance_boost) * adjusted_risk:
                        mission_log += f"\n**{mission['name']}**: {mission['desc']}"
                        if "credits_loss" in mission:
                            credits_loss = int(guild_data[user_id]["credits"] * mission["credits_loss"])
                            guild_data[user_id]["credits"] = max(0, guild_data[user_id]["credits"] - credits_loss)
                            credits -= credits_loss
                        if "durability_loss" in mission:
                            if mission["name"] == "Solar Flare" and random.random() < 0.5:
                                credits += mission["credits_gain"]
                            elif guild_data[user_id]["shield"] > 0 and "shield_loss" in mission:
                                guild_data[user_id]["shield"] = max(0, guild_data[user_id]["shield"] - mission.get("shield_loss", 0))
                            else:
                                durability_loss += mission["durability_loss"] - durability_protection
                        if "credits_gain" in mission and mission["name"] != "Solar Flare":
                            credits += mission["credits_gain"]
                        if "ore_gain" in mission:
                            ore += mission["ore_gain"]
                        if "fuel_loss" in mission:
                            fuel = max(0, fuel - mission["fuel_loss"])
                        if "fuel_gain" in mission:
                            if random.random() < 0.5:
                                fuel += mission["fuel_gain"]
                            else:
                                guild_data[user_id]["shield"] = max(0, guild_data[user_id]["shield"] - mission["shield_loss"])
                        break

                guild_data[user_id]["credits"] += credits
                guild_data[user_id]["ore"] += ore
                guild_data[user_id]["fuel"] += fuel
                guild_data[user_id]["durability"] = max(0, guild_data[user_id]["durability"] - durability_loss)
                guild_data[user_id]["last_mine"] = now
                guild_data[user_id]["total_mines"] += 1
                new_unlocks = self.cog.check_achievements(guild_data[user_id])
                self.cog.save_guild_data(self.guild_id, guild_data)

                result = (
                    f"🌠 Mining on {planet}\n"
                    f"Credits: +{credits}\n"
                    f"Ore: +{ore}\n"
                    f"Fuel: +{fuel}\n"
                    f"Durability: -{durability_loss} (Now {guild_data[user_id]['durability']})\n"
                    f"Shield: {guild_data[user_id]['shield']}"
                )
                if mission_log:
                    result += mission_log
                image = await self.cog.generate_image(f"Success!\n+{credits} Cr, +{ore} Ore, +{fuel} Fuel")
                embed, file = self.cog.create_embed("Mining Report", result, image_bytes=image)
                msg = await interaction.response.send_message(embed=embed, file=file, ephemeral=True)
                if msg:
                    await asyncio.sleep(6)
                    await msg.delete()
                await self.notify_achievements(new_unlocks)

            @discord.ui.button(label="Shop", style=discord.ButtonStyle.blurple, emoji="🛒")
            async def shop_button(self, interaction: discord.Interaction, button: Button):
                if self.shop_open:
                    await interaction.response.send_message("Shop’s already open!", ephemeral=True)
                    return

                self.shop_open = True
                for item in self.children:
                    item.disabled = True
                await self.message.edit(view=self)

                guild_data = self.cog.get_guild_data(self.guild_id)
                shop_list = "\n".join([f"{item}: {self.cog.shop_items[item]['cost'].get('credits', 0)} cr{' + ' + str(self.cog.shop_items[item]['cost']['ore']) + ' ore' if 'ore' in self.cog.shop_items[item]['cost'] else ''}{' + ' + str(self.cog.shop_items[item]['cost']['fuel']) + ' fuel' if 'fuel' in self.cog.shop_items[item]['cost'] else ''} - {self.cog.shop_items[item]['desc']}" for item in self.cog.shop_items])
                embed, _ = self.cog.create_embed("Space Miner Shop", f"Upgrades & Crew:\n{shop_list}\n\nSelect to buy/sell!")

                class ShopSelect(Select):
                    def __init__(self, cog, user, guild_id, parent_view):
                        options = [discord.SelectOption(label=item, description=cog.shop_items[item]["desc"]) for item in cog.shop_items]
                        super().__init__(placeholder="Buy an item", options=options)
                        self.cog = cog
                        self.user = user
                        self.guild_id = guild_id
                        self.parent_view = parent_view

                    async def callback(self, interaction: discord.Interaction):
                        await interaction.response.send_message("Processing...", ephemeral=True)
                        item = self.values[0]
                        cost = self.cog.shop_items[item]["cost"]
                        user_id = str(self.user.id)
                        guild_data = self.cog.get_guild_data(self.guild_id)

                        if guild_data[user_id]["credits"] < cost.get("credits", 0) or guild_data[user_id]["ore"] < cost.get("ore", 0) or guild_data[user_id]["fuel"] < cost.get("fuel", 0):
                            await interaction.followup.send(f"Not enough resources for {item}!", ephemeral=True)
                            return
                        if item in guild_data[user_id]["upgrades"]:
                            await interaction.followup.send(f"You already own {item}!", ephemeral=True)
                            return

                        guild_data[user_id]["credits"] -= cost.get("credits", 0)
                        guild_data[user_id]["ore"] -= cost.get("ore", 0)
                        guild_data[user_id]["fuel"] -= cost.get("fuel", 0)
                        guild_data[user_id]["upgrades"].append(item)
                        self.cog.save_guild_data(self.guild_id, guild_data)
                        new_unlocks = self.cog.check_achievements(guild_data[user_id])

                        image = await self.cog.generate_image(f"Success!\nBought {item}!")
                        embed, file = self.cog.create_embed("Purchase Complete!", f"{self.user.mention}, acquired {item}!\nEffect: {self.cog.shop_items[item]['desc']}", image_bytes=image)
                        msg = await interaction.followup.send(embed=embed, file=file, ephemeral=True)
                        if msg:
                            await asyncio.sleep(6)
                            await msg.delete()
                        await self.parent_view.notify_achievements(new_unlocks)

                class SellSelect(Select):
                    def __init__(self, cog, user, guild_id, parent_view):
                        guild_data = cog.get_guild_data(guild_id)
                        user_id = str(user.id)
                        options = [discord.SelectOption(label=item, description=f"Sell for {cog.shop_items[item]['sell_price']} credits") for item in guild_data[user_id]["upgrades"]] if guild_data[user_id]["upgrades"] else [discord.SelectOption(label="No items", description="Nothing to sell")]
                        super().__init__(placeholder="Sell an item", options=options)
                        self.cog = cog
                        self.user = user
                        self.guild_id = guild_id
                        self.parent_view = parent_view

                    async def callback(self, interaction: discord.Interaction):
                        await interaction.response.defer()
                        item = self.values[0]
                        if item == "No items":
                            await interaction.followup.send("No items to sell!", ephemeral=True)
                            return
                        user_id = str(self.user.id)
                        guild_data = self.cog.get_guild_data(self.guild_id)
                        sell_price = self.cog.shop_items[item]["sell_price"]
                        guild_data[user_id]["credits"] += sell_price
                        guild_data[user_id]["upgrades"].remove(item)
                        self.cog.save_guild_data(self.guild_id, guild_data)
                        image = await self.cog.generate_image(f"Success!\nSold {item}!")
                        embed, file = self.cog.create_embed("Sale Complete!", f"{self.user.mention}, sold {item} for {sell_price} credits!", image_bytes=image)
                        msg = await interaction.followup.send(embed=embed, file=file, ephemeral=True)
                        if msg:
                            await asyncio.sleep(6)
                            await msg.delete()

                shop_view = View()
                shop_view.add_item(ShopSelect(self.cog, self.user, self.guild_id, self))
                shop_view.add_item(SellSelect(self.cog, self.user, self.guild_id, self))
                shop_view.add_item(Button(label="Close Shop", style=discord.ButtonStyle.red, emoji="❌", custom_id="close_shop"))

                async def close_shop_callback(interaction: discord.Interaction):
                    if interaction.user.id != self.user.id:
                        await interaction.response.send_message("Only the captain can close!", ephemeral=True)
                        return
                    self.shop_open = False
                    for item in self.children:
                        item.disabled = False
                    await self.message.edit(view=self)
                    if self.shop_message:
                        try:
                            await self.shop_message.delete()
                        except (discord.errors.Forbidden, discord.errors.NotFound):
                            pass
                        self.shop_message = None
                    await interaction.response.send_message("Shop closed!", ephemeral=True)

                for item in shop_view.children:
                    if item.custom_id == "close_shop":
                        item.callback = close_shop_callback

                self.shop_message = await interaction.channel.send(embed=embed, view=shop_view, delete_after=60)
                await interaction.response.defer()

            @discord.ui.button(label="Craft", style=discord.ButtonStyle.blurple, emoji="🔧")
            async def craft_button(self, interaction: discord.Interaction, button: Button):
                if self.shop_open:
                    await interaction.response.send_message("Finish current task first!", ephemeral=True)
                    return

                self.shop_open = True
                for item in self.children:
                    item.disabled = True
                await self.message.edit(view=self)

                guild_data = self.cog.get_guild_data(self.guild_id)
                craft_list = "\n".join([f"{item}: {self.cog.craftable_items[item]['cost'].get('credits', 0)} cr{' + ' + str(self.cog.craftable_items[item]['cost']['ore']) + ' ore' if 'ore' in self.cog.craftable_items[item]['cost'] else ''}{' + ' + str(self.cog.craftable_items[item]['cost']['fuel']) + ' fuel' if 'fuel' in self.cog.craftable_items[item]['cost'] else ''} - {self.cog.craftable_items[item]['desc']}" for item in self.cog.craftable_items])
                embed, _ = self.cog.create_embed("Crafting Bay", f"Craftable Items:\n{craft_list}\n\nSelect to craft!")

                class CraftSelect(Select):
                    def __init__(self, cog, user, guild_id, parent_view):
                        options = [discord.SelectOption(label=item, description=cog.craftable_items[item]["desc"]) for item in cog.craftable_items]
                        super().__init__(placeholder="Choose an item", options=options)
                        self.cog = cog
                        self.user = user
                        self.guild_id = guild_id
                        self.parent_view = parent_view

                    async def callback(self, interaction: discord.Interaction):
                        await interaction.response.send_message("Crafting...", ephemeral=True)
                        item = self.values[0]
                        cost = self.cog.craftable_items[item]["cost"]
                        user_id = str(self.user.id)
                        guild_data = self.cog.get_guild_data(self.guild_id)
                        now = datetime.datetime.utcnow().timestamp()

                        if guild_data[user_id]["credits"] < cost.get("credits", 0) or guild_data[user_id]["ore"] < cost.get("ore", 0) or guild_data[user_id]["fuel"] < cost.get("fuel", 0):
                            await interaction.followup.send(f"Not enough resources for {item}!", ephemeral=True)
                            return

                        if item == "Fuel Cell":
                            last_fuel_cell = guild_data[user_id]["last_fuel_cell"]
                            cooldown = 1800
                            if now - last_fuel_cell < cooldown:
                                remaining = int(cooldown - (now - last_fuel_cell))
                                minutes = remaining // 60
                                await interaction.followup.send(f"Fuel Cell on cooldown! Ready in {minutes}m.", ephemeral=True)
                                return
                            guild_data[user_id]["last_fuel_cell"] = now

                        guild_data[user_id]["credits"] -= cost.get("credits", 0)
                        guild_data[user_id]["ore"] -= cost.get("ore", 0)
                        guild_data[user_id]["fuel"] -= cost.get("fuel", 0)
                        guild_data[user_id]["crafted"].append(item)

                        if self.cog.craftable_items[item]["effect"] == "repair":
                            guild_data[user_id]["durability"] = min(100, guild_data[user_id]["durability"] + self.cog.craftable_items[item]["value"])
                        elif self.cog.craftable_items[item]["effect"] == "ore_boost":
                            guild_data[user_id]["upgrades"].append(item)
                        elif self.cog.craftable_items[item]["effect"] == "shield_boost":
                            guild_data[user_id]["shield"] = min(100, guild_data[user_id]["shield"] + self.cog.craftable_items[item]["value"])
                        elif self.cog.craftable_items[item]["effect"] == "fuel_boost":
                            guild_data[user_id]["fuel"] += self.cog.craftable_items[item]["value"]

                        self.cog.save_guild_data(self.guild_id, guild_data)
                        new_unlocks = self.cog.check_achievements(guild_data[user_id])

                        if item == "Distress Signal" and guild_data[user_id]["durability"] == 28:
                            decoded_message = base64.b64decode(self.cog.easter_egg_encoded).decode('utf-8')
                            image = await self.cog.generate_image("Signal Sent!\nEaster Egg!")
                            embed, file = self.cog.create_embed("Encrypted Transmission", f"{self.user.mention}, Distress Signal at 28 durability!\n\n{decoded_message}", image_bytes=image)
                        else:
                            image = await self.cog.generate_image(f"Success!\nCrafted {item}!")
                            embed, file = self.cog.create_embed("Crafting Complete!", f"{self.user.mention}, crafted {item}!\nEffect: {self.cog.craftable_items[item]['desc']}", image_bytes=image)
                        msg = await interaction.followup.send(embed=embed, file=file, ephemeral=True)
                        if msg:
                            await asyncio.sleep(6)
                            await msg.delete()
                        await self.parent_view.notify_achievements(new_unlocks)

                craft_view = View()
                craft_view.add_item(CraftSelect(self.cog, self.user, self.guild_id, self))
                craft_view.add_item(Button(label="Close Bay", style=discord.ButtonStyle.red, emoji="❌", custom_id="close_craft"))

                async def close_craft_callback(interaction: discord.Interaction):
                    if interaction.user.id != self.user.id:
                        await interaction.response.send_message("Only the captain can close!", ephemeral=True)
                        return
                    self.shop_open = False
                    for item in self.children:
                        item.disabled = False
                    await self.message.edit(view=self)
                    if self.shop_message:
                        try:
                            await self.shop_message.delete()
                        except (discord.errors.Forbidden, discord.errors.NotFound):
                            pass
                        self.shop_message = None
                    await interaction.response.send_message("Bay closed!", ephemeral=True)

                for item in craft_view.children:
                    if item.custom_id == "close_craft":
                        item.callback = close_craft_callback

                self.shop_message = await interaction.channel.send(embed=embed, view=craft_view, delete_after=60)
                await interaction.response.defer()

            @discord.ui.button(label="Travel", style=discord.ButtonStyle.grey, emoji="🌍")
            async def travel_button(self, interaction: discord.Interaction, button: Button):
                if self.shop_open:
                    await interaction.response.send_message("Finish current task first!", ephemeral=True)
                    return

                self.shop_open = True
                for item in self.children:
                    item.disabled = True
                await self.message.edit(view=self)

                guild_data = self.cog.get_guild_data(self.guild_id)
                user_id = str(self.user.id)
                current_planet = guild_data[user_id]["current_planet"]
                planet_list = "\n".join([f"{planet}: {self.cog.planets[planet]['desc']} (Fuel Cost: {self.cog.planets[planet]['travel_cost']})" for planet in self.cog.planets if planet != current_planet])
                embed, _ = self.cog.create_embed("Star Chart", f"Current: {current_planet}\nFuel: {guild_data[user_id]['fuel']}\n\nDestinations:\n{planet_list}\n\nSelect a planet!")

                class PlanetSelect(Select):
                    def __init__(self, cog, user, guild_id, parent_view):
                        options = [discord.SelectOption(label=planet, description=f"{cog.planets[planet]['desc']} (Fuel Cost: {cog.planets[planet]['travel_cost']})") for planet in cog.planets if planet != guild_data[str(user.id)]["current_planet"]]
                        super().__init__(placeholder="Choose a planet", options=options)
                        self.cog = cog
                        self.user = user
                        self.guild_id = guild_id
                        self.parent_view = parent_view

                    async def callback(self, interaction: discord.Interaction):
                        planet = self.values[0]
                        user_id = str(self.user.id)
                        guild_data = self.cog.get_guild_data(self.guild_id)
                        travel_cost = self.cog.planets[planet]["travel_cost"]

                        if guild_data[user_id]["fuel"] < travel_cost:
                            await interaction.response.send_message(f"Not enough fuel! Need {travel_cost}, have {guild_data[user_id]['fuel']}.", ephemeral=True)
                            return

                        guild_data[user_id]["fuel"] -= travel_cost
                        guild_data[user_id]["current_planet"] = planet
                        if planet not in guild_data[user_id]["visited_planets"]:
                            guild_data[user_id]["visited_planets"].append(planet)
                            new_unlocks = self.cog.check_achievements(guild_data[user_id])
                            await self.parent_view.notify_achievements(new_unlocks)
                        self.cog.save_guild_data(self.guild_id, guild_data)

                        image = await self.cog.generate_image(f"Arrived!\n{planet}")
                        embed, file = self.cog.create_embed("Planet Reached!", f"{self.user.mention}, arrived at {planet}!\nDesc: {self.cog.planets[planet]['desc']}\nFuel: {guild_data[user_id]['fuel']}", image_bytes=image)
                        msg = await interaction.response.send_message(embed=embed, file=file, ephemeral=True)
                        if msg:
                            await asyncio.sleep(6)
                            await msg.delete()

                travel_view = View()
                travel_view.add_item(PlanetSelect(self.cog, self.user, self.guild_id, self))
                travel_view.add_item(Button(label="Cancel Travel", style=discord.ButtonStyle.red, emoji="❌", custom_id="close_travel"))

                async def close_travel_callback(interaction: discord.Interaction):
                    if interaction.user.id != self.user.id:
                        await interaction.response.send_message("Only the captain can cancel!", ephemeral=True)
                        return
                    self.shop_open = False
                    for item in self.children:
                        item.disabled = False
                    await self.message.edit(view=self)
                    if self.shop_message:
                        try:
                            await self.shop_message.delete()
                        except (discord.errors.Forbidden, discord.errors.NotFound):
                            pass
                        self.shop_message = None
                    await interaction.response.send_message("Travel canceled!", ephemeral=True)

                for item in travel_view.children:
                    if item.custom_id == "close_travel":
                        item.callback = close_travel_callback

                self.shop_message = await interaction.channel.send(embed=embed, view=travel_view, delete_after=60)
                await interaction.response.defer()

            @discord.ui.button(label="Trade", style=discord.ButtonStyle.grey, emoji="🤝")
            async def trade_button(self, interaction: discord.Interaction, button: Button):
                if self.shop_open:
                    await interaction.response.send_message("Finish current task first!", ephemeral=True)
                    return

                self.shop_open = True
                for item in self.children:
                    item.disabled = True
                await self.message.edit(view=self)

                guild_data = self.cog.get_guild_data(self.guild_id)
                user_id = str(self.user.id)
                tradable_players = [
                    (uid, self.cog.bot.get_user(int(uid)))
                    for uid in guild_data.keys()
                    if uid != user_id and self.cog.bot.get_user(int(uid)) and not self.cog.bot.get_user(int(uid)).bot
                ]
                if not tradable_players:
                    await interaction.response.send_message("No trade partners available!", ephemeral=True)
                    self.shop_open = False
                    for item in self.children:
                        item.disabled = False
                    await self.message.edit(view=self)
                    return

                embed, _ = self.cog.create_embed("Trade Hub", f"{self.user.mention}, select a player to trade with!")

                class TradeSelect(View):
                    def __init__(self, cog, user, guild_id, parent_view, targets):
                        super().__init__(timeout=60)
                        self.cog = cog
                        self.user = user
                        self.guild_id = guild_id
                        self.parent_view = parent_view
                        self.targets = targets
                        self.message = None
                        self.add_items()

                    def add_items(self):
                        options = [discord.SelectOption(label=target.display_name, value=str(target.id)) for _, target in self.targets]
                        select = Select(placeholder="Choose a partner", options=options[:25], custom_id="trade_select")
                        select.callback = self.trade_select_callback
                        self.add_item(select)
                        cancel_button = Button(label="Cancel", style=discord.ButtonStyle.red, emoji="❌", custom_id="close_trade")
                        cancel_button.callback = self.cancel_callback
                        self.add_item(cancel_button)

                    async def interaction_check(self, interaction: discord.Interaction) -> bool:
                        if interaction.user.id != self.user.id:
                            await interaction.response.send_message("Only the initiator can select!", ephemeral=True)
                            return False
                        return True

                    async def trade_select_callback(self, interaction: discord.Interaction):
                        target_id = interaction.data["values"][0]
                        target = self.cog.bot.get_user(int(target_id))
                        guild_data = self.cog.get_guild_data(self.guild_id)

                        class TradeView(View):
                            def __init__(self, cog, initiator, target, guild_id, parent_view):
                                super().__init__(timeout=60)
                                self.cog = cog
                                self.initiator = initiator
                                self.target = target
                                self.guild_id = guild_id
                                self.parent_view = parent_view
                                self.initiator_offer = {"credits": 0, "ore": 0, "fuel": 0}
                                self.target_offer = {"credits": 0, "ore": 0, "fuel": 0}
                                self.initiator_accepted = False
                                self.target_accepted = False
                                self.message = None

                            async def interaction_check(self, interaction: discord.Interaction) -> bool:
                                if interaction.user.id not in [self.initiator.id, self.target.id]:
                                    await interaction.response.send_message("Not your trade!", ephemeral=True)
                                    return False
                                return True

                            @discord.ui.button(label="Offer Credits", style=discord.ButtonStyle.blurple)
                            async def offer_credits(self, interaction: discord.Interaction, button: Button):
                                guild_data = self.cog.get_guild_data(self.guild_id)
                                user_id = str(interaction.user.id)
                                offer = self.initiator_offer if interaction.user.id == self.initiator.id else self.target_offer
                                await interaction.response.send_message("How many credits?", ephemeral=True)
                                def check(m):
                                    return m.author.id == interaction.user.id and m.channel == interaction.channel and m.content.isdigit()
                                try:
                                    msg = await self.cog.bot.wait_for("message", check=check, timeout=30)
                                    amount = int(msg.content)
                                    if guild_data[user_id]["credits"] < amount:
                                        await interaction.followup.send(f"Only have {guild_data[user_id]['credits']} credits!", ephemeral=True)
                                    else:
                                        offer["credits"] = amount
                                        await interaction.followup.send(f"Offered {amount} credits!", ephemeral=True)
                                        await self.update_trade_message()
                                except asyncio.TimeoutError:
                                    pass

                            @discord.ui.button(label="Offer Ore", style=discord.ButtonStyle.blurple)
                            async def offer_ore(self, interaction: discord.Interaction, button: Button):
                                guild_data = self.cog.get_guild_data(self.guild_id)
                                user_id = str(interaction.user.id)
                                offer = self.initiator_offer if interaction.user.id == self.initiator.id else self.target_offer
                                await interaction.response.send_message("How much ore?", ephemeral=True)
                                def check(m):
                                    return m.author.id == interaction.user.id and m.channel == interaction.channel and m.content.isdigit()
                                try:
                                    msg = await self.cog.bot.wait_for("message", check=check, timeout=30)
                                    amount = int(msg.content)
                                    if guild_data[user_id]["ore"] < amount:
                                        await interaction.followup.send(f"Only have {guild_data[user_id]['ore']} ore!", ephemeral=True)
                                    else:
                                        offer["ore"] = amount
                                        await interaction.followup.send(f"Offered {amount} ore!", ephemeral=True)
                                        await self.update_trade_message()
                                except asyncio.TimeoutError:
                                    pass

                            @discord.ui.button(label="Offer Fuel", style=discord.ButtonStyle.blurple)
                            async def offer_fuel(self, interaction: discord.Interaction, button: Button):
                                guild_data = self.cog.get_guild_data(self.guild_id)
                                user_id = str(interaction.user.id)
                                offer = self.initiator_offer if interaction.user.id == self.initiator.id else self.target_offer
                                await interaction.response.send_message("How much fuel?", ephemeral=True)
                                def check(m):
                                    return m.author.id == interaction.user.id and m.channel == interaction.channel and m.content.isdigit()
                                try:
                                    msg = await self.cog.bot.wait_for("message", check=check, timeout=30)
                                    amount = int(msg.content)
                                    if guild_data[user_id]["fuel"] < amount:
                                        await interaction.followup.send(f"Only have {guild_data[user_id]['fuel']} fuel!", ephemeral=True)
                                    else:
                                        offer["fuel"] = amount
                                        await interaction.followup.send(f"Offered {amount} fuel!", ephemeral=True)
                                        await self.update_trade_message()
                                except asyncio.TimeoutError:
                                    pass

                            @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
                            async def accept(self, interaction: discord.Interaction, button: Button):
                                if interaction.user.id == self.initiator.id:
                                    self.initiator_accepted = True
                                    await interaction.response.send_message("Accepted!", ephemeral=True)
                                elif interaction.user.id == self.target.id:
                                    self.target_accepted = True
                                    await interaction.response.send_message("Accepted!", ephemeral=True)

                                await self.update_trade_message()

                                if self.initiator_accepted and self.target_accepted:
                                    guild_data = self.cog.get_guild_data(self.guild_id)
                                    initiator_id = str(self.initiator.id)
                                    target_id = str(self.target.id)

                                    if not any(self.initiator_offer.values()) and not any(self.target_offer.values()):
                                        await interaction.channel.send("Nothing offered!", delete_after=5)
                                        return

                                    if guild_data[initiator_id]["credits"] < self.initiator_offer["credits"] or guild_data[initiator_id]["ore"] < self.initiator_offer["ore"] or guild_data[initiator_id]["fuel"] < self.initiator_offer["fuel"] or guild_data[target_id]["credits"] < self.target_offer["credits"] or guild_data[target_id]["ore"] < self.target_offer["ore"] or guild_data[target_id]["fuel"] < self.target_offer["fuel"]:
                                        image = await self.cog.generate_image("Failed!\nInsufficient Resources")
                                        embed, file = self.cog.create_embed("Trade Failed", "Someone lacks resources!", image_bytes=image)
                                        msg = await interaction.channel.send(embed=embed, file=file)
                                        if msg:
                                            await asyncio.sleep(5)
                                            await msg.delete()
                                    else:
                                        guild_data[initiator_id]["credits"] -= self.initiator_offer["credits"]
                                        guild_data[initiator_id]["ore"] -= self.initiator_offer["ore"]
                                        guild_data[initiator_id]["fuel"] -= self.initiator_offer["fuel"]
                                        guild_data[target_id]["credits"] -= self.target_offer["credits"]
                                        guild_data[target_id]["ore"] -= self.target_offer["ore"]
                                        guild_data[target_id]["fuel"] -= self.target_offer["fuel"]

                                        guild_data[initiator_id]["credits"] += self.target_offer["credits"]
                                        guild_data[initiator_id]["ore"] += self.target_offer["ore"]
                                        guild_data[initiator_id]["fuel"] += self.target_offer["fuel"]
                                        guild_data[target_id]["credits"] += self.initiator_offer["credits"]
                                        guild_data[target_id]["ore"] += self.initiator_offer["ore"]
                                        guild_data[target_id]["fuel"] += self.initiator_offer["fuel"]

                                        self.cog.save_guild_data(self.guild_id, guild_data)
                                        image = await self.cog.generate_image("Success!\nTrade Complete")
                                        embed, file = self.cog.create_embed("Trade Complete!", f"{self.initiator.mention} gave: {self.initiator_offer['credits']} cr, {self.initiator_offer['ore']} ore, {self.initiator_offer['fuel']} fuel\n{self.target.mention} gave: {self.target_offer['credits']} cr, {self.target_offer['ore']} ore, {self.target_offer['fuel']} fuel", image_bytes=image)
                                        msg = await interaction.channel.send(embed=embed, file=file)
                                        if msg:
                                            await asyncio.sleep(5)
                                            await msg.delete()

                                    self.parent_view.shop_open = False
                                    for item in self.parent_view.children:
                                        item.disabled = False
                                    await self.parent_view.message.edit(view=self.parent_view)
                                    await self.message.delete()
                                    self.stop()

                            @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, emoji="❌")
                            async def cancel(self, interaction: discord.Interaction, button: Button):
                                image = await self.cog.generate_image("Canceled!\nTrade Aborted")
                                embed, file = self.cog.create_embed("Trade Canceled", f"{interaction.user.mention} canceled the trade.", image_bytes=image)
                                msg = await interaction.channel.send(embed=embed, file=file)
                                if msg:
                                    await asyncio.sleep(5)
                                    await msg.delete()
                                self.parent_view.shop_open = False
                                for item in self.parent_view.children:
                                    item.disabled = False
                                await self.parent_view.message.edit(view=self.parent_view)
                                await self.message.delete()
                                self.stop()

                            async def update_trade_message(self):
                                embed, _ = self.cog.create_embed(
                                    "Trade Request",
                                    f"{self.initiator.mention} offers: {self.initiator_offer['credits']} cr, {self.initiator_offer['ore']} ore, {self.initiator_offer['fuel']} fuel (Accepted: {self.initiator_accepted})\n"
                                    f"{self.target.mention} offers: {self.target_offer['credits']} cr, {self.target_offer['ore']} ore, {self.target_offer['fuel']} fuel (Accepted: {self.target_accepted})\n\n"
                                    "Both must accept!"
                                )
                                await self.message.edit(embed=embed, view=self)

                            async def on_timeout(self):
                                image = await self.cog.generate_image("Timed Out!\nTrade Expired")
                                embed, file = self.cog.create_embed("Trade Timed Out", "Trade expired due to inactivity.", image_bytes=image)
                                msg = await self.message.channel.send(embed=embed, file=file)
                                if msg:
                                    await asyncio.sleep(5)
                                    await msg.delete()
                                self.parent_view.shop_open = False
                                for item in self.parent_view.children:
                                    item.disabled = False
                                await self.parent_view.message.edit(view=self.parent_view)
                                await self.message.delete()

                        image = await self.cog.generate_image(f"Trade Initiated!\nWith {target.name}")
                        embed, file = self.cog.create_embed("Trade Request", f"{self.user.mention} wants to trade with {target.mention}!\nOffer resources below.", image_bytes=image)
                        trade_view = TradeView(self.cog, self.user, target, self.guild_id, self.parent_view)
                        await self.message.delete()
                        self.parent_view.shop_message = await interaction.channel.send(embed=embed, file=file, view=trade_view, delete_after=60)
                        trade_view.message = self.parent_view.shop_message
                        await interaction.response.defer()

                    async def cancel_callback(self, interaction: discord.Interaction):
                        image = await self.cog.generate_image("Canceled!\nTrade Hub Closed")
                        embed, file = self.cog.create_embed("Trade Hub Closed", f"{self.user.mention}, trade selection canceled.", image_bytes=image)
                        msg = await interaction.channel.send(embed=embed, file=file)
                        if msg:
                            await asyncio.sleep(5)
                            await msg.delete()
                        self.parent_view.shop_open = False
                        for item in self.parent_view.children:
                            item.disabled = False
                        await self.parent_view.message.edit(view=self.parent_view)
                        await self.message.delete()
                        self.stop()

                    async def on_timeout(self):
                        image = await self.cog.generate_image("Timed Out!\nTrade Hub Closed")
                        embed, file = self.cog.create_embed("Trade Hub Closed", f"{self.user.mention}, trade selection timed out.", image_bytes=image)
                        msg = await self.message.channel.send(embed=embed, file=file)
                        if msg:
                            await asyncio.sleep(5)
                            await msg.delete()
                        self.parent_view.shop_open = False
                        for item in self.parent_view.children:
                            item.disabled = False
                        await self.parent_view.message.edit(view=self.parent_view)
                        await self.message.delete()

                trade_select_view = TradeSelect(self.cog, self.user, self.guild_id, self, tradable_players)
                self.shop_message = await interaction.channel.send(embed=embed, view=trade_select_view, delete_after=60)
                trade_select_view.message = self.shop_message
                await interaction.response.send_message("Trade hub opened!", ephemeral=True)

            @discord.ui.button(label="Attack", style=discord.ButtonStyle.red, emoji="⚔️")
            async def attack_button(self, interaction: discord.Interaction, button: Button):
                if self.shop_open:
                    await interaction.response.send_message("Finish current task first!", ephemeral=True)
                    return

                self.shop_open = True
                for item in self.children:
                    item.disabled = True
                await self.message.edit(view=self)

                guild_data = self.cog.get_guild_data(self.guild_id)
                user_id = str(self.user.id)
                now = datetime.datetime.utcnow().timestamp()
                last_attack = guild_data[user_id]["last_attack"]
                cooldown = 3600
                if now - last_attack < cooldown:
                    remaining = int(cooldown - (now - last_attack))
                    minutes = remaining // 60
                    await interaction.response.send_message(f"Attack systems recharging! Ready in {minutes}m!", ephemeral=True)
                    self.shop_open = False
                    for item in self.children:
                        item.disabled = False
                    await self.message.edit(view=self)
                    return

                attackable_players = [
                    (uid, self.cog.bot.get_user(int(uid)))
                    for uid in guild_data.keys()
                    if uid != user_id and guild_data[uid]["durability"] > 0 and self.cog.bot.get_user(int(uid)) and not self.cog.bot.get_user(int(uid)).bot
                ]
                if not attackable_players:
                    await interaction.response.send_message("No targets available!", ephemeral=True)
                    self.shop_open = False
                    for item in self.children:
                        item.disabled = False
                    await self.message.edit(view=self)
                    return

                embed, _ = self.cog.create_embed("Combat Bay", f"{self.user.mention}, select a target!\n(60% base win chance, modified by shields)")

                class AttackSelect(Select):
                    def __init__(self, cog, user, guild_id, parent_view, targets):
                        options = [discord.SelectOption(label=target.display_name, value=str(target.id)) for _, target in targets]
                        super().__init__(placeholder="Choose a target", options=options[:25])
                        self.cog = cog
                        self.user = user
                        self.guild_id = guild_id
                        self.parent_view = parent_view

                    async def callback(self, interaction: discord.Interaction):
                        target_id = self.values[0]
                        target = self.cog.bot.get_user(int(target_id))
                        guild_data = self.cog.get_guild_data(self.guild_id)
                        user_id = str(self.user.id)
                        guild = self.cog.bot.get_guild(int(self.guild_id))

                        attacker_shield = guild_data[user_id]["shield"]
                        defender_shield = guild_data[target_id]["shield"]
                        base_chance = 0.6
                        shield_modifier = (attacker_shield - defender_shield) * 0.005
                        win_chance = max(0.2, min(0.8, base_chance + shield_modifier))
                        attacker_wins = random.random() < win_chance

                        loot_credits = min(500, int(guild_data[target_id]["credits"] * 0.1))
                        loot_ore = min(100, int(guild_data[target_id]["ore"] * 0.1))
                        loot_fuel = min(50, int(guild_data[target_id]["fuel"] * 0.1))

                        if attacker_wins:
                            guild_data[user_id]["credits"] += loot_credits
                            guild_data[user_id]["ore"] += loot_ore
                            guild_data[user_id]["fuel"] += loot_fuel
                            guild_data[target_id]["credits"] = max(0, guild_data[target_id]["credits"] - loot_credits)
                            guild_data[target_id]["ore"] = max(0, guild_data[target_id]["ore"] - loot_ore)
                            guild_data[target_id]["fuel"] = max(0, guild_data[target_id]["fuel"] - loot_fuel)
                            guild_data[target_id]["durability"] = max(0, guild_data[target_id]["durability"] - 10)
                            guild_data[user_id]["successful_attacks"] += 1
                            attacker_dmg = 5 if random.random() < 0.2 else 0
                            guild_data[user_id]["durability"] = max(0, guild_data[user_id]["durability"] - attacker_dmg)
                            attacker_result = f"Looted {loot_credits} cr, {loot_ore} ore, {loot_fuel} fuel" + (f"\nTook {attacker_dmg} damage" if attacker_dmg else "")
                            defender_result = f"{self.user.mention} stole {loot_credits} cr, {loot_ore} ore, {loot_fuel} fuel\nLost 10 durability\nGuild: {guild.name if guild else 'Unknown'}"
                            image = await self.cog.generate_image(f"Victory!\n+{loot_credits} Cr, +{loot_ore} Ore")
                        else:
                            guild_data[user_id]["durability"] = max(0, guild_data[user_id]["durability"] - 10)
                            attacker_result = "Lost! Took 10 durability damage"
                            defender_result = f"Repelled {self.user.mention}’s attack!\nGuild: {guild.name if guild else 'Unknown'}"
                            image = await self.cog.generate_image("Defeat!\n-10 Durability")

                        guild_data[user_id]["last_attack"] = now
                        self.cog.save_guild_data(self.guild_id, guild_data)

                        attacker_embed, attacker_file = self.cog.create_embed("Combat Report", f"Attacked {target.mention}!\n{attacker_result}", image_bytes=image)
                        defender_embed, defender_file = self.cog.create_embed("Combat Report", defender_result, image_bytes=image)

                        attacker_msg = await interaction.response.send_message(embed=attacker_embed, file=attacker_file, ephemeral=True)
                        if attacker_msg:
                            await asyncio.sleep(6)
                            await attacker_msg.delete()

                        try:
                            defender_msg = await target.send(embed=defender_embed, file=defender_file)
                            if defender_msg:
                                await asyncio.sleep(6)
                                await defender_msg.delete()
                        except discord.errors.Forbidden:
                            defender_msg = await interaction.channel.send(embed=defender_embed, file=defender_file)
                            if defender_msg:
                                await asyncio.sleep(6)
                                await defender_msg.delete()

                        self.parent_view.shop_open = False
                        for item in self.parent_view.children:
                            item.disabled = False
                        await self.parent_view.message.edit(view=self.parent_view)
                        if self.parent_view.shop_message:
                            try:
                                await self.parent_view.shop_message.delete()
                            except (discord.errors.Forbidden, discord.errors.NotFound):
                                pass

                attack_view = View()
                attack_view.add_item(AttackSelect(self.cog, self.user, self.guild_id, self, attackable_players))
                attack_view.add_item(Button(label="Cancel", style=discord.ButtonStyle.red, emoji="❌", custom_id="close_attack"))

                async def close_attack_callback(interaction: discord.Interaction):
                    if interaction.user.id != self.user.id:
                        await interaction.response.send_message("Only the captain can cancel!", ephemeral=True)
                        return
                    self.shop_open = False
                    for item in self.children:
                        item.disabled = False
                    await self.message.edit(view=self)
                    if self.shop_message:
                        try:
                            await self.shop_message.delete()
                        except (discord.errors.Forbidden, discord.errors.NotFound):
                            pass
                        self.shop_message = None
                    await interaction.response.send_message("Attack canceled!", ephemeral=True)

                for item in attack_view.children:
                    if item.custom_id == "close_attack":
                        item.callback = close_attack_callback

                self.shop_message = await interaction.channel.send(embed=embed, view=attack_view, delete_after=60)
                await interaction.response.defer()

            @discord.ui.button(label="Status", style=discord.ButtonStyle.grey, emoji="📊")
            async def status_button(self, interaction: discord.Interaction, button: Button):
                user_id = str(self.user.id)
                guild_data = self.cog.get_guild_data(self.guild_id)
                upgrades = ", ".join(guild_data[user_id]["upgrades"]) if guild_data[user_id]["upgrades"] else "None"
                achievements = ", ".join([self.cog.achievements[ach]["title"] for ach in guild_data[user_id]["achievements"]]) if guild_data[user_id]["achievements"] else "None"
                status_text = (
                    f"🪐 **Ship Stats** 🪐\n"
                    f"Location: {guild_data[user_id]['current_planet']}\n"
                    f"Credits: {guild_data[user_id]['credits']}\n"
                    f"Ore: {guild_data[user_id]['ore']}\n"
                    f"Fuel: {guild_data[user_id]['fuel']}\n"
                    f"Durability: {guild_data[user_id]['durability']}/100\n"
                    f"Shield: {guild_data[user_id]['shield']}/100\n"
                    f"Speed: {guild_data[user_id]['speed']}%\n"
                    f"Upgrades: {upgrades}\n"
                    f"Achievements: {achievements}\n"
                    f"Total Mines: {guild_data[user_id]['total_mines']}\n"
                    f"Successful Attacks: {guild_data[user_id]['successful_attacks']}"
                )
                embed, _ = self.cog.create_embed("Mining Status", status_text)
                await interaction.response.send_message(embed=embed, ephemeral=True)

            @discord.ui.button(label="Abort", style=discord.ButtonStyle.red, emoji="🏁")
            async def abort_button(self, interaction: discord.Interaction, button: Button):
                for item in self.children:
                    item.disabled = True
                embed, _ = self.cog.create_embed("Mission Aborted", f"{self.user.mention}, session terminated!\n\n*Ship powering down...*")
                self.shop_open = False
                try:
                    await interaction.response.edit_message(embed=embed, view=self)
                    image = await self.cog.generate_image("Mission Ended!\nShip Offline")
                    embed_with_image, file = self.cog.create_embed("Mission Aborted", "Ship offline!", image_bytes=image)
                    confirmation_msg = await interaction.channel.send(embed=embed_with_image, file=file)
                    if confirmation_msg:
                        await asyncio.sleep(6)
                        await confirmation_msg.delete()
                    if self.shop_message:
                        try:
                            await self.shop_message.delete()
                        except (discord.errors.Forbidden, discord.errors.NotFound):
                            pass
                        self.shop_message = None
                except discord.errors.HTTPException:
                    msg = await interaction.channel.send("Session ended, but couldn’t update UI!")
                    if msg:
                        await asyncio.sleep(5)
                        await msg.delete()
                self.stop()

        embed, _ = self.create_embed("Space Miner", f"{ctx.author.mention}, {welcome_message}\nCourse set from {user_data['current_planet']}.\nControl your rig below!")
        view = SpaceMinerView(self, ctx.author, ctx.guild.id)
        message = await ctx.send(embed=embed, view=view)
        view.message = message

async def setup(bot):
    await bot.add_cog(SpaceMiner(bot))