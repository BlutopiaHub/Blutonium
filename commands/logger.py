import discord
from discord.ext import commands
from discord.utils import get
import os 

class logger(commands.Cog):
    """
    Listeners for logging (Make a channel called logs!)
    """
    def __init__(self, client : commands.Bot):
        self.client = client
        self.blacklist = [264445053596991498,336642139381301249]

    #@commands.Cog.listener()
    #async def on_user_update(self,bus:discord.Member, aus:discord.Member):

        #if bus.avatar_url == aus.avatar_url:
       #     pass 
       # else:
      #      try:
      #          dst = os.path.join(str(os.getcwd()),f'Data/images/{bus.id}.png')
     #           dstg = os.path.join(str(os.getcwd()),f'Data/images/{bus.id}.gif')
     #       except:
        #        return

        #    try:
         #       if bus.is_avatar_animated():
          #          os.remove(dstg)
         #       else:
      #              os.remove(dst)
      #      except:
     #           return

    @commands.Cog.listener()
    async def on_voice_state_update(self,usr : discord.Member,bfv : discord.VoiceState,afv:discord.VoiceState):

        if bfv.channel is None:
            pass
        elif bfv.channel.guild.id in self.blacklist:
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
                channel = get(bfv.channel.guild.channels, name='logs')
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
                channel = get(bfv.channel.guild.channels, name='logs')
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
                channel = get(bfv.channel.guild.channels, name='logs')
                await channel.send(embed = emb)   
                return
            except: 
                return


    @commands.Cog.listener()
    async def on_message_delete(self, msg):

        if msg.guild.id in self.blacklist:
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
            chan : discord.TextChannel = get(msg.guild.channels, name="logs")
            await chan.send(embed=emb)
        except:
            return
      

    @commands.Cog.listener()
    async def on_message_edit(self,bmsg,amsg):

        if bmsg.guild.id in self.blacklist:
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
            chan : discord.TextChannel = get(bmsg.guild.channels, name="logs")
            await chan.send(embed=emb)
        except:
            return

    @commands.Cog.listener()
    async def on_member_ban(self,guild,banmember):

        if guild.id in self.blacklist:
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
            chan : discord.TextChannel = get(guild.channels, name="logs")
            await chan.send(embed=emb)
        except:
            return
    

    @commands.Cog.listener()
    async def on_member_unban(self,guild, banmember):
            
        if guild.id in self.blacklist:
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
            chan : discord.TextChannel = get(guild.channels, name="logs")
            await chan.send(embed=emb)
        except:
            return


def setup(client):
    client.add_cog(logger(client))
