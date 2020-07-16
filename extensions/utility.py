import discord, datetime, time
from discord.ext import commands, menus
import psutil, operator, os
import humanize as h
import requests, shutil
import random, platform, blutapi
from discord.utils import get
import inspect,pytz
from Setup import * 

LEFTREACTION='⬅️'
XREACTION='🇽'
RIGHTREACTION='➡️'


class embedColor:
    orange = 0xec5c17
    yellow = 0xFFFF00
    blurple = 0x7289DA
    blue = 0x499FFF 
    grey = 0xCCCCCC 
    white = 0xffffff
    cyan = 0x53dff7

class utility(commands.Cog,name='Utility'):
    """
    Random Useful commands
    """
    def __init__(self, client):
        self.client = client
        self.sniped = {}
        self.clientid = clientid
                
    @commands.command(help='Help command to get started on using the bot!')
    async def help(self,ctx,*cog):
        """Gets all cogs and commands of mine."""
        prefix = blutapi.getprefix(ctx.guild)
        cogembeds=[]

        try:
            if not cog:
                """Cog listing.  What more?"""

                for x in self.client.cogs:

                    if x == "Jishaku":
                        pass
                    else:
                        halp=discord.Embed(title=f'{x}', description=f'{self.client.cogs[x].__doc__}', timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern')))

                        for command in self.client.get_cog(x).get_commands():

                            if not command.hidden:
                                if command.aliases:
                                    halp.add_field(name=f"{command.name} - ({', '.join(command.aliases)})", value=command.help)
                                else:
                                    halp.add_field(name=f"{command.name}", value=command.help)
                        
                        cogembeds.append(halp)

            msg = await ctx.send(embed=cogembeds[0])
            await msg.add_reaction('◀')
            await msg.add_reaction('⏹')
            await msg.add_reaction('▶')
            page= 0

            uses = 0

            def check(reaction, user):
                return reaction.message.id == msg.id and user == ctx.author
            while uses < 20:
                try:
                    reaction, _ = await self.client.wait_for('reaction_add', timeout=100.0, check=check)
                    await msg.remove_reaction(reaction.emoji, ctx.author)
                    if reaction.emoji == '▶' and page < len(cogembeds)-1:
                        page +=1
                        uses +=1
                        await msg.edit(embed=cogembeds[page])
                    if reaction.emoji == '◀' and page != 0:
                        page -=1
                        uses +=1
                        await msg.edit(embed=cogembeds[page])
                    if reaction.emoji == '⏹':
                        await msg.delete()

                except TimeoutError:
                    uses = 20                       
        except Exception as err:
            await ctx.send(err)
            
    @commands.Cog.listener()
    async def on_message_delete(self,msg):
        self.sniped[msg.guild.id] = msg

    @commands.command(aliases=['snp'], help='Snipe the last message deleted in this server')
    async def snipe(self,msg):

        try:
            sniped:discord.Message = self.sniped[msg.guild.id]
        except:
            return await msg.channel.send("``Nothing to snipe``")

        emb = discord.Embed(title=f'Sniped a message from {sniped.author}', timestamp=sniped.created_at)
        emb.add_field(name="Message Content", value=sniped.content)
        emb.add_field(name='Sent in', value=f'#{sniped.channel}')
        emb.set_thumbnail(url=sniped.author.avatar_url)
        emb.set_footer(text='Sent at')
        
        try:
            img : discord.message.Attachment = sniped.attachments[0]
            emb.set_image(url=img.proxy_url)
        except Exception as err:
            print(err)
            pass

        await msg.channel.send(embed=emb)
    
    @commands.command(aliases=['stats','binfo','about'], help='Gathers and displays Bot info')
    async def botinfo(self,msg):
        pythonVersion = platform.python_version()
        clientVersion = '1.14.0'
        dpyVersion = discord.__version__
        serverCount = len(self.client.guilds)
        memberCount = len(set(self.client.get_all_members()))
        embed = discord.Embed(title=f'{self.client.user.name} Stats', colour=msg.author.colour, timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern')))
        embed.add_field(name='Bot Version:', value=clientVersion)
        embed.add_field(name='Python Version:', value=pythonVersion)
        embed.add_field(name='Discord.Py Version', value=dpyVersion)
        embed.add_field(name='Total Guilds:', value=serverCount)
        embed.add_field(name='Total Users:', value=memberCount)
        embed.add_field(name='Bot Creator:', value="<@393165866285662208>")
        embed.set_footer(text=f'{self.client.user.name} || command credit: Tayso20')
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_image(url='https://top.gg/api/widget/627521478761381920.svg')
        await msg.send(embed=embed)

    @commands.command(help='Sends A rich embed with invite links for the bot and support server')
    async def invite(self, msg):

        emb = discord.Embed(timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern')))
        emb.add_field(name='**Invite Link**', value=f'[Click me!](https://discordapp.com/oauth2/authorize?client_id={self.clientid}&scope=bot&permissions=8)', inline=False)
        emb.add_field(name='**join the support server here!**', value='[Click me!](https://discord.gg/NNfD6eQ)', inline=False)
        emb.set_author(name=self.client.user, icon_url=self.client.user.avatar_url)
        await msg.channel.send(embed=emb)

    @commands.command(aliases=['pong'], help= 'Shows Bot latency')
    async def ping(self,msg):
        time_1 = time.perf_counter()
        await msg.trigger_typing()
        time_2 = time.perf_counter()
        ping = round((time_2-time_1)*1000)
        await msg.send(f"⏳ Pong! My ping is `{ping}ms`")

    @commands.command(aliases=['sic','sav'])
    async def servericon(self,msg:commands.Context):

        server = msg.guild.icon_url

        servericon = f'{msg.guild.id}.gif'

        pth = os.getcwd()
        dst = os.path.join(str(pth),'Data/images')
        src = os.path.join(str(pth),servericon)
        src2 = os.path.join(dst,servericon)

        images = os.listdir(dst)

        async def sendav(src,src2,img):
            shutil.move(src2,pth)
            await msg.channel.send(file=discord.File(servericon))
            shutil.move(src,dst)

        pull = requests.get(server, allow_redirects=True)

        if servericon in images:
            await sendav(src,src2,servericon)
            return
        else:
            open(servericon,'wb').write(pull.content)
            shutil.move(src,dst)

        await sendav(src,src2,servericon)
        return

    @commands.command(aliases=['sinfo', 'guild'], help='Gathers and Displays server info')
    async def serverinfo(self, msg):
        embed = discord.Embed(
            title = f'{msg.guild}',
            colour = discord.Colour.blue(),
            timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
        )

        botcount = 0
        for bot in msg.guild.members:
            if bot.bot:
                botcount += 1

        membercount = len(msg.guild.members) - botcount
        TextChs = len(msg.guild.text_channels)
        voiceChs = len(msg.guild.voice_channels)
        catcount = len(msg.guild.categories)
        roles = len(msg.guild.roles)
        servericonurl = str(msg.guild.icon_url)

        embed.add_field(name='Text channels',value=TextChs,inline=True)
        embed.add_field(name='categories',value=catcount,inline=True)
        embed.add_field(name='Region',value=f'{msg.guild.region}',inline=True)
        embed.add_field(name='Voice channels',value=voiceChs,inline=True)
        embed.add_field(name='Server ID',value=f'{msg.guild.id}',inline=True)
        embed.add_field(name='Server owner', value=f'{msg.guild.owner}',inline=True)
        embed.add_field(name='total members',value=len(msg.guild.members),inline=True)
        embed.add_field(name='humans', value=membercount,inline=True)
        embed.add_field(name='bots',value=botcount,inline=True)
        embed.add_field(name='Created',value=f'{h.naturaltime(msg.guild.created_at)}',inline=True)
        embed.add_field(name='roles',value=roles)
        embed.set_thumbnail(url=servericonurl)

        await msg.channel.send(embed=embed)

    @commands.command(aliases=['uinfo', 'whois','profile'], help='Gathers and Displays user info')
    async def userinfo(self,msg:commands.Context,*, user=None):

        perms = []

        try:
            member = get(msg.guild.members, id=int(user))
            
        except:

            if user:
                try:
                    member = get(msg.guild.members, name=user)
                    
                except:
                    member = get(msg.guild.members, display_name=user)

            if  user is None:
                member : discord.Member = msg.author
            else:
                for men in msg.message.mentions:
                    member = men


        for perm in member.guild_permissions:

            Key = ['ban members', 'manage guild','mention everyone', 'administrator', "send messages"]
            if perm[1]:
                name = perm[0]
                name = name.replace('_', ' ')
    
                if name in Key:
                    perms.append(f'{name}\n')
            else:
                pass


        permsd = list(dict.fromkeys(perms))
        roles = []

        for role in member.roles:
            roles.append(role.mention)

        def joinpos(user, guild):
            try:
                joins = tuple(sorted(guild.members, key=operator.attrgetter("joined_at")))
                if None in joins:
                    return None
                for key, elem in enumerate(joins):
                    if elem == user:
                        return key + 1, len(joins)
                return None
            except Exception as error:
                print(error)
                return None

        joined = joinpos(member,msg.guild)

        def checkfornitro(user):
            if user.is_avatar_animated():
                nitro = True
            
            for role in user.roles:
                if role.name == "Nitro Booster":
                    nitro = True

            return nitro
    
        isnitro = checkfornitro(member)
        embed = discord.Embed(title=f'{member.name}',colour=member.colour, timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern')))

        embed.add_field(name='Joined Guild', value=f'{h.naturaltime(member.joined_at)}',inline=True)
        embed.add_field(name='Joined Discord', value=f'{h.naturaltime(member.created_at)}',inline=True)
        embed.add_field(name='Guild join position', value=f'{joined[0]}/{joined[1]}')
        embed.add_field(name=f'Roles({len(roles)})', value=' '.join(roles), inline=False)
        embed.add_field(name='Key Permissions', value=''.join(permsd),inline=False)
        if member.name == member.display_name:
            embed.add_field(name='Nickname', value=f'None')
        else:
            embed.add_field(name='Nickname', value=f'{member.display_name}')
        embed.add_field(name='Tag', value=f'#{member.discriminator}',inline=True)
        embed.add_field(name='nitro?', value=f'{isnitro}')
       

        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=member.id, icon_url=member.avatar_url)

        await msg.channel.send(embed=embed)

    @commands.command(aliases=["date","datetime","time"], help="Show the current date and time")
    async def day(self,ctx):
        today = datetime.datetime.today().strftime('%Y-%h-%d %H:%M:%S')

        await ctx.send(today)
    
    @commands.command(aliases=['rmember'])
    async def randommember(self,ctx:commands.Context):

        members = ctx.guild.members
        member:discord.Member = random.choice(members)

        emb = discord.Embed(title=member.name)

        emb.set_thumbnail(url=member.avatar_url)
        emb.add_field(name='id', value=f'{member.id}')

        await ctx.send(embed=emb)

def setup(client):
    client.add_cog(utility(client))
