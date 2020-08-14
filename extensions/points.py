from discord.ext import commands
import discord, blutapi, pytz
from discord.utils import get
from dateutil.relativedelta import relativedelta
from random import randrange
from Setup import *
import datetime

def getuser(msg,inp):

    try:
        member = get(msg.guild.members, id=int(inp))
            
    except:

        if inp:
            try:
                member = get(msg.guild.members, name=inp)
                    
            except:
                member = get(msg.guild.members, display_name=inp)

        if  inp is None:
            member : discord.Member = msg.author
        else:
            for men in msg.message.mentions:
                member = men
    return member


class points(commands.Cog,name="Points"):

    """
    Fun Game Where you acumulate points to gamble them! (Not responsible for sudden gambling addictions)
    """

    def __init__(self,client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def setpoints(Self,ctx,ammount,*,user = None):

        user = getuser(ctx,user)

        ammount = int(ammount)
        blutapi.setpoints(user,ammount)
        await ctx.send(f"successfully set {user} to {ammount} points")

    @commands.command(aliases=["givepoints","give"])
    async def gift(self, ctx,ammount, *, user=None):

        user = getuser(ctx,user)

        ammount = int(ammount)

        gifterpoints = int(blutapi.getpoints(ctx.author))
        recepoints = int(blutapi.getpoints(user))

        if user == ctx.author:
            return await ctx.send("You cant gift yourself points")

        if gifterpoints < ammount:
            return await ctx.send("You dont have enough points to gift that.")  

        if ammount == 0:
            return await ctx.send("You cant gift 0 points")

        if ammount < 0:
            return await ctx.send("You Cant gift - points nub")

        gnewpoints = gifterpoints - int(ammount)
        rnewpoints = recepoints + ammount

        try:
            blutapi.setpoints(ctx.author,gnewpoints)
            blutapi.setpoints(user, rnewpoints)
            await ctx.send("Transaction Sucessful!")
        except Exception as err:
            await ctx.send(f"Transaction failed : {err}")

    @commands.command() 
    @commands.is_owner()
    async def reset(self,ctx,*,user=None):

        user = getuser(ctx,user)

        blutapi.setpoints(user, 0)

        await ctx.send(f"Successfuly reset {user}")

    @commands.command(help="Display your points",aliases=["balance", "bal"])
    async def points(self,ctx,param=None):

        init = blutapi.getpoints(ctx.author)

        if param is None:
            points = init
        elif param == "half":
            points = init/2
        elif param == "quart":
            points = init/4
        elif param == "eighth":
            points = init/8

        points = int(points)

        await ctx.send(f"You have `{points}` points")

    @commands.command(help="help feed your gambling addiction ")
    async def gamble(self,ctx, ammount):

        user = ctx.author
        startingpoints = int(blutapi.getpoints(user))
        chance = randrange(0,2)
        ammount = ammount.lower()

        if ammount == "all":
            ammount = startingpoints

        if ammount == "half":
            ammount = startingpoints/2

        if ammount == "quart":
            ammount = startingpoints/4
        
        if ammount == "eighth":
            ammount = startingpoints/8

        ammount = int(ammount)

        if ammount == 0:
            return await ctx.send("You cant gamble 0 points")
        
        if ammount > startingpoints:
            return await ctx.send("You cant gamble more than you have!")

        if ammount < 0:
            return await ctx.send("You cant gamble - points nub")

        if chance:
            newpoints = ammount + startingpoints
            
            if ammount == startingpoints:
                await ctx.send(f"You went all in and WON! You now have `{newpoints}` points")
            else:
                await ctx.send(f"You gambled `{ammount}` and WON! You now have `{newpoints}` points")

        else:
            newpoints = startingpoints - ammount

            if ammount == startingpoints:
                await ctx.send(f"You went all in and lost everything LMAO. You now have `{newpoints}` points")
            else: 
                await ctx.send(f"You gambled `{ammount}` And lost it all lol. You now have `{newpoints}` points")

        blutapi.setpoints(user, newpoints)

    @commands.command(help="claim your daily points")
    async def daily(self,ctx):

        isClaimed = blutapi.getclaimed(ctx.author)

        print(isClaimed[0])

        if not isClaimed[0]:
            
            now = datetime.datetime.now()
            nextclaimDelta = relativedelta(now,isClaimed[1])
            
            nextclaim = f"You can claim your points again in **{abs(nextclaimDelta.hours)} hours, {abs(nextclaimDelta.minutes)} minutes, {abs(nextclaimDelta.seconds)} seconds.**"

            await ctx.send(nextclaim)

        else:

            points = int(blutapi.getpoints(ctx.author))
            points = points + 100

            blutapi.setpoints(ctx.author,points)

            await ctx.send('You have claimed your daily **100 points**')


    @commands.command(help="Shows the server leaderboard for points", aliases=["lb", "baltop"])
    async def leaderboard(self,ctx:commands.Context):
        
        lb = blutapi.getleaderboard(ctx.guild)

        emb = discord.Embed(title=f'{ctx.guild} Leaderboard',timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern')),colour=0x36393F)
        emb.set_thumbnail(url=ctx.guild.icon_url)

        q = 1

        for x in lb:

            user = getuser(ctx,x[0])

            emb.add_field(name=f"#{q} - {user}",value=f'{x[1]} Points', inline=False)

            q += 1

        await ctx.send(embed=emb)


def setup(client):
    client.add_cog(points(client))