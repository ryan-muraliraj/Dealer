import discord, datetime, random, string, math
import constants, strings, bets
from jsonmanager import JSONManager
from coinflip import CoinFlipManager, CoinFlip

from discord.ext import bridge, commands

class Dealer(bridge.Bot):
    
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.presences = True
        intents.message_content = True
        self.jsonmanager = JSONManager()
        self.coinflipmanager = CoinFlipManager()
        self.betmanager = bets.BetManager()


        super().__init__(command_prefix="*", intents=intents, help_command=None)

        self.load_commands()

    def run(self):
        print("The Dealer is starting...")
        super().run(constants.get_discord_token(), reconnect=True)


    def load_commands(self):
        JM = self.jsonmanager
        CFM = self.coinflipmanager
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
                return (0,random.randint(300,400))
            elif(odds < 20):
                return (1,random.randint(500,700))
            else:
                return (2,random.randint(1200,1600))

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
        
        @self.slash_command(name="spinall")
        async def spin(ctx):
            togamble = 0
            if(JM.load_server('WHX', ctx.author, True)):
                togamble = JM.load_server('WHX', ctx.author, False)
                if(togamble < 100):
                    await ctx.respond(f"You do not have 100 credits to gamble.")
                else:
                    spinresult = await gen_spin(togamble)
                    JM.save_to_server('WHX',ctx.author,spinresult[1])
                    embed = await embed_spin(ctx.author, spinresult, togamble)
                    await ctx.respond(embed=embed)
            else:
                await ctx.respond("An error occured")
            
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
            multipliers = [0.4, 0.6, 0.8, 1, 1.2, 1.4, 2, 3, 4, 8, 16, 32]
            weights = [40,150,300,150,250,200,15,15,8,4,2,1]
            rand = random.choices(multipliers, weights=weights)
            multiplier = rand[0]
            winnings = math.ceil(multiplier*togamble)
            return (multiplier, winnings)

        async def embed_spin(user, spinresult : tuple, investment:int):
            credits = JM.load_server('WHX', user, False)
            net = ""
            netint = spinresult[1]-investment
            if(netint < 0):
                net = f"for a {abs(netint)} credit loss!"
            elif(netint > 0):
                net = f"for a {netint} net gain of credits!"
            else:
                net = "to break even!"
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


        @self.slash_command(name="coinflip")
        async def coinflip(ctx, call : discord.Option(str, description="Create the coinflip with your side already chosen", autocomplete=discord.utils.basic_autocomplete(["Heads","Tails"]), required=False, default=None) = None):
            if(not(call in ["Heads", "Tails", None])):
                await ctx.respond("That was not a valid coin side")
            else:
                id = CFM.create_cf() if call == None else CFM.create_cf((call, ctx.author))
                embed = await embed_coinflip()
                if(call == "Heads"):
                    embed = await embed_coinflip(player1=ctx.author)
                elif(call == "Tails"):
                    embed = await embed_coinflip(player2=ctx.author)
                else:
                    pass
                await ctx.respond(embed = embed, view = buttons_coinflip(id))
            
            pass
        #finish coinflip embed update when flip coin as well as denying player ability to assign themself to both outcomes.
        async def embed_coinflip(player1 = "", player2 = "", winner = False):
            embed = discord.Embed(title="Coinflip", description=f"Here is the coinflip!", color=discord.Color.dark_blue())
            if(not(winner)):
                embed.add_field(name="Heads", value=player1)
                embed.add_field(name="Tails", value=player2, inline=True)
            else:
                embed.set_author(name="Coinflip")
                embed.description = ""
                if(player1 == ""):
                    embed.title = f"The result is Tails. {player2} wins."
                else:
                    embed.title = f"The result is Heads. {player1} wins."
            return embed
            pass

        class buttons_coinflip(discord.ui.View):
            def __init__(self, id:int):
                self.cfid = id
                self.cf = CFM.get_cf(self.cfid)
                super().__init__(timeout = None)

            @discord.ui.button(label="Heads", style=discord.ButtonStyle.primary)
            async def heads_button_callback(self, button, interaction):
                if(self.cf.heads_taken() or self.cf.is_in(interaction.user.name)):
                    pass
                else:
                    self.cf.add_player(("Heads", interaction.user.name))
                    # await interaction.response.send_message(f"{interaction.user} locked in for Heads")
                    if(self.cf.is_full()):
                        embed = await embed_coinflip(interaction.user.name, self.cf.players["Tails"])
                        await interaction.response.defer()
                        print("trying to enable all")
                        self.enable_all_items()      
                        await interaction.edit_original_response(embed=embed, view=self)
                    else:
                        embed = await embed_coinflip(player1=interaction.user.name)
                        await interaction.response.defer()
                        await interaction.edit_original_response(embed=embed, view=self)
                        
                pass

            @discord.ui.button(label="Tails", style=discord.ButtonStyle.primary)
            async def tails_button_callback(self, button, interaction):
                if(self.cf.tails_taken() or self.cf.is_in(interaction.user.name)):
                    pass
                else:
                    self.cf.add_player(("Tails", interaction.user.name))
                    # await interaction.response.send_message(f"{interaction.user} locked in for Tails")
                    if(self.cf.is_full()):
                        embed = await embed_coinflip(self.cf.players["Heads"], interaction.user.name)
                        await interaction.response.defer()
                        self.enable_all_items()
                        await interaction.edit_original_response(embed=embed, view=self)
                    else:
                        embed = await embed_coinflip(player2=interaction.user.name)
                        await interaction.response.defer()
                        await interaction.edit_original_response(embed=embed, view=self)                    
                pass               


            @discord.ui.button(label="Flip Coin", style=discord.ButtonStyle.primary, disabled=True)
            async def flip_button_callback(self, button, interaction):
                result = self.cf.compute()
                embed = await embed_coinflip()
                if(result[0] == "Heads"):
                    embed = await embed_coinflip(player1=result[1], winner=True)
                else:
                    embed = await embed_coinflip(player2=result[1], winner=True)
                await interaction.response.defer()
                self.disable_all_items()
                await interaction.edit_original_response(embed=embed, view=self)
                pass            

        @self.command(name="test")
        async def test(ctx):
                print("a")
                await ctx.message.add_reaction("🗿")
                print("b")

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