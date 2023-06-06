import discord, datetime, random, string, math
import constants, strings, bets
from jsonmanager import JSONManager

from discord.ext import bridge, commands

class Dealer(bridge.Bot):
    
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.presences = True
        intents.message_content = True
        self.jsonmanager = JSONManager()
        self.betmanager = bets.BetManager()

        super().__init__(command_prefix="*", intents=intents, help_command=None)

        self.load_commands()

    def run(self):
        print("The Dealer is starting...")
        super().run(constants.get_discord_token(), reconnect=True)


    def load_commands(self):
        JM = self.jsonmanager
        BM = self.betmanager

        @self.slash_command(name="profile")
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
                embed = discord.Embed(title=user, description=f"Credits: {credits}", color=discord.Color.dark_blue())
                embed.set_author(name="Profile")
                embed.set_thumbnail(url=f"{user.display_avatar}")
                embed.set_footer(text=datetime.datetime.now().strftime('%m/%d/%Y'))
                return embed

        @self.bridge_command(name="daily")
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
            embed = discord.Embed(description=response, color=discord.Color.dark_blue())
            embed.set_author(name=user.name, icon_url=user.display_avatar)
            embed.set_thumbnail(url=f"{self.user.display_avatar}")
            embed.add_field(name="Total Credits", value=credits)
            embed.set_footer(text="Claimed "+datetime.datetime.now().strftime('%m/%d/%Y'))
            return embed

        @self.bridge_command(name="lottery")
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
            embed = discord.Embed(title="Lottery Ticket", description=f"`{lottery_ticket[1]}`", color=discord.Color.dark_blue())
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

        @self.slash_command(name="spin")
        async def spin(ctx, amount : discord.Option(int, "Enter an amount to put into the spin", required=False, default=None) = None):
            togamble = 0
            if(amount == None):
                togamble = 100
                await process_spin(ctx, togamble)
            elif(amount < 100):
                await ctx.respond("You must put at least 100 credits into a spin.")
            else:
                togamble = amount
                await process_spin(ctx, togamble)
                pass
            pass
        
        async def process_spin(ctx, togamble):
            if(JM.load_server('WHX', ctx.author, True)):
                credits = JM.load_server('WHX', ctx.author, False)
                if(credits < togamble):
                    await ctx.respond(f"You do not have {togamble} credits to gamble.")
                else:
                    spinresult = await gen_spin(togamble)
                    JM.save_to_server('WHX',ctx.author,credits-togamble+spinresult[1])
                    embed = await embed_spin(ctx.author, spinresult, togamble)
                    await ctx.respond(embed=embed)
                    pass
            else:
                await ctx.respond("You need at least 100 credits to spin.")
            
        async def gen_spin(togamble:int) -> tuple:
            rand = random.randint(1,500)
            multiplier = 0
            if (rand <= 250):
                multiplier = 0.6
            elif (rand <= 300):
                multiplier = 0.8
            elif (rand <= 400):
                multiplier = 1
            elif (rand <= 470):
                multiplier = 1.2
            elif (rand <= 480):
                multiplier = 1.4
            elif (rand <= 495):
                multiplier = 2
            elif (rand == 496):
                multiplier = 3
            elif (rand == 497):
                multiplier = 4
            elif (rand == 498):
                multiplier = 8
            elif (rand == 499):
                multiplier = 16
            elif (rand == 500):
                multiplier = 32
            else:
                multiplier = 1
            winnings = math.ceil(multiplier*togamble)
            return (multiplier, winnings)

        async def embed_spin(user, spinresult : tuple, investment:int):
            credits = JM.load_server('WHX', user, False)
            net = ""
            netint = spinresult[1]-investment
            if(netint < 0):
                net = f"for a {abs(netint)} loss of credits!"
            elif(netint > 0):
                net = f"for a {netint} return on credits!"
            else:
                net = "to cut even!"
            embed = discord.Embed(description=f"You landed on {spinresult[0]}x {net}", color=discord.Color.dark_blue())
            embed.set_author(name=user.name, icon_url=user.display_avatar)
            embed.set_thumbnail(url=f"{self.user.display_avatar}")
            embed.add_field(name="Spent", value=investment)
            embed.add_field(name="Won", value=spinresult[1], inline=True)
            embed.add_field(name="Total Credits", value=credits, inline=False)
            embed.set_footer(text="Gamblers are always 1 spin away from hitting big!")
            return embed           
        
        @self.bridge_command(name="leaderboard")
        async def leaderboard(ctx):
            server = JM.load_all('WHX')
            server = sorted(server.items(), key = lambda item:item[1], reverse=True)
            embed = discord.Embed(title="Leaderboard", description=f"These are the top five gamblers in WHX:", color=discord.Color.dark_blue())
            embed.set_author(name="WHX")
            embed.set_thumbnail(url=f"{self.user.display_avatar}")
            embed.set_footer(text=datetime.datetime.now().strftime('%m/%d/%Y'))       
            z = 1     
            for x,y in server[:5]:
                embed.add_field(name="", value=f"**{z}.** {x}: `{y} credits`", inline = False)
                z+=1
            await ctx.respond(embed=embed)

        @self.slash_command(name="bet")
        async def bet(ctx, title: discord.Option(str, "Enter a title for the bet", required = True)):
            embed = await embed_bet(title)
            betid = BM.create_bet(title)
            await ctx.respond(embed=embed, view=buttons_bet(betid))
        
        async def embed_bet(title):
            embed = discord.Embed(title=title, description="The bets are on.", color=discord.Color.dark_blue())
            embed.set_thumbnail(url=f"{self.user.display_avatar}")
            return embed

        class buttons_bet(discord.ui.View):
            def __init__(self, betid:int):
                self.betid = betid
                super().__init__(timeout=None)

            @discord.ui.button(label="Join Bet", style=discord.ButtonStyle.success)
            async def jb_button_callback(self, button, interaction):
                await interaction.response.defer()
                embed = discord.Embed(description="asdfadsf")
                await interaction.edit_original_response(embed=embed)
                # await interaction.response.send_message(view=select_bet(self.betid), ephemeral=True)
            
            # @discord.ui.button(label="Lock Bet", style=discord.ButtonStyle.danger, disabled=True)
            # async def lb_button_callback(self, button, interaction):
            #     await interaction.response.send_message("WOOO")

            @discord.ui.button(label="Check Outcomes", style=discord.ButtonStyle.primary)
            async def co_button_callback(self, button, interaction):
                bet = BM.get_bet(self.betid)
                outcomes = bet.get_outcomes()
                for x in outcomes:
                    print(x.title, x.id)
                await interaction.response.send_message("Printed outcomes to console.")
            
            @discord.ui.button(label="Add Outcome", style=discord.ButtonStyle.primary)
            async def ao_button_callback(self, button, interaction):
                await interaction.response.send_modal(modal_outcome(self.betid, title="Add Outcome"))

        class select_bet(discord.ui.View):
            def __init__(self, betid:int):
                self.betid = betid
                super().__init__()

            @discord.ui.select( # the decorator that lets you specify the properties of the select menu
            placeholder = "What outcome would you like to bet on?", # the placeholder text that will be displayed if nothing is selected
            min_values = 1, # the minimum number of values that must be selected by the users
            max_values = 1, # the maximum number of values that can be selected by the users
            options = [ # the list of options from which users can choose, a required field
                discord.SelectOption(
                    label="Sentinels win 2-1",
                    value = '0',
                    description="possible 1.5x return"
                ),
                discord.SelectOption(
                    label="NRG win 2-0",
                    value = '1',
                    description="possible 1.1x return"
                ),
                discord.SelectOption(
                    label="Sentinels win 2-0",
                    value = '2',
                    description="possible 2.7x return"
                )
            ]
            )
            async def select_callback(self, select, interaction): # the function called when the user is done selecting options
                #await interaction.response.send_message(f"Awesome! I like {index} too!", ephemeral=True)      
                await interaction.response.send_modal(modal_bet(title=select.values[0]))      

        class modal_bet(discord.ui.Modal):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)
                self.add_item(discord.ui.InputText(label="How much would you like to bet?", required=True, placeholder="100", min_length=3))

            async def callback(self, interaction: discord.Interaction):
                embed = discord.Embed(title="Modal Results")
                embed.add_field(name="Short Input", value=self.children[0].value)
                await interaction.response.send_message(embed=embed)            

        class modal_outcome(discord.ui.Modal):
            def __init__(self, betid:int, *args, **kwargs) -> None:
                self.betid = betid
                super().__init__(*args, **kwargs)
                self.add_item(discord.ui.InputText(label="What is the title of the outcome?", required=True))

            async def callback(self, interaction: discord.Interaction):
                bet = BM.get_bet(self.betid)
                bet.add_outcome(self.children[0].value)
                embed = discord.Embed(title="Modal Results")
                embed.add_field(name="Short Input", value=self.children[0].value)
                await interaction.response.send_message(embed=embed) 

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