# CoinRush Cog for DisFrame

Welcome to **CoinRush**, an enhanced economy game cog for your Discord bot! Built for the DisFrame framework using Python and `discord.py`, this cog brings a rich, guild-only experience with jobs, coins, items, trading, achievements, and a casino. Whether you're a lawful worker or a sneaky thief, CoinRush offers endless fun and strategy!

## Features

- **Jobs**: Choose from a variety of jobs like Hacker, Police, Paramedic, or even illicit ones like Drug Dealer and Cartel Boss. Each has unique pay ranges and risks!
- **Economy**: Earn coins through work, daily rewards, or risky investments. Spend them in the shop or trade with others.
- **Items**: Purchase items like Cool Hat, Laser Gun, or VIP Badge from the shop to boost work earnings, enhance stealing, or protect your stash.
- **Stealing**: Take a chance to steal coins or items from other players—success depends on your items and their defenses!
- **Trading**: Negotiate trades with other players for coins and items via an interactive UI.
- **Casino**: Spin the slots for a chance at big wins—or big losses!
- **Achievements**: Unlock titles like "Millionaire" or "Gambler" by hitting gameplay milestones.
- **VIP Role**: Buy the VIP Badge for 95% theft protection and an exclusive ⭐VIP role in your guild.
- **Dynamic Images**: Work, steal, and casino actions generate custom images with earnings or penalties.

## Installation

### For DisFrame Users
If you're using the DisFrame bot framework, installation is a breeze:

1. **Download the Files**:
   - Grab `coinrush.py` and the `assets` folder from this repository.

2. **Drag and Drop**:
   - Place the `assets` folder directly in your DisFrame root directory (where `bot.py` lives). It contains images and fonts used by CoinRush.
   - Drop `coinrush.py` into the `cmds` folder in your DisFrame root directory to load it automatically with your bot.

3. **Optional Organization**:
   - For cleaner organization, you can create a `games` folder inside `cmds` (e.g., `cmds/games/`) and place `coinrush.py` there. DisFrame will still load it as long as it’s in a subfolder of `cmds`.

4. **Run Your Bot**:
   - Start your DisFrame bot (`python bot.py`). CoinRush will be loaded and ready!

5. **Setup in Guild**:
   - Use `!coinrushsetup` (replace `!` with your bot’s prefix) in a guild to create the ⭐VIP role if it’s missing. Ensure the bot has "Manage Roles" permission.

### For Non-DisFrame Users
If you’re not using DisFrame, you’ll need to adapt the cog:

1. Ensure your bot uses `discord.py` and has a similar cog loading system.
2. Place `coinrush.py` in your bot’s `cmds` directory.
3. Add the `assets` folder to your bot’s root directory.
4. Load the cog manually with bots load/unload/reload feature.

## Usage

### Commands
- `!coinhelp` - View all commands and gameplay tips.
- `!coin` - Start the CoinRush game with an interactive UI (Work, Steal, Shop, Balance, Invest, Trade, Casino).
- `!setjob <job>` - Pick a job (e.g., `!setjob Hacker`) or list available jobs.
- `!quitjob` - Quit your current job.
- `!daily` - Claim a daily coin reward (50-100 coins, once every 24 hours).
- `!trade` - Start a trade with another player.
- `!coinleader` - See the guild’s top coin holders.
- `!achievements` - Check your unlocked achievements.
- `!coinrushsetup` - Create the ⭐VIP role (requires "Manage Roles" permission).

### Gameplay Tips
- **Jobs**: Elicit jobs (e.g., Cartel Boss) pay more but risk fines or jail time. Safe jobs (e.g., Chef) are steady earners.
- **Items**: Use items like Medkit to avoid hospital bills or Smoke Bomb to escape busts.
- **Casino**: Bet coins in slots—match three symbols for a 5x payout!
- **VIP**: The VIP Badge offers near-total theft protection and a shiny role.

## Requirements

- **Assets**: The `assets` folder includes:
  - `images/coinrush_base.jpg` (default action image).
  - `images/busted_base.jpg` (bust penalty image).
  - `images/hospital_base.jpg` (hospital penalty image).
  - `fonts/impact.ttf` (text overlay font).
- **Permissions**: The bot needs "Manage Roles" for VIP functionality and "Embed Links" for rich UI.
- **Data**: Creates a `data/games/coinrush/` folder to store guild-specific game data.

## Notes
- **Image Placeholder**: If asset images are missing, the cog falls back to a gray background.

## Contributing
This cog is part of the DisFrame community cogs repo! Feel free to:
- Suggest new jobs, items, or achievements via issues or pull requests.
- Submit bug fixes or enhancements.
- Share your gameplay ideas on the [DisFrame Discord](https://discord.gg/48JH3UkerX).

Drag it into your DisFrame bot and start the rush!

---

**Author**: SirCryptic  
**GitHub**: [github.com/SirCryptic](https://github.com/SirCryptic)  
**License**: Free for use within the DisFrame community—enjoy!
