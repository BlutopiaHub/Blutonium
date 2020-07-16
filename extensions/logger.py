import discord
from discord.ext import commands
from discord.utils import get
import blutapi, os, datetime,pytz
from Setup import *


    
class logger(commands.Cog,name='Logger'):
    """
    Listeners for logging 
    """
    def __init__(self, client : commands.Bot):
        self.client = client
        self.qualified_name
        
    @commands.Cog.listener()
    async def on_voice_state_update(self,usr : discord.Member,bfv : discord.VoiceState,afv:discord.VoiceState):


        try:
            loggerdata = blutapi.getlogdata(afv.channel.guild)
        except:
            loggerdata = blutapi.getlogdata(bfv.channel.guild)

        if loggerdata[1]:
            pass
        else:
            return


        if afv.channel == bfv.channel:
            pass
        else:
            emb = discord.Embed(
                title = f'{usr}',
                description = 'User changed voice channels',
                timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
            )

            emb.add_field(name = "Update", value = f"**{bfv.channel}** -> **{afv.channel}**")
            emb.set_thumbnail(url=usr.avatar_url)
            try:   
                channel = get(bfv.channel.guild.channels, id=loggerdata[2])
                await channel.send(embed = emb)
                return
            except:
                return

        if afv.mute == bfv.mute:
            pass
        else:
            if afv.mute:

                emb = discord.Embed(
                title = f'{usr}',
                description = 'User server muted',
                timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
                )
                emb.set_thumbnail(url=usr.avatar_url)
                
            else:
                
                emb = discord.Embed(
                title = f'{usr}',
                description = 'User was Unserver-muted',
                timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
                )
                emb.set_thumbnail(url=usr.avatar_url)

            try:
                channel = get(bfv.channel.guild.channels, id=loggerdata[2])
                await channel.send(embed = emb)   
                return
            except: 
                return
              

        if afv.deaf == bfv.deaf:
            pass
        else:
            if afv.deaf:

                emb = discord.Embed(
                title = f'{usr}',
                description = 'User was server Deafened',
                timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
                )
                emb.set_thumbnail(url=usr.avatar_url)
                
            else:
                
                emb = discord.Embed(
                title = f'{usr}',
                description = 'User was Unserver-deafened',
                timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
                )
                emb.set_thumbnail(url=usr.avatar_url)
            try:
                channel = get(bfv.channel.guild.channels, id=loggerdata[2])
                await channel.send(embed = emb)   
                return
            except: 
                return

    @commands.Cog.listener()
    async def on_message_delete(self, msg):

        loggerdata = blutapi.getlogdata(msg.guild)

        if loggerdata[1]:
            pass
        else:
            return

        emb = discord.Embed(
            title=f'{msg.guild}',
            description=f'A message was deleted',
            colour= discord.Colour.red(),
            timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
        )

        emb.add_field(name='Message Deleted',value=f'{msg.content}',inline=True)
        emb.add_field(name='Message Author',value=f'{msg.author}',inline=True)
        emb.set_thumbnail(url=msg.author.avatar_url)

        try:
            chan : discord.TextChannel = get(msg.guild.channels, id=loggerdata[2])
            await chan.send(embed=emb)
        except:
            return
      
    @commands.Cog.listener()
    async def on_message_edit(self,bmsg,amsg):

        loggerdata = blutapi.getlogdata(bmsg.guild)

        if loggerdata[1]:
            pass
        else:
            return


        if amsg.author == self.client.user:
            return

        emb = discord.Embed(
            title=f'{bmsg.author}',
            description=f'A message was edited',
            colour=discord.Colour.blue(),
            timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
        )

        emb.add_field(name='Before',value=f'{bmsg.content}',inline=True)
        emb.add_field(name='After',value=f'{amsg.content}',inline=True)
        emb.set_thumbnail(url=bmsg.author.avatar_url)
    
        try:
            chan : discord.TextChannel = get(bmsg.guild.channels, id=loggerdata[2])
            await chan.send(embed=emb)
        except:
            return

    @commands.Cog.listener()
    async def on_member_ban(self,guild,banmember):

        loggerdata = blutapi.getlogdata(guild)

        if loggerdata[1]:
            pass
        else:
            return

        bans = await guild.bans()

        Member_name, Member_disc = str(banmember).split('#')

        for ban in bans:
            user = ban.user

            if (user.name, user.discriminator) == (Member_name, Member_disc):

                reason = ban.reason

        emb = discord.Embed(
            title=f'{banmember}',
            description=f'**Member was banned from {guild}**',
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
        )

        emb.set_thumbnail(url=banmember.avatar_url)
        emb.add_field(name='Reason', value=f'{reason}')

        try:
            chan : discord.TextChannel = get(guild.channels, id=loggerdata[2])
            await chan.send(embed=emb)
        except:
            return

    @commands.Cog.listener()
    async def on_member_unban(self,guild, banmember):

        loggerdata = blutapi.getlogdata(guild)

        if loggerdata[1]:
            pass
        else:
            return
            
        bans = await guild.bans()

        Member_name, Member_disc = str(banmember).split('#')

        for ban in bans:
            user = ban.user

            if (user.name, user.discriminator) == (Member_name, Member_disc):

                reason = ban.reason

        emb = discord.Embed(
            title=f'{banmember}',
            description=f'**Member was unbanned from {guild}**',
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
        )

        emb.set_thumbnail(url=banmember.avatar_url)
        emb.add_field(name='Reason for initial ban', value=f'{reason}')

        try:
            chan : discord.TextChannel = get(guild.channels, id=loggerdata[2])
            await chan.send(embed=emb)
        except:
            return


def setup(client):
    client.add_cog(logger(client))
