import discord, datetime, random, string
import constants, strings
from jsonmanager import JSONManager

from discord.ext import bridge, commands

class Dealer(bridge.Bot):
    
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.presences = True
        intents.message_content = True
        self.jsonmanager = JSONManager()

        super().__init__(command_prefix="*", intents=intents, help_command=None)

        self.load_commands()

    def run(self):
        print("The Dealer is starting...")
        super().run(constants.get_discord_token(), reconnect=True)


    def load_commands(self):
        JM = self.jsonmanager
       
        @self.slash_command(name="profile", guild_ids=[696122756072341616])
        async def profile(ctx, user: discord.Option(discord.Member, "Enter a username", required=False, default=None) = None):
            await ret_profile(ctx, user)
                
        @self.command(name="profile")
        async def profile(ctx, user = None):
            tomember = commands.MemberConverter()
            try:
                if(user == None):
                    await ret_profile(ctx,user)
                else:
                    user = await tomember.convert(ctx, user)
                    await ret_profile(ctx,user)
            except:
                await ctx.reply("That user was not found or has zero credits.")

        async def ret_profile(ctx, user) -> None:
            puser = ctx.author
            if not(user is None):
                puser = user
            if(JM.load_server('WHX', puser, True)):
                embed = await embed_profile(puser)
                if(type(ctx) is commands.Context):
                    await ctx.reply(embed=embed)
                else:
                    await ctx.respond(embed=embed)
            else:
                if(type(ctx) is commands.Context):
                    await ctx.reply("That user was not found or has zero credits.")
                else:
                    await ctx.respond("That user was not found or has zero credits.")

        async def embed_profile(user) -> discord.Embed:
                credits = JM.load_server('WHX', user, False)
                embed = discord.Embed(title=user, description=f"Credits: {credits}", color=discord.Color.random())
                embed.set_author(name="Profile")
                embed.set_thumbnail(url=f"{user.display_avatar}")
                embed.set_footer(text=datetime.datetime.now().strftime('%m/%d/%Y'))
                return embed

        @self.bridge_command(name="daily", guild_ids=[696122756072341616])
        async def daily(ctx):
            var = JM.daily('WHX', ctx.author)
            if not(type(var) is bool):
                result = datetime.timedelta(hours=24)-var
                minutes = (result.seconds % 3600) // 60
                hours = (result.seconds // 3600)
                await ctx.respond(f"You can claim your daily in {hours} hours and {minutes} minutes.")
            else:
                var = await gen_daily()
                response = await strings.daily_message(*var)
                if(JM.load_server('WHX', ctx.author, True)):
                    credits = JM.load_server('WHX', ctx.author, False)
                    JM.save_to_server('WHX', ctx.author, int(credits) + var[1])
                else:
                    JM.save_to_server('WHX', ctx.author, var[1])
                embed = await embed_daily(ctx.author, response)
                await ctx.respond(embed=embed)

        async def gen_daily() -> tuple:
            odds = random.randint(1,20)
            if(odds < 16):
                return (0,random.randint(100,199))
            elif(odds < 20):
                return (1,random.randint(200,400))
            else:
                return (2,random.randint(1000,1500))

        async def embed_daily(user, response) -> discord.Embed:
            credits = JM.load_server('WHX', user, False)
            embed = discord.Embed(description=response, color=discord.Color.random())
            embed.set_author(name=user.name, icon_url=user.display_avatar)
            embed.set_thumbnail(url=f"{self.user.display_avatar}")
            embed.add_field(name="Total Credits", value=credits)
            embed.set_footer(text="Claimed "+datetime.datetime.now().strftime('%m/%d/%Y'))
            return embed

        @self.bridge_command(name="lottery", guild_ids=[696122756072341616])
        async def lottery(ctx):

            today = await ret_lottery()

            if(JM.load_server('WHX', ctx.author, True)):
                credits = JM.load_server('WHX', ctx.author, False)
                if(credits < 50):
                    await ctx.respond("You need at least 50 credits to buy a lottery ticket!")
                else:
                    JM.save_to_server('WHX', ctx.author, int(credits) - 50)
                    lotticket = await gen_lottery(today)
                    winnings = 0
                    
                    if(lotticket[0] == 8):
                        credits = JM.load_server('WHX', ctx.author, False)
                        winnings = await int_lottery()
                        JM.save_to_server('WHX', ctx.author, int(credits)+winnings)
                        embed = await embed_lottery(ctx.author, lotticket, winnings)
                        sent = await ctx.respond(embed=embed)
                        message = await sent.original_response()
                        await message.add_reaction("🥳")
                        await message.add_reaction("🎉")
                               
                    else:
                        embed = await embed_lottery(ctx.author, lotticket)
                        await ctx.respond(embed=embed)
            else:
                await ctx.respond("You need at least 50 credits to buy a lottery ticket!")
                pass
            pass

        async def ret_lottery() -> str:
            now = datetime.datetime.now()
            year = now.year % 100
            month = now.month
            day = now.day

            a = string.ascii_uppercase[year % 26]
            b = string.ascii_uppercase[month % 26]
            c = string.ascii_uppercase[day % 26]
            d = string.ascii_uppercase[(year+month) % 26]
            e = string.ascii_uppercase[(month+day) % 26]
            f = string.ascii_uppercase[(year+day) % 26]
            g = string.ascii_uppercase[(year+month+day) % 26]
            h = string.ascii_uppercase[(day-month) % 26]

            result = f"{a}{b}{c}{d}{e}{f}{g}{h}"

            return result

        async def gen_lottery(today:str) -> tuple:
            spl = [*today]
            ticket = []
            count = 0
            for x in spl:
                rand = random.randint(1,2)
                if(rand == 1):
                    ticket.append(x)
                    count += 1
                else:
                    ticket.append(random.choice(string.ascii_uppercase))
            tikstr = ''.join(ticket)
            return (count, tikstr)
        
        async def embed_lottery(user, lottery_ticket:tuple, winnings:int = None):
            credits = JM.load_server('WHX', user, False)
            wintik = await ret_lottery()
            offby = 8-lottery_ticket[0]
            embed = discord.Embed(title="Lottery Ticket", description=f"`{lottery_ticket[1]}`", color=discord.Color.random())
            if(offby != 0):
                embed.set_author(name=user.name, icon_url=user.display_avatar)
                embed.set_thumbnail(url=f"{self.user.display_avatar}")
                embed.add_field(name="Total Credits", value=credits)
                embed.add_field(name="Winning Ticket", value=f"`{wintik}`", inline=True)
                embed.add_field(name="", value=f"You were {offby} letters off!", inline=False)
                embed.set_footer(text="Purchased on "+datetime.datetime.now().strftime('%m/%d/%Y'))    
            else:
                embed.title = "Winning Lottery Ticket"
                embed.set_author(name=user.name, icon_url=user.display_avatar)
                embed.set_thumbnail(url=f"{self.user.display_avatar}")
                embed.add_field(name="Total Credits", value=credits)
                embed.add_field(name="", value=f"Congratulations! You have won the lottery!\n {winnings} credits have been added to your balance.", inline=False)
                embed.set_footer(text="Purchased on "+datetime.datetime.now().strftime('%m/%d/%Y'))
            return embed                           
            

        async def int_lottery() -> int:
            return random.randint(20,30)*1000

        @self.event
        async def on_ready():
            print("The Dealer is up and running.")

        @self.event
        async def on_reaction_add(reaction, user):
            message = reaction.message
            if message.author == self.user:
                if reaction.emoji == "😭":
                    print("Reaction was added.")
                    async for user in reaction.users():
                        await reaction.remove(user)



d = Dealer()
d.run()