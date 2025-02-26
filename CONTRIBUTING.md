# Contributing to DisFrame Community Cogs

Thank you for your interest in contributing to the DisFrame Community Cogs repository! This is a collaborative space to enhance the DisFrame Discord bot framework with new commands, features, and utilities. Whether you’re fixing bugs, adding cogs, or improving documentation, your contributions are welcome.

## How to Contribute

### Getting Started
1. **Fork the Repository**: Click the "Fork" button on the [DisFrame Community Cogs GitHub page](https://github.com/sircryptic/DisFrame-cogs) to create your own copy.
2. **Clone Your Fork**: Clone your forked repository to your local machine using Git.
3. **Set Up DisFrame**: Ensure you have the main [DisFrame bot](https://github.com/sircryptic/disframe) installed and running locally to test your cogs (see the [Hosting Guide](https://sircryptic.github.io/DisWeb/pages/guide.html)).
4. **Create a Branch**: Work on a new branch for your contribution (e.g., `git checkout -b feature/new-cog`).

### Making Changes
- **Add a Cog**: Place your Python cog file in the `cmds/` directory. Ensure it follows the `discord.py` cog structure with a `setup` function.
- **Test Your Cog**: Run the DisFrame bot locally to verify your cog works as intended.
- **Follow Guidelines**:
  - Keep code readable and well-documented with comments or docstrings.
  - Respect the existing naming conventions (e.g., lowercase command names).
  - Ensure compatibility with Python 3.8+ and `discord.py==2.4.0`.

### Submitting Your Contribution
1. **Commit Changes**: Use clear, descriptive commit messages (e.g., "Add new meme generator cog").
2. **Push to Your Fork**: Push your branch to your GitHub fork.
3. **Create a Pull Request (PR)**:
   - Go to the original [DisFrame Community Cogs repo](https://github.com/sircryptic/DisFrame-cogs).
   - Click "New Pull Request" and select your branch.
   - Provide a detailed description of your changes, including purpose and testing notes.
4. **Review Process**: Your PR will be reviewed by maintainers. Respond to feedback and make requested changes if needed.

## Licensing

- **Core Repository License**: The DisFrame Community Cogs repository is licensed under the [MIT License](https://github.com/sircryptic/DisFrame-cogs/blob/main/LICENSE). Original framework files (e.g., templates or utilities) retain copyright © 2025 SirCryptic.
- **Your Contributions**: I encourage you to license your cogs under the MIT License for consistency. However, you may choose any open-source license compatible with MIT (e.g., Apache 2.0, BSD), retaining your own copyright. Please:
  - Include a copyright notice in your cog file (e.g., `# Copyright © [Your Name] 2025`).
  - Specify your chosen license in the file or PR description.
- **Compatibility**: Ensure your license allows integration with the MIT-licensed DisFrame framework.

## Guidelines

- **Quality**: Submit functional, tested code that enhances DisFrame’s capabilities (e.g., moderation tools, fun commands, games).
- **Respect**: Avoid submitting malicious code or content that violates Discord’s Terms of Service.
- **Collaboration**: If building on someone else’s cog, credit them in your file or PR.

## Need Help?

- Join our [Discord server](https://discord.gg/48JH3UkerX) for support or to discuss ideas.
- Open an issue on the [DisFrame Community Cogs repo](https://github.com/sircryptic/DisFrame-cogs/issues) for bugs or suggestions.

## Acknowledgments

Every contributor helps make DisFrame better! Your name may be featured in the repository or documentation unless you request otherwise.

Happy coding, and thank you for joining the DisFrame community!
