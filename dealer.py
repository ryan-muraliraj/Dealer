import discord, datetime
import constants, JSONmanager

from discord.ext import bridge, commands

class Dealer(bridge.Bot):
    
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.presences = True
        intents.message_content = True
        self.jsonmanager = JSONmanager.Manager()

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

        async def ret_profile(ctx, user):
            puser = ctx.author
            if not(user is None):
                puser = user
            if(JM.load_server('WHX', puser, True)):
                credits = JM.load_server('WHX', puser, False)
                embed = discord.Embed(title=puser, description=f"Credits: {credits}", color=discord.Color.random())
                embed.set_author(name="Profile")
                embed.set_thumbnail(url=f"{puser.display_avatar}")
                embed.set_footer(text=datetime.datetime.now().strftime('%m/%d/%Y'))
                if(type(ctx) is commands.Context):
                    await ctx.reply(embed=embed)
                else:
                    await ctx.respond(embed=embed)
            else:
                if(type(ctx) is commands.Context):
                    await ctx.reply("That user was not found or has zero credits.")
                else:
                    await ctx.respond("That user was not found or has zero credits.")

        @self.bridge_command(name="daily", guild_ids=[696122756072341616])
        async def daily(ctx):
            var = JM.daily('WHX', ctx.author)
            if not(type(var) is int):
                result = datetime.timedelta(hours=24)-var
                minutes = (result.seconds % 3600) // 60
                hours = (result.seconds // 3600)
                await ctx.respond(f"You can claim your daily in {hours} hours and {minutes} minutes.")
            else:
                if(JM.load_server('WHX', ctx.author, True)):
                    credits = JM.load_server('WHX', ctx.author, False)
                    JM.save_to_server('WHX', ctx.author, int(credits) + var)
                else:
                    JM.save_to_server('WHX', ctx.author, var)
                await ctx.respond(f"Daily claimed! {var} credits added to balance. Come back in 24 hours.")

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