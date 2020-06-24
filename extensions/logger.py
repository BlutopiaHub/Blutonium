import discord
from discord.ext import commands
from discord.utils import get
import os 
import MySQLdb
from Setup import *


def Checker(**permissions):
    original = commands.has_permissions(**permissions).predicate
    async def extended(ctx):
        if ctx.guild is None:
            return False
        return commands.is_owner() or await original(ctx)
    return commands.check(extended)

def getlogdata(guild):

    db = MySQLdb.connect(host=sqhost, user=squname, passwd=sqpassword, db=sqdbname)
    cur = db.cursor()

    guildid = str(guild.id)
    sql = f"SELECT * FROM logs WHERE id={guildid}"
    cur.execute(sql)
    data = cur.fetchone()

    if data is None:
        chan = get(guild.channels, name='logs')
        if chan is None:
            chanid = 0000000000000000000
        else:
            chanid = chan.id
        sql = f"INSERT INTO logs VALUES ({guildid}, True,{chanid})"
        cur.execute(sql)
        data = (guildid,True,chanid)

    db.commit()
    db.close()

    return data

def togglelogs(guild):

    db = MySQLdb.connect(host=sqhost, user=squname, passwd=sqpassword, db=sqdbname)
    cur = db.cursor()

    guildid = str(guild.id)
    sql = f"SELECT enabled FROM logs WHERE id={guildid}"
    cur.execute(sql)

    islogs = cur.fetchone()[0]

    if islogs:
        sql = f"UPDATE logs SET enabled = False WHERE id = {guildid}"
        cur.execute(sql)
        db.commit()
        
    else:
        sql = f"UPDATE logs SET enabled = True WHERE id = {guildid}"
        cur.execute(sql)
        db.commit()

    sql = f"SELECT enabled FROM logs WHERE id={guildid}"
    cur.execute(sql)

    islogs = cur.fetchone()[0]    

    db.close()

    return islogs  

def setlogchannel(guild,channelid):

    db = MySQLdb.connect(host=sqhost, user=squname, passwd=sqpassword, db=sqdbname)
    cur = db.cursor()   

    guildid = str(guild.id)
    sql = f"UPDATE logs SET channel={channelid} WHERE id = {guildid}"
    cur.execute(sql)

    db.commit()
    db.close()

    return 0
    
class logger(commands.Cog,name='Logger'):
    """
    Listeners for logging (Make a channel called logs!)
    """
    def __init__(self, client : commands.Bot):
        self.client = client
        self.qualified_name

    @commands.command(help="Set the logs channel")
    @commands.has_permissions(manage_channels=True)
    async def logchannel(self,ctx,channel:discord.TextChannel):

        try:
            res = setlogchannel(ctx.guild, channel.id)
            await ctx.send(f"✅ Log channel has been set to #{channel}")
        except Exception as err:
            await ctx.send(f"❌ Failled to set logs channel: {err}")
        


    @commands.command(help="Turn logs On or off")
    @commands.has_permissions(manage_channels=True)
    async def togglelogs(self, ctx):

        d = togglelogs(ctx.guild)
        
        if d:
            await ctx.send("✅ Logs have been enabled")
        else:
            await ctx.send("❌ Logs have been disabled")

    
    @commands.Cog.listener()
    async def on_voice_state_update(self,usr : discord.Member,bfv : discord.VoiceState,afv:discord.VoiceState):

        if bfv.channel is None:
            loggerdata = getlogdata(afv.channel.guild)
        else:
            loggerdata = getlogdata(bfv.channel.guild)

        if loggerdata[1]:
            pass
        else:
            return


        if afv.channel == bfv.channel:
            pass
        else:
            emb = discord.Embed(
                title = f'{usr}',
                description = 'User changed voice channels'
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
                description = 'User server muted'
                )
                emb.set_thumbnail(url=usr.avatar_url)
                
            else:
                
                emb = discord.Embed(
                title = f'{usr}',
                description = 'User was Unserver-muted'
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
                description = 'User was server Deafened'
                )
                emb.set_thumbnail(url=usr.avatar_url)
                
            else:
                
                emb = discord.Embed(
                title = f'{usr}',
                description = 'User was Unserver-deafened'
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

        loggerdata = getlogdata(msg.guild)

        if loggerdata[1]:
            pass
        else:
            return

        emb = discord.Embed(
            title=f'{msg.guild}',
            description=f'A message was deleted',
            colour= discord.Colour.red()
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

        loggerdata = getlogdata(bmsg.guild)

        if loggerdata[1]:
            pass
        else:
            return


        if amsg.author == self.client.user:
            return

        emb = discord.Embed(
            title=f'{bmsg.author}',
            description=f'A message was edited',
            colour=discord.Colour.blue()
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

        loggerdata = getlogdata(guild)

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
            colour=discord.Colour.red()
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

        loggerdata = getlogdata(guild)

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
            colour=discord.Colour.red()
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
