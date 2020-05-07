import discord
from discord.ext import commands
from discord.utils import get
import ast
import platform
import humanize as h
import psutil
import os
import cpuinfo
import speedtest


class owner(commands.Cog):

    """
    Commands restricted to the bot owner
    """
    
    def __init__(self, client):
        self.client=client

    @commands.command(aliases=['sys'],help='Shows Information about the system that the bot is running on')
    @commands.is_owner()
    async def system(self,msg):

        Speed = speedtest.Speedtest()
        Speed.get_best_server()

        upload = Speed.upload(threads=None)
        download = Speed.download(threads=None)

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
            em.add_field(name="System Connection info",value=f"{h.naturalsize(download)}/s Down {h.naturalsize(upload)}/s Up",inline=True)
            

            await msg.send(embed=em)
        except Exception as e:
            await msg.send(f"Failed to get system info: {e} ")

    @commands.command(aliases=['lc'],help='Loads any Cog')
    @commands.is_owner()
    async def load(self,msg,ext):
        try:
            self.client.load_extension(f'commands.{ext}')
            await msg.channel.send(f'`{ext}` Was successfully loaded')
        except Exception as error:
            await msg.channel.send(f'there was an error loading `{ext}`: {error}')

    @commands.command(aliases=['ulc'],help='Unloads any cog')
    @commands.is_owner()
    async def unload(self,msg,ext):
        try:
            self.client.unload_extension(f'commands.{ext}')
            await msg.channel.send(f'`{ext}` Was successfully unloaded.')
        except Exception as error:
            await msg.channel.send(f'there was an error unloading `{ext}`: {error}')

    @commands.command(aliases=['rlc'], help='reloads any cog')
    @commands.is_owner()
    async def reload(self,msg,ext):
        try:
            self.client.unload_extension(f'commands.{ext}')
            self.client.load_extension(f'commands.{ext}')
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
            'msg': msg,
            '__import__': __import__
        }

        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = (await eval(f"{fn_name}()", env))
        ress = type(result)
        emb = discord.Embed(title='✅  Eval',colour=discord.Colour.green(), description='Execution was successfull')
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

            await msg.channel.send(embed=emb)


def setup(client):
    client.add_cog(owner(client))
