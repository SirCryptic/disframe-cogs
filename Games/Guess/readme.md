# GuessGame Cog for DisFrame

Welcome to **GuessGame**, a classic "Guess the Number" game for your Discord bot! Built for the DisFrame framework using Python and `discord.py`, this cog offers a simple yet engaging experience with text feedback and image overlays. Play solo in DMs or compete with friends in guild channels!

## Features

- **Multiplayer Support**: In guilds, anyone in the channel can join the guess-off!
- **Solo Play**: Enjoy a private game in DMs—just you versus the bot.
- **Dynamic Feedback**: Get "Too High" or "Too Low" hints with custom images using Impact font.
- **Winning Celebration**: Correct guesses trigger a victory image and message.
- **Lightweight**: No complex setup—just pure guessing fun.

## Installation

### For DisFrame Users
Adding GuessGame to your DisFrame bot is quick and easy:

1. **Download the Files**:
   - Grab `guessgame.py` and the `assets` folder from this repository.

2. **Drag and Drop**:
   - Place the `assets` folder in your DisFrame root directory (where `bot.py` is). It contains the base image and font for feedback.
   - Drop `guessgame.py` into the `cmds` folder in your DisFrame root directory to load it automatically.

3. **Optional Organization**:
   - For a neater setup, create a `games` folder inside `cmds` (e.g., `cmds/games/`) and place `guessgame.py` there. DisFrame will still load it from subfolders.

4. **Run Your Bot**:
   - Start your DisFrame bot (`python bot.py`). GuessGame will be ready to play!

### For Non-DisFrame Users
If you’re not using DisFrame, adapt the cog as follows:

1. Ensure your bot uses `discord.py` with a cog system.
2. Place `guessgame.py` in your cog directory.
3. Add the `assets` folder to your bot’s root.
4. Update `config.py` references (`BOT_PREFIX`, `BOT_NAME`, `BOT_VERSION`) to match your bot’s setup.
5. Restart The bot or load the cog manually with bots load/unload/reload feature.

## Usage

### Command
- `!guess [number]` (replace `!` with your bot’s prefix):
  - Without a number: Starts a new game with a secret number between 1 and 100.
  - With a number: Makes a guess in the active game.

### How to Play
- **Guilds**: Start with `!guess`—anyone in the channel can guess with `!guess <number>`. First to guess correctly wins!
- **DMs**: Use `!guess` to start a solo game, then keep guessing until you win.
- **Feedback**: "Too High" or "Too Low" hints guide you, with a victory message when you nail it.

## Requirements

- **Python Packages**:
  - `discord.py`: Core library for Discord interactions (typically included with DisFrame).
  - `Pillow`: For image generation (`pip install Pillow`).
  - `aiohttp`: For async operations (often bundled with DisFrame, but `pip install aiohttp` if needed).
- **Assets**:
  - `assets/images/guess_base.jpg`: Default feedback image.
  - `assets/fonts/impact.ttf`: Font for text overlays.
- **Permissions**: The bot needs "Embed Links" for rich feedback.
- **Fallback**: If assets are missing, it uses a gray background and default font.

### Installing Requirements
Run these commands in your DisFrame bot’s environment:
```bash
pip install Pillow aiohttp
```

## Notes
- **Multiplayer**: In guilds, only one game runs per channel at a time.

## Contributing
This cog is part of the DisFrame community cogs repo! Help us enhance it:
- Suggest new features (e.g., hints, leaderboards) via issues or pull requests.
- Fix bugs or tweak the game.
- Join the [DisFrame Discord](https://discord.gg/48JH3UkerX) to share ideas!

Drop it into your DisFrame bot and start guessing!

---

**Author**: SirCryptic  
**GitHub**: [github.com/SirCryptic](https://github.com/SirCryptic)  
**License**: Free for use with DisFrame — have fun guessing!
