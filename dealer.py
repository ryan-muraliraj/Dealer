import discord
from mparse import *
import constants

class dealer(discord.Client):
    
    def __init__(self):
        
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        

    async def process_msg(self, message):
        try:
            parser = Parser(message)
            response = parser.parse()
            if(parser.embed):
                await message.channel.send(embed=response)
            else:
                await message.channel.send(response)


        except Exception as e:
            print(e)

    def run(self):
        token = constants.get_discord_token()
        super().run(token)
        
    async def on_ready(self):
        print(f'{self.user} is live')

    async def on_message(self, message):
        if message.author == self.user:
            return
        elif message.content[0] == '*':
            await self.process_msg(message)
        else:
            return
