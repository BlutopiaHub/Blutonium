import discord, datetime, time
from discord.ext import commands
import asyncio, pytz
from itertools import cycle
import blutapi
from Setup import *

start_time = time.time()

class events(commands.Cog,name='Events'):
    """
    Events and listeners for the bot
    """
    def __init__(self,client):
        
        self.client = client
   
    @commands.command(help='Shows bot uptime')
    async def uptime(self, msg):
        current_time = time.time()
        difference = int(round(current_time - start_time)) 
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=msg.message.author.colour, timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern')))
        embed.add_field(name="⏳Uptime", value=text)
        embed.set_author(name=f'{self.client.user}',icon_url=self.client.user.avatar_url)
        try:
            await msg.channel.send(embed=embed)
        except discord.HTTPException:
            await msg.channel.send(f'⏳ Ive Been up for: `{text}`')

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        res = await blutapi.genguilddata(guild)
        print(res)

    @commands.Cog.listener()
    async def on_ready(self):

        for guild in self.client.guilds:

            res = await blutapi.genguilddata(guild)

            print(res)
            
        statuses = [f'over {len(set(self.client.get_all_members()))} users!', f'over {len(self.client.guilds)} guilds!','Forgot your prefix? @mention me!', 'over your mind']


        displaying = cycle(statuses)

        running = True

        print('\nBlutonium is operational!')
        print(f'logged in as {self.client.user}\n')

        while running:
            current_status = next(displaying)
            await self.client.change_presence(status=discord.Status.online, activity=discord.Activity(name=current_status ,type=3))
            await asyncio.sleep(20)

def setup(client):
    client.add_cog(events(client))
