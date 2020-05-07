import discord, datetime, time
from discord.ext import commands
import asyncio
from itertools import cycle

start_time = time.time()

class events(commands.Cog):
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
        embed = discord.Embed(colour=msg.message.author.colour)
        embed.add_field(name="⏳Uptime", value=text)
        embed.set_author(name=f'{self.client.user}',icon_url=self.client.user.avatar_url)
        try:
            await msg.channel.send(embed=embed)
        except discord.HTTPException:
            await msg.channel.send(f'⏳ Ive Been up for: `{text}`')

    @commands.Cog.listener()
    async def on_ready(self):

        statuses = [f'over {len(set(self.client.get_all_members()))} users!', f'over {len(self.client.guilds)} guilds!']

        msgs = cycle(statuses)

        running = True

        while running:
            current_status = next(msgs)
            await self.client.change_presence(status=discord.Status.online, activity=discord.Activity(name=current_status ,type=3))
            await asyncio.sleep(10)

def setup(client):
    client.add_cog(events(client))
