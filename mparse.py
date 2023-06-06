import discord, datetime
import manager

class Parser():

    def __init__(self,message):
        self.message = message.content.lower()
        self.user = message.author
        self.embed = False
        self.m = manager.Manager()


    def parse(self):

        x = self.message[1:]
        x = x.split()
        match x[0]:
            
            case 'ping':
                return "pong"
            case 'daily':
                num = self.m.daily('WHX', self.user)
                if not isinstance(num, int):
                    result = datetime.timedelta(hours=24)-num
                    minutes = (result.seconds % 3600) // 60
                    hours = (result.seconds // 3600)
                    return f"You can claim your daily in {hours} hours and {minutes} minutes."
                else:
                    pass
                if(self.m.load_server('WHX', self.user, True)):
                    x = self.m.load_server('WHX', self.user, False)
                    self.m.save_to_server('WHX', self.user, int(x)+num)
                else:
                    self.m.save_to_server('WHX', self.user, num)
                return f"Daily claimed! {num} credits added to balance. Come back in 24 hours."
            case ['profile' | 'bank' | 'money' | 'credits' | 'credit', *args]:
                return self.profile(args[0])
            case other:
                return "Not a recognized command."

    def profile(self, user = None):
            if user == None:
                user = self.user
            self.embed = True
            x = self.m.load_server('WHX', user, False)
            
            embed = discord.Embed(title=user, description=f"Credits: {x}", color=discord.Color.random())
            embed.set_author(name="Profile")
            embed.set_thumbnail(url=f"{self.user.display_avatar}")
            embed.set_footer(text="5-14-2023")
            return embed        

        