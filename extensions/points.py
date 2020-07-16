from discord.ext import commands
import discord
import MySQLdb
from random import randrange
from Setup import *
import datetime

def get_users():
    db = MySQLdb.connect(host=sqhost, user=squname, passwd=sqpassword, db=sqdbname)
    cur = db.cursor()

    sql = "SELECT id FROM points"
    cur.execute(sql)

    query = cur.fetchall()
    ids = []
    
    for x in query:
        ids.append(x[0])
    db.close()

    return ids

def get_points(id):
    db = MySQLdb.connect(host=sqhost, user=squname, passwd=sqpassword, db=sqdbname)
    cur = db.cursor()

    sql = f"SELECT points FROM points where id = {id}"

    res = cur.execute(sql)
    points = cur.fetchone()

    if points is None:
        points = [0,"lol" ]
        sql = f"INSERT INTO points Values ({id}, 0)"
        cur.execute(sql)
        db.commit()
        db.close()

    return points[0]

def set_points(id,ammount):
    db = MySQLdb.connect(host=sqhost, user=squname, passwd=sqpassword, db=sqdbname)
    cur = db.cursor()

    sql = f"UPDATE points SET points = {ammount} where id = {id}"   

    res = cur.execute(sql) 
    db.commit()
    db.close()
    
def get_daily(id):
    db = MySQLdb.connect(host=sqhost, user=squname, passwd=sqpassword, db=sqdbname)
    cur = db.cursor()

    sql = f"SELECT prev FROM daily WHERE id = {id}"

    res = cur.execute(sql)
    prev = cur.fetchone()
    today = datetime.datetime.today().strftime('%y%m%d')

    if prev is None:
        prev = [22,23]
        sql = f"INSERT INTO daily VALUES ({id}, {today})"
        cur.execute(sql)
       
    sql = f"UPDATE daily SET prev = {today} where id = {id}"
    cur.execute(sql)
       
    db.commit()
    db.close()

    return prev[0]

class points(commands.Cog,name="Points"):

    """
    Fun Game Where you acumulate points to gamble them! (Not responsible for sudden gambling addictions)
    """

    def __init__(self,client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def setpoints(Self,ctx,user:discord.Member,ammount):

        ammount = int(ammount)
        set_points(user.id,ammount)
        await ctx.send(f"successfully set {user} to {ammount} points")

    @commands.command()
    async def gift(self, ctx, user:discord.Member, ammount):

        ammount = int(ammount)

        gifterpoints = int(get_points(ctx.author.id))
        recepoints = int(get_points(user.id))

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
            set_points(ctx.author.id,gnewpoints)
            set_points(user.id, rnewpoints)
            await ctx.send("Transaction Sucessful!")
        except Exception as err:
            await ctx.send(f"Transaction failed : {err}")

    @commands.command() 
    @commands.is_owner()
    async def reset(self,ctx,user:discord.Member):

        set_points(user.id, 0)

        await ctx.send(f"Successfuly reset {user}")

    @commands.command(help="Display your points")
    async def points(self,ctx,param=None):

        init = get_points(ctx.author.id)

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

        userid = ctx.author.id
        startingpoints = int(get_points(userid))
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

        set_points(userid, newpoints)

    @commands.command(help="claim your daily points")
    async def daily(self,ctx):

        authorid = ctx.author.id

        prev = get_daily(authorid)
        today = int(datetime.datetime.today().strftime('%y%m%d'))

        if prev == today:
            print("True")
        
        if prev == today:
            await ctx.send(f"You have already claimed your daily points!")
        else:
            prevpoints = get_points(authorid)
            newpoints = prevpoints + 100
            set_points(authorid, newpoints)

            await ctx.send("You have been awarded your daily 100 points!")

    @commands.command(help="Shows the server leaderboard for points", aliases=["lb"])
    async def leaderboard(self,ctx:commands.Context):
        
        guild : discord.Guild = ctx.guild
        members = []

        for member in guild.members[0:50]:

            members.append((str(member), get_points(member.id)))

        def takesecond(elem):
            return elem[1]

        members.sort(key=takesecond,reverse=True)

        emb = discord.Embed()

        for x in members:
            if x[1]==0:
                pass 
            else:
                emb.add_field(name=x[0],value=f'{x[1]} points',inline=False)

        await ctx.send(embed=emb)

def setup(client):
    client.add_cog(points(client))