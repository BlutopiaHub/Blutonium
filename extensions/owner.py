import discord, pytz, pg8000
from discord.ext import commands
from discord.utils import get
import humanize as h
import psutil, platform, ast
import os, cpuinfo, speedtest
import blutapi, datetime
from Setup import *

def guildembed(guild):
    embed = discord.Embed(
        title = f'{guild}',
        colour = discord.Colour.blue(),
        timestamp=datetime.datetime.now()
    )

    botcount = 0
    for bot in guild.members:
        if bot.bot:
            botcount += 1
            
    membercount = len(guild.members) - botcount
    TextChs = len(guild.text_channels)
    voiceChs = len(guild.voice_channels)
    catcount = len(guild.categories)
    roles = len(guild.roles)
    servericonurl = str(guild.icon_url)

    embed.add_field(name='Text channels',value=TextChs,inline=True)
    embed.add_field(name='categories',value=catcount,inline=True)
    embed.add_field(name='Region',value=f'{guild.region}',inline=True)
    embed.add_field(name='Voice channels',value=voiceChs,inline=True)
    embed.add_field(name='Server ID',value=f'{guild.id}',inline=True)
    embed.add_field(name='Server owner', value=f'{guild.owner}',inline=True)
    embed.add_field(name='total members',value=len(guild.members),inline=True)
    embed.add_field(name='humans', value=membercount,inline=True)
    embed.add_field(name='bots',value=botcount,inline=True)
    embed.add_field(name='Created',value=f'{h.naturaltime(guild.created_at)}',inline=True)
    embed.add_field(name='roles',value=roles)
    embed.set_thumbnail(url=servericonurl)
    return embed

