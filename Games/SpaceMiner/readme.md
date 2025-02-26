# SpaceMiner Cog for DisFrame

Welcome to **SpaceMiner**, an expansive guild-only space mining adventure for your Discord bot! Built for the DisFrame framework using Python and `discord.py`, this cog lets you explore planets, manage a crew, upgrade your ship, craft items, trade resources, and battle rivals in a cosmic quest for riches and glory.

## Features

- **Planets**: Mine on diverse worlds like Asteria (credit-rich), Ferron (ore-heavy), or Nebulon (high-risk, high-reward). Each has unique resources and risks!
- **Resources**: Gather credits, ore, and fuel to sustain your journey and upgrade your rig.
- **Upgrades & Crew**: Buy items like Drill Bit, Hyperdrive, or Navigator to boost mining, speed, or mission success. Craft tools like Repair Kits or Fuel Cells.
- **Missions**: Encounter random events—pirate ambushes, rare asteroids, or cosmic storms—adding thrill to every mine.
- **Trading**: Swap credits, ore, and fuel with other players via an interactive trade UI.
- **Combat**: Attack rival miners to steal resources (60% base win chance, modified by shields).
- **Achievements**: Unlock titles like "Galactic Explorer" or "Shieldmaster" by mastering the stars.
- **Explorer Role**: Earn all achievements for the exclusive 🚀Galactic Explorer role!
- **Dynamic Images**: Mining, trading, and combat actions generate custom images with results.

## Installation

### For DisFrame Users
Adding SpaceMiner to your DisFrame bot is straightforward:

1. **Download the Files**:
   - Grab `spaceminer.py` and the `assets` folder from this repository.

2. **Drag and Drop**:
   - Place the `assets` folder in your DisFrame root directory (where `bot.py` is). It contains the base image and font used by SpaceMiner.
   - Drop `spaceminer.py` into the `cmds` folder in your DisFrame root directory to load it automatically.

3. **Optional Organization**:
   - For a tidier setup, create a `games` folder inside `cmds` (e.g., `cmds/games/`) and place `spaceminer.py` there. DisFrame will still load it from subfolders.

4. **Run Your Bot**:
   - Start your DisFrame bot (`python bot.py`). SpaceMiner will be ready to launch!

5. **Setup in Guild**:
   - Use `!spacesetup` (replace `!` with your bot’s prefix) in a guild to create the 🚀Galactic Explorer role. Requires "Manage Roles" permission for you and the bot.

### For Non-DisFrame Users
If you’re not using DisFrame, adapt the cog as follows:

1. Ensure your bot uses `discord.py` with a cog system.
2. Place `spaceminer.py` in your cog directory.
3. Add the `assets` folder to your bot’s root.
4. Modify `config.py` references (`BOT_PREFIX`, `BOT_NAME`, `BOT_VERSION`) to fit your bot’s setup.
5. Restart The bot or load the cog manually with bots load/unload/reload feature.

## Usage

### Commands
- `!spacehelp` - View commands and gameplay tips.
- `!space` - Launch your mining rig with an interactive UI (Mine, Shop, Craft, Travel, Trade, Attack, Status).
- `!spacebalance` - Check your ship’s resources, upgrades, and achievements.
- `!spaceleader` - See the guild’s top miners.
- `!spacesetup` - Create the 🚀Galactic Explorer role (requires "Manage Roles").

### Gameplay Tips
- **Mining**: Higher-risk planets (e.g., Nebulon) offer bigger hauls but trigger more missions.
- **Upgrades**: Equip items like Plasma Cutter for 50% more credits or Shield Generator to fend off attacks.
- **Crafting**: Build Repair Kits to fix durability or Fuel Cells for extra juice (30-min cooldown).
- **Combat**: Attack wisely—shields boost your win chance!
- **Achievements**: Unlock all 8 to earn the 🚀Galactic Explorer role.

## Requirements

- **Python Packages**:
  - `discord.py`: Core library for Discord interactions (typically included with DisFrame).
  - `Pillow`: For image generation (`pip install Pillow`).
- **Assets**:
  - `assets/images/spaceminer_base.jpg`: Default action image.
  - `assets/fonts/impact.ttf`: Font for text overlays.
- **Permissions**: The bot needs:
  - "Manage Roles" for the Explorer role.
  - "Embed Links" for UI.
- **Data**: Creates a `data/games/spaceminer/` folder for guild-specific data.

### Installing Requirements
Run this command in your bot’s environment:
```bash
pip install Pillow
```

## Notes
- **Image Fallback**: If `spaceminer_base.jpg` is missing, a purple background is used.

## Contributing
This cog is part of the DisFrame community cogs repo! Help us expand it:
- Suggest new planets, items, or missions via issues or pull requests.
- Fix bugs or add features.
- Join the [DisFrame Discord](https://discord.gg/48JH3UkerX) to share ideas!

Drop it into your DisFrame bot and explore the galaxy!

---

**Author**: SirCryptic  
**GitHub**: [github.com/SirCryptic](https://github.com/SirCryptic)  
**License**: Free for use with DisFrame — blast off!
