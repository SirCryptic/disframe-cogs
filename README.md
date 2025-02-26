<p align="center">
  <a href="https://github.com/sircryptic/disframe-cogs/stargazers"><img src="https://img.shields.io/github/stars/sircryptic/disframe-cogs.svg" alt="GitHub stars"></a>
  <a href="https://github.com/sircryptic/disframe-cogs/network"><img src="https://img.shields.io/github/forks/sircryptic/disframe-cogs.svg" alt="GitHub forks"></a>
   <a href="https://github.com/sircryptic/disframe-cogs/watchers"><img src="https://img.shields.io/github/watchers/sircryptic/disframe-cogs.svg" alt="GitHub watchers"></a>
</p>

# DisFrame-Cogs

Welcome to **DisFrame-Cogs**, the community cog repository for the [DisFrame Discord bot framework](https://github.com/sircryptic/disframe)! This repo is a hub for sharing and discovering custom cogs to extend your DisFrame bot with new features, games, utilities, and more. Built by the community, for the community!

## What is DisFrame?
DisFrame is a flexible, modular Discord bot framework written in Python using `discord.py`. It’s designed to make bot development easy and extensible through a cog-based system. Whether you’re adding moderation tools, fun games, or unique commands, DisFrame’s structure lets you plug in cogs seamlessly.

## Purpose
This repository hosts a collection of community-created cogs for DisFrame. Each cog is a self-contained module you can add to your bot to enhance its functionality. From economy games like CoinRush to admin utilities, you’ll find tools here to supercharge your Discord server!

## Getting Started

### Prerequisites
- A running DisFrame bot (see the [DisFrame repo](https://github.com/sircryptic/disframe) for setup).
- Basic knowledge of Python and Discord bot commands.

### Installation
Adding cogs to your DisFrame bot is simple:

1. **Browse the Repo**:
   - Check out the folders here (e.g., `coinrush/`) for available cogs.

2. **Download a Cog**:
   - Each cog folder typically contains a `.py` file (e.g., `coinrush.py`) and an optional `README.md` with specific instructions.
   - Some cogs may include an `assets` folder with images, fonts, or other resources.

3. **Drag and Drop**:
   - Place the `.py` file (e.g., `coinrush.py`) into your DisFrame bot’s `cmds/` folder in the root directory. DisFrame will load it automatically on startup.
   - **Optional Organization**: For tidiness, create a subfolder like `cmds/games/` and drop the `.py` file there—DisFrame supports subfolders!
   - If the cog includes an `assets` folder, move it to your DisFrame root directory (next to `bot.py`) to keep resources accessible.

4. **Run Your Bot**:
   - Start your bot with `python bot.py`. The cog will be loaded and ready to use!
   - Check the cog’s `README.md` for any setup commands (e.g., `!coinrushsetup` for CoinRush).

### Example: Adding CoinRush
- Download `coinrush/coinrush.py` and `coinrush/assets/`.
- Place `coinrush.py` in `cmds/` or `cmds/games/`.
- Move the `assets/` folder to your DisFrame root.
- Run your bot and type `!coinhelp` to start playing!

## Available Cogs
Here’s a growing list of cogs you can explore:
- **[CoinRush](coinrush/README.md)**: An economy game with jobs, items, trading, achievements, and a casino.

More cogs coming soon—add yours to the collection!

## Contributing
We’d love your help growing this community! Here’s how to contribute:

1. **Fork the Repo**:
   - Click "Fork" at [github.com/sircryptic/DisFrame-cogs](https://github.com/sircryptic/DisFrame-cogs).

2. **Create Your Cog**:
   - Write a cog in Python following DisFrame’s cog structure (see [DisFrame docs](https://github.com/sircryptic/disframe) or existing cogs like `coinrush.py`).
   - Add a `README.md` in your cog’s folder with a description, features, and usage instructions.

3. **Organize Your Files**:
   - Place your cog in a folder (e.g., `mycog/mycog.py`).
   - Include any assets in a subfolder (e.g., `mycog/assets/`).

4. **Submit a Pull Request**:
   - Push your changes to your fork and create a pull request to this repo.
   - Describe your cog in the PR—why it’s awesome and how it works!

5. **Join the Community**:
   - Share ideas, report bugs, or chat with us on the [DisFrame Discord](https://discord.gg/48JH3UkerX).

## Guidelines
- **Compatibility**: Ensure your cog works with DisFrame’s latest version.
- **Documentation**: Include a `README.md` with clear setup and usage steps.
- **Naming**: Use descriptive, unique names for your cog to avoid conflicts.
- **Respect**: Keep it fun and friendly—no malicious code!

## Resources
- **DisFrame Framework**: [github.com/sircryptic/disframe](https://github.com/sircryptic/disframe)
- **DisFrame Website**: [sircryptic.github.io/DisWeb](https://sircryptic.github.io/DisWeb/)
- **Community Discord**: [discord.gg/48JH3UkerX](https://discord.gg/48JH3UkerX)

## License
Cogs here are free for use with DisFrame—check individual cog `README.md` files for specific licensing details (if any).

---

**Maintained by**: SirCryptic & the DisFrame Community  
**Get Involved**: Star this repo, add a cog, or join the fun!
