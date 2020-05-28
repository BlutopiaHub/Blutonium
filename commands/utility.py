import discord, datetime, time
from discord.ext import commands
import psutil
import platform
import MySQLdb
import operator
from discord.utils import get
from Setup import * 


def get_prefix(guild):
    db = MySQLdb.connect(host=sqhost, user=squname, passwd=sqpassword, db=sqdbname)
    cur = db.cursor()

    guildid = str(guild.id)
    sql = f"SELECT * FROM prefixes WHERE id={guildid}"  
    cur.execute(sql)
    prefix = cur.fetchone()[1]
    db.close()

    return prefix


class utility(commands.Cog):
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
        prefix = get_prefix(ctx.guild)

        try:
            if not cog:
                """Cog listing.  What more?"""
                halp=discord.Embed(title='Help!',
                                description=f'Use `{prefix}help *category*` to see all the commands!')
                cogs_desc = ''
                for x in self.client.cogs:
                    cogs_desc += f'**{x}** - {self.client.cogs[x].__doc__}\n'
                halp.add_field(name='Categories',value=cogs_desc[0:len(cogs_desc)-1],inline=True)
                cmds_desc = ''
                for y in self.client.walk_commands():
                    if not y.cog_name and not y.hidden:
                        cmds_desc += ('{} - {}'.format(y.name,y.help)+'\n')
                halp.add_field(name='tip',value=f'***Use {prefix}changeprefix to change the bot prefix***',inline=False)
                await ctx.message.add_reaction(emoji='❔')
                await ctx.send('',embed=halp)
            else:
                """Helps me remind you if you pass too many args."""
                if len(cog) > 1:
                    halp = discord.Embed(title='Error!',description='That is way too many cogs!',color=discord.Color.red())
                    await ctx.send('',embed=halp)
                else:
                    """Command listing within a cog."""
                    found = False
                    for x in self.client.cogs:
                        for y in cog:
                            if x == y:
                                halp=discord.Embed(title=cog[0]+' Command Listing',description=self.client.cogs[cog[0]].__doc__)
                                for c in self.client.get_cog(y).get_commands():
                                    if not c.hidden:
                                        halp.add_field(name=f"{c.name}-{c.aliases}",value=c.help,inline=False)
                                found = True
                    if not found:
                        """Reminds you if that cog doesn't exist."""
                        halp = discord.Embed(title='Error!',description='How do you even use "'+cog[0]+'"?',color=discord.Color.red())
                    else:
                        await ctx.message.add_reaction(emoji='❔')
                    await ctx.send('',embed=halp)
        except Exception as err:
            await ctx.send(f"Excuse me, I can't send embeds. {err}")
            
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
        emb.set_thumbnail(url=sniped.author.avatar_url)
        emb.set_footer(text='Sent at')
    

        await msg.channel.send(embed=emb)
    



    @commands.command(aliases=['stats','binfo'], help='Gathers and displays Bot info')
    async def botinfo(self,msg):
        pythonVersion = platform.python_version()
        clientVersion = '1.9.1'
        dpyVersion = discord.__version__
        serverCount = len(self.client.guilds)
        memberCount = len(set(self.client.get_all_members()))
        embed = discord.Embed(title=f'{self.client.user.name} Stats', colour=msg.author.colour)
        embed.add_field(name='Bot Version:', value=clientVersion)
        embed.add_field(name='Python Version:', value=pythonVersion)
        embed.add_field(name='Discord.Py Version', value=dpyVersion)
        embed.add_field(name='Total Guilds:', value=serverCount)
        embed.add_field(name='Total Users:', value=memberCount)
        embed.add_field(name='Bot Creator:', value="<@393165866285662208>")
        embed.add_field(name='Status:', value=discord.Status.online)
        embed.set_footer(text=f'{self.client.user.name} || command credit: Tayso20')
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await msg.send(embed=embed)


    @commands.command(help='Sends A rich embed with invite links for the bot and support server')
    async def invite(self, msg):

        emb = discord.Embed()
        emb.add_field(name='**Invite Link**', value=f'[Click me!](https://discordapp.com/oauth2/authorize?client_id={self.clientid}&scope=bot&permissions=8)', inline=False)
        emb.add_field(name='**Im made with the drizzi bot template! join the support server here!**', value='[Click me!](https://discord.gg/NNfD6eQ)', inline=False)
        emb.set_author(name=self.client.user, icon_url=self.client.user.avatar_url)
        await msg.channel.send(embed=emb)

    @commands.command(help="Shows any users current activity")
    async def activity(self,msg,user=None):

        for member in msg.message.mentions:
            user = member

        if not msg.message.mentions:
            user = msg.author

        print(user.activity)

        Name = user.activity.name
        stat = str(user.activity.type).split('.')[1]

        emb = discord.Embed(title = f'{stat} {Name}')
        await msg.channel.send(embed=emb)



    @commands.command(aliases=['pong'], help= 'Shows Bot latency')
    async def ping(self,msg):
        time_1 = time.perf_counter()
        await msg.trigger_typing()
        time_2 = time.perf_counter()
        ping = round((time_2-time_1)*1000)
        await msg.send(f"⏳ Pong! My ping is `{ping}ms`")

    @commands.command(aliases=['sinfo', 'guild'], help='Gathers and Displays server info')
    async def serverinfo(self, msg):
        embed = discord.Embed(
            title = f'{msg.guild}',
            colour = discord.Colour.blue(),
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
        embed.add_field(name='Created At',value=f'{msg.guild.created_at}',inline=True)
        embed.add_field(name='roles',value=roles)
        embed.set_thumbnail(url=servericonurl)

        await msg.channel.send(embed=embed)

    @commands.command(aliases=['uinfo', 'whois','profile'], help='Gathers and Displays user info')
    async def userinfo(self,msg):

        perms = []

        for user in msg.message.mentions:
            member = user

        if  not msg.message.mentions:
            member = msg.author

        for perm in msg.channel.permissions_for(member):

            if perm[1]:
                name = perm[0]
                perms.append(name)
            else:
                pass

        permsd = list(dict.fromkeys(perms))
        roles = []

        for role in member.roles:
            roles.append(role.name)

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
                return True
            else:
                return False

        isnitro = checkfornitro(member)

        embed = discord.Embed(
            title=f'{member.name}',
            colour=member.colour
        )
        embed.add_field(name='joined server', value=f'{member.joined_at}',inline=True)
        embed.add_field(name='joined discord', value=f'{member.created_at}',inline=True)
        embed.add_field(name='server join pos', value=f'{joined[0]}/{joined[1]}')
        embed.add_field(name=f'Roles({len(roles)})', value=', '.join(roles), inline=False)
        embed.add_field(name='permissions', value=', '.join(permsd),inline=False)
        embed.add_field(name='Nickname', value=f'{member.display_name}')
        embed.add_field(name='Tag', value=f'#{member.discriminator}',inline=True)
        embed.add_field(name='nitro?', value=f'{isnitro}')
        embed.add_field(name='id', value=f'{member.id}')

        embed.set_thumbnail(url=member.avatar_url)

        await msg.channel.send(embed=embed)

def setup(client):
    client.add_cog(utility(client))
