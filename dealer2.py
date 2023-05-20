import discord
import constants

from discord.ext import commands

class Dealer(commands.Bot):
    
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.presences = True
        intents.message_content = True

        super().__init__(command_prefix="*", intents=intents, help_command=None)

        self.load_commands()

    def run(self):
        print("The Dealer is starting...")
        super().run(constants.get_discord_token(), reconnect=True)


    def load_commands(self):

        @self.bridge_command(name="help", guild_ids=[696122756072341616])
        async def help(ctx):
            await ctx.respond("YOU NEED HELP!?")

d = Dealer()
d.run()