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
        
        if usr.bot:
            return

        try:
            loggerdata = blutapi.getlogdata(afv.channel.guild)
        except Exception as err:
            loggerdata = blutapi.getlogdata(bfv.channel.guild)

        if loggerdata[1]:
            pass
        else:
            return


        if afv.channel == bfv.channel:
            pass
        else:
            
            emb1 = discord.Embed(title = f'{usr}',timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern')),colour=0x36393F)
            emb2 = discord.Embed(title = f'{usr}',timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern')),colour=0x36393F)
            emb3 = discord.Embed(title = f'{usr}',timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern')),colour=0x36393F)


            emb1.add_field(name = "User changed voice channels", value = f"*{bfv.channel}* -> *{afv.channel}*")
            emb2.add_field(name = "User left a voice channel", value = f"{bfv.channel}")
            emb3.add_field(name = "User joined a voice channel", value = f"{afv.channel}")

            emb1.set_thumbnail(url=usr.avatar_url)
            emb2.set_thumbnail(url=usr.avatar_url)
            emb3.set_thumbnail(url=usr.avatar_url)
            
            try:
                channel = get(bfv.channel.guild.channels, id=loggerdata[2])
                if afv.channel is None:
                    return await channel.send(embed=emb2)
                else:
                    return await channel.send(embed=emb1)
            except:
                channel = get(afv.channel.guild.channels, id=loggerdata[2])
                return await channel.send(embed=emb3)
         

        if afv.mute == bfv.mute:
            pass
        else:
            if afv.mute:

                emb = discord.Embed(
                title = f'{usr}',
                description = 'User server muted',
                timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern')),
                colour=0x36393F
                )
                emb.set_thumbnail(url=usr.avatar_url)
                
            else:
                
                emb = discord.Embed(
                title = f'{usr}',
                description = 'User was Unserver-muted',
                timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern')),
                colour=0x36393F
                )
                emb.set_thumbnail(url=usr.avatar_url)

            try:
                channel = get(bfv.channel.guild.channels, id=loggerdata[2])
                await channel.send(embed = emb)   
                return
            except Exception as err: 
                print(err)
                return
              

        if afv.deaf == bfv.deaf:
            pass
        else:
            if afv.deaf:

                emb = discord.Embed(
                title = f'{usr}',
                description = 'User was server Deafened',
                timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern')),
                colour=0x36393F
                )
                emb.set_thumbnail(url=usr.avatar_url)
                
            else:
                
                emb = discord.Embed(
                title = f'{usr}',
                description = 'User was Unserver-deafened',
                timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern')),
                colour=0x36393F
                )
                emb.set_thumbnail(url=usr.avatar_url)
            try:
                channel = get(bfv.channel.guild.channels, id=loggerdata[2])
                await channel.send(embed = emb)   
                return
            except Exception as err: 
                print(err)
                return

    @commands.Cog.listener()
    async def on_message_delete(self, msg):

        if msg.author.bot:

            return

        loggerdata = blutapi.getlogdata(msg.guild)

        if loggerdata[1]:
            pass
        else:
            return

        emb = discord.Embed(
            title=f'{msg.guild}',
            description=f'A message was deleted in {msg.channel.mention}',
            colour=0x36393F,
            timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
        )

        emb.add_field(name='Message Deleted',value=f'{msg.content}',inline=True)
        emb.add_field(name='Message Author',value=f'{msg.author.mention}',inline=True)
        emb.set_footer(text=f'Msg ID: {msg.id}')
        emb.set_thumbnail(url=msg.author.avatar_url)

        try:
            chan : discord.TextChannel = get(msg.guild.channels, id=loggerdata[2])
            await chan.send(embed=emb)
        except Exception as err:
            print(err)
            return
      
    @commands.Cog.listener()
    async def on_message_edit(self,bmsg,amsg):
                
        if amsg.content == bmsg.content:
            return

        if bmsg.author.bot:
            return

        loggerdata = blutapi.getlogdata(bmsg.guild)

        if loggerdata[1]:
            pass
        else:
            return

        if amsg.author == self.client.user:
            return

        emb = discord.Embed(
            title=f'{bmsg.author}',
            description=f'A message was edited in {bmsg.channel.mention}',
            colour=0x36393F,
            timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
        )

        emb.add_field(name='Before',value=f'{bmsg.content}',inline=True)
        emb.add_field(name='After',value=f'{amsg.content}',inline=True)
        emb.set_footer(text=f'Msg ID: {bmsg.id}')
        emb.set_thumbnail(url=bmsg.author.avatar_url)
    
        try:
            chan : discord.TextChannel = get(bmsg.guild.channels, id=loggerdata[2])
            await chan.send(embed=emb)
        except Exception as err:
            print(err)
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
            colour=0x36393F,
            timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
        )

        emb.set_thumbnail(url=banmember.avatar_url)
        emb.add_field(name='Reason', value=f'{reason}')

        try:
            chan : discord.TextChannel = get(guild.channels, id=loggerdata[2])
            await chan.send(embed=emb)
        except Exception as err:
            print(err)
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
            colour=0x36393F,
            timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
        )

        emb.set_thumbnail(url=banmember.avatar_url)
        emb.add_field(name='Reason for initial ban', value=f'{reason}')

        try:
            chan : discord.TextChannel = get(guild.channels, id=loggerdata[2])
            await chan.send(embed=emb)
        except Exception as err:
            print(err)
            return

def setup(client):
    client.add_cog(logger(client))
