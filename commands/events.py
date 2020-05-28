import discord, datetime, time
from discord.ext import commands
import asyncio
from itertools import cycle
import MySQLdb
from Setup import *

start_time = time.time()

def get_prefix(guild):
    db = MySQLdb.connect(host=sqhost, user=squname, passwd=sqpassword, db=sqdbname)
    cur = db.cursor()

    guildid = str(guild.id)
    sql = f"SELECT * FROM prefixes WHERE id={guildid}"  
    cur.execute(sql)
    prefix = cur.fetchone()[1]
    db.close()

    return prefix

def set_prefix(guild):
    db = MySQLdb.connect(host=sqhost, user=squname, passwd=sqpassword, db=sqdbname)
    cur = db.cursor()

    guildid = str(guild.id)
    sql = f"INSERT INTO prefixes VALUES ({guildid}, '{defprefix}')"
    cur.execute(sql)
    db.commit()
    db.close()

class events(commands.Cog):
    """
    Events and listeners for the bot
    """
    def __init__(self,client):
        
        self.client = client

   # @commands.Cog.listener()
   # async def on_message(self,msg):
#
   #     messagec : str = msg.content
#
 #       if msg.guild is None:
  #          return print(f'{msg.author}-{messagec}')

   #     if messagec.startswith('<@'):

    #        prefix = get_prefix(msg.guild)

    #        if self.client.user in msg.mentions:
      #          await msg.add_reaction('❤️')
     #           return await msg.channel.send(f'Hi! My prefix for this server is ``{prefix}``')
   
    @commands.command(help='Shows bot uptime')
    async def uptime(self, msg):
        current_time = time.time()
        difference = int(round(current_time - start_time)) 
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=msg.message.author.colour)
        embed.add_field(name="⏳Uptime", value=text)
        embed.set_author(name=f'{self.client.user}',icon_url=self.client.user.avatar_url)
        try:
            await msg.channel.send(embed=embed)
        except discord.HTTPException:
            await msg.channel.send(f'⏳ Ive Been up for: `{text}`')


    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        set_prefix(guild)

    @commands.Cog.listener()
    async def on_ready(self):

        print('\nDrizzi is Ready!')
        print(f'logged in as {self.client.user}\n')

        x = []

        for guilds in self.client.guilds:
            x.append(guilds)


        for guild in x:

            bruh = get_prefix(guild)

            if bruh is None:
                set_prefix(guild)
                print(f'[CONSOLE] Sucsessfully set prefix in {guild.name}')
                
            else:
                print(f"""[CONSOLE] Guild '{guild.name}' has a prefix: {bruh}""")

        statuses = [f'over {len(set(self.client.get_all_members()))} users!', f'over {len(self.client.guilds)} guilds!']

        msgs = cycle(statuses)

        running = True

        while running:
            current_status = next(msgs)
            await self.client.change_presence(status=discord.Status.online, activity=discord.Activity(name=current_status ,type=3))
            await asyncio.sleep(10)

    
def setup(client):
    client.add_cog(events(client))