class owner(commands.Cog,name='Owner'):

    """
    Commands restricted to the bot owner
    """
    
    def __init__(self, client):
        self.client : commands.Bot = client
        self.last = {}

    @commands.command(aliases=['ss'])
    @commands.is_owner()
    async def screenshot(self,ctx,*Kwargs):

        if not Kwargs[0].startswith('http://'):
            site = "http://" + Kwargs[0]

        scr = f"https://image.thum.io/get/width/1920/crop/1080{site}"

        try:

            emb = discord.Embed(title="Screenshot", description=site)
            emb.set_image(url=scr)
        except:
            emb = discord.Embed(title="FAILED!")

        await ctx.send(embed=emb)

    @commands.command(aliases=['dev'], help="A set of secret commands for bot owner")
    @commands.is_owner()
    async def develloper(self,ctx,*kwargs):

        if kwargs[0] == 'sql':

            res = blutapi.query_database(" ".join(kwargs[1:]))

            await ctx.send(res)
 
        if kwargs[0] == 'edit':
            ori:discord.Message = ctx.message
            msg:discord.Message= self.last[ctx.guild.id]

            if kwargs[1] == '-s':
                try:
                    await ori.delete()
                except:
                    pass
                return await msg.edit(content=' '.join(kwargs[2:]))
            return await msg.edit(content=' '.join(kwargs[1:]))

        if kwargs[0] == 'say':

            ori:discord.Message = ctx.message
            if kwargs[1] == '-s':
                try:
                    await ori.delete()
                except:
                    pass
                self.last[ctx.guild.id] = await ctx.send(' '.join(kwargs[2:]))
                return
            self.last[ctx.guild.id] = await ctx.send(' '.join(kwargs[1:]))
            return

        if kwargs[0] == 'setprefix':
            blutapi.update_prefix(ctx.guild,kwargs[1])

            emb = discord.Embed(title=f'{ctx.guild}', description='The prefix for this server was successfully changed!', color=discord.Colour.green(),timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern')))
            emb.add_field(name='Changed to:', value=f'{kwargs[1]}')
            await ctx.channel.send(embed=emb)

        if kwargs[0] == 'guilds':
            totalguilds = self.client.guilds
            try:
                if kwargs[1]:
                    try:
                        id = int(kwargs[1])
                        guild : discord.Guild = get(totalguilds, id=id)

                        if guild is None:
                            raise Exception

                        emb = guildembed(guild)
                
                        return await ctx.send(embed=emb)
                    except:
                        
                        id = " ".join(kwargs[1:])
                        guild : discord.Guild = get(totalguilds, name=id)

                        if guild is None:
                            return await ctx.send("guild not found")

                        emb = guildembed(guild)
                        msg = await ctx.send(embed=emb)

            except: 
                
                emb = discord.Embed(title=f"All guilds")

                if len(totalguilds) < 25:
                    for guild in totalguilds:
                        emb.add_field(name=guild,value=f'{guild.id} - {len(guild.members)} Members')

                    return await ctx.send(embed=emb)
                else:
                    emb2 = discord.Embed(title=f"All guilds 2")
                    for guild in totalguilds[0:24]:
                        emb.add_field(name=guild,value=f'{guild.id} - {len(guild.members)} Members')
                    if len(totalguilds) < 48:
                        for guild in totalguilds[24:]:
                            emb2.add_field(name=guild,value=f'{guild.id} - {len(guild.members)} Members')
                    else:
                        for guild in totalguilds[24:48]:
                            emb2.add_field(name=guild,value=f'{guild.id} - {len(guild.members)} Members')
                    msg = await ctx.send(embed=emb)
                    await msg.add_reaction('◀')
                    await msg.add_reaction('⏹')
                    await msg.add_reaction('▶')
                    pages = [emb,emb2]

                    page=0

                    uses = 0

                    def check(reaction, user):
                        return reaction.message.id == msg.id and user == ctx.author
                    while uses < 15:
                        try:
                            reaction, _ = await self.client.wait_for('reaction_add', timeout=100.0, check=check)
                            await msg.remove_reaction(reaction.emoji, ctx.author)
                            if reaction.emoji == '▶' and page == 0:
                                page +=1
                                uses +=1
                                await msg.edit(embed=pages[page])
                            if reaction.emoji == '◀' and page == 1:
                                page -=1
                                uses +=1
                                await msg.edit(embed=pages[page])
                            if reaction.emoji == '⏹':
                                await msg.delete()

                        except TimeoutError:
                            uses = 15                

    @commands.command(aliases=['bl','cban'],help="Bans a user from using commands on this discord bot")
    @commands.is_owner()
    async def blacklist(self,msg,user:discord.Member):

        userid = user.id
        bl = blutapi.blacklist_user(userid)
        await msg.channel.send(f"✅ **User {user} was successfully blacklisted**")
        
    @commands.command(aliases=['ubl','cuban'],help="Unbans a user from using commands on this discord bot")
    @commands.is_owner()
    async def unblacklist(self,msg,user:discord.Member):

        userid = user.id
        ubl = blutapi.unblacklist_user(userid)
        await msg.channel.send(f"✅ **User {user} was successfully unblacklisted**")

    @commands.command(aliases=['sys'],help='Shows Information about the system that the bot is running on')
    @commands.is_owner()
    async def system(self,msg):

        #Speed = speedtest.Speedtest()
        #Speed.get_best_server()

        #upload = Speed.upload(threads=None)
        #download = Speed.download(threads=None)

        try:
            proc = psutil.Process()
            system = platform.uname()
            mem = proc.memory_full_info()
            cpu_per = psutil.cpu_percent() 
            cores = psutil.cpu_count()
            memory = psutil.virtual_memory().total >> 20
            em = discord.Embed(color=discord.Color.red(), title="System Info",)
                               #description="Host OS" +  +
                                           #"Cores" + f" : **{cores}**\n" +
                                           #"CPU" + f" : **{cpu_per}%**\n" +
                                          # "RAM usage" + f" : **Using {h.naturalsize(mem.rss)} physical memory\n" +
                                          # "Storage" + f" : **{storage_free} GB {sf}**")

            em.add_field(name='Host OS',value=f"**{system.system}-{system.version.split('SMP')[0]}**", inline=True)
            em.add_field(name="CPU info",value=f"{int(cores)}x {cpuinfo.get_cpu_info()['brand']}",inline=True)
            em.add_field(name='Host Name',value=f"{platform.node()}",inline=False)
            em.add_field(name="Process Memory usage",value=f"{h.naturalsize(mem.rss)} / {memory} MB",inline=True)
            em.add_field(name="Process CPU usage",value=f"{cpu_per}%",inline=True)
            #em.add_field(name="System Connection info",value=f"{h.naturalsize(download)}/s Down {h.naturalsize(upload)}/s Up",inline=True)
            

            await msg.send(embed=em)
        except Exception as e:
            await msg.send(f"Failed to get system info: {e} ")

    @commands.command(aliases=['lc'],help='Loads any Cog')
    @commands.is_owner()
    async def load(self,msg,ext):
        try:
            self.client.load_extension(f'extensions.{ext}')
            await msg.channel.send(f'`{ext}` Was successfully loaded')
        except Exception as error:
            await msg.channel.send(f'there was an error loading `{ext}`: {error}')

    @commands.command(aliases=['ulc'],help='Unloads any cog')
    @commands.is_owner()
    async def unload(self,msg,ext):
        try:
            self.client.unload_extension(f'extensions.{ext}')
            await msg.channel.send(f'`{ext}` Was successfully unloaded.')
        except Exception as error:
            await msg.channel.send(f'there was an error unloading `{ext}`: {error}')

    @commands.command(aliases=['rlc'], help='reloads any cog')
    @commands.is_owner()
    async def reload(self,msg,ext):

        if ext == "all":

            exts = []
            sucessful = []

            for f in os.listdir('./extensions'):
                if f.endswith('.py'):
                    d = f.replace('.py','')
                    exts.append(d)

            for ext in exts:
                try:
                    self.client.unload_extension(f'extensions.{ext}')
                    self.client.load_extension(f'extensions.{ext}')
                    sucessful.append(ext)
                except Exception as error:
                    print(error)
                    return await msg.channel.send(f'there was an error reloading `{ext}`: Check console')  
          
            return await msg.send(f"`{', '.join(sucessful)}` Were sucessfully reloaded")

        try:
            self.client.unload_extension(f'extensions.{ext}')
            self.client.load_extension(f'extensions.{ext}')
            await msg.channel.send(f'`{ext}` Was successfully reloaded.')
        except Exception as error:
            await msg.channel.send(f'there was an error reloading `{ext}`: {error}')

    @commands.command(help='send a direct message to any user that has a mutual server with the bot')
    @commands.is_owner()
    async def dm(self,msg, user, *,content):

        user : discord.User = get(self.client.get_all_members(), name=user)

        await user.send(content)

    @commands.command(aliases=['ev'], help='Executes Python code as The bot')
    @commands.is_owner()
    async def eval(self,msg, *, cmd):

        def insert_returns(body):
            # insert return stmt if the last expression is a expression statement
            if isinstance(body[-1], ast.Expr):
                body[-1] = ast.Return(body[-1].value)
                ast.fix_missing_locations(body[-1])

            # for if statements, we insert returns into the body and the orelse
            if isinstance(body[-1], ast.If):
                insert_returns(body[-1].body)
                insert_returns(body[-1].orelse)

            # for with blocks, again we insert returns into the body
            if isinstance(body[-1], ast.With):
                insert_returns(body[-1].body)

        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")

        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            'client': self.client,
            'discord': discord,
            'commands': commands,
            'ctx': msg,
            '__import__': __import__,
            'sqldb': dbuname,
            'sqldbp': dbpassword
        }

        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = (await eval(f"{fn_name}()", env))
        ress = type(result)
        support = get(self.client.guilds , id=629436501964619776)
        emoji = get(support.emojis, name="BlutoCheck")
        emb = discord.Embed(title=f'{emoji}  Eval',colour=discord.Colour.green(), description='Execution was successfull')
        emb.add_field(name=f'Output Console', value = f'```{result}```')
        emb.add_field(name = 'type', value=f'```{ress}```')

        await msg.channel.send(embed=emb)

    @eval.error
    async def ev_error(self,msg,error):

        if isinstance(error, commands.CommandInvokeError):

            emb = discord.Embed(title=f'❌  ERROR' ,colour=discord.Colour.red(), description='An error occured while trying to execute this code')
            emb.add_field(name='Error', value=f'```{error}```')

            await msg.channel.send(embed=emb)

        if isinstance(error, commands.NotOwner):

            emb = discord.Embed(title=f'❌  ERROR' ,colour=discord.Colour.red(), description='You arent the bot owner')
            emb.add_field(name='Details', value='***EVAL*** Is a VERY Sensitive command that allows you to direcly run code on the bot Please dont run this command')

            await msg.channel.send(embed=emb,)

def setup(client):
    client.add_cog(owner(client))
