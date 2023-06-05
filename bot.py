import discord


# Client class for Discord bot
class DiscordClient(discord.Client):
    def __init__(self, *, intents: discord.Intents = discord.Intents.default()):
        super().__init__(intents=intents)
        # command tree to contain all registered slash commands
        self.tree = discord.app_commands.CommandTree(self)

    # sync available slash commands with Discord
    async def setup_hook(self):
        await self.tree.sync()
