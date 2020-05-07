import discord
from discord import Spotify
from discord.ext import commands
from discord.utils import get
import math
from time import *
import datetime
import os
from random import randrange
import requests
from Setup import *
import shutil
import twitch
import humanize as h

class fun(commands.Cog):
    """
    Fun Commands for messing with friends and having a good time
    """
    def __init__(self, client):
        self.client=client
        self.helix = twitch.Helix(twitchkey, use_cache=True)
        self.hypix = HPapikey

    
    @commands.command(help='The ultimate judge')
    async def pp(self,msg,user:discord.Member=None):

        if user is None:
            user = msg.author

        length = randrange(1, 25)

        pp = "8"+("="*length)+"3"

        if length > 22:
            lens = "Too long to measure"
            pp = "8====================================================================================3"
        else:
            lens = f'{length} inches'
        
        

        if user.id == ownerid:
            lens="too long to measure"
            pp = "8=========================================================================================3"

        emb= discord.Embed(title=f"{user}'s pp length'")

        emb.add_field(name=lens, value=f"**{pp}**")

        await msg.channel.send(embed=emb)

    @commands.command(help='Get a users hypixel data')
    async def hypixel(self,msg,query):

        link=f'https://mc-heads.net/avatar/{query}'
        data = requests.request("GET", f"https://api.hypixel.net/player?key={self.hypix}&name={query}").json()

        if data["player"] is None:
            emb= discord.Embed(title='Player not found!!',description='Player does not have a hypixel profile or Drizzi failed to get the players information')
            emb.set_thumbnail(url=link)
            return await msg.send(embed=emb)
         
        emb = discord.Embed(title=query)

        login = data["player"]["lastLogin"]

        emb.add_field(name='Rank',value=f'**{data["player"]["newPackageRank"]}**')
        #emb.add_field(name='Karma',value=f'**{data["player"]["karma"]}**')
        emb.add_field(name='Last Login',value=f"**{datetime.datetime.fromtimestamp(int(str(login)[:-3])).strftime('%Y-%m-%d %H:%M')}**")
        emb.set_thumbnail(url=link)
        
        await msg.send(embed=emb)


    @commands.command(aliases=['ttv'], help='Fetch and display a twitch users profile')
    async def twitch(self,msg, user):

        ttv = self.helix.user(user)
        displayname = ttv.display_name
    
        emb = discord.Embed(
            title=displayname
        )
        

        def CheckforLive(ttv):

            if ttv.is_live:
                return '🔴 Live'

            else:
                return '🔵 Offline'


        emb.set_thumbnail(url=ttv.profile_image_url)
        emb.add_field(name='Followers', value=ttv.followers().total)
        emb.add_field(name='Following', value=ttv.following().total)
        emb.add_field(name='Status', value=CheckforLive(ttv))
        print(ttv.email)
        if ttv.is_live:
            emb.add_field(name='Stream', value=f'[{ttv.stream.title}](https://twitch.tv/{ttv.display_name})')
            emb.add_field(name='Viewers', value=ttv.stream.viewer_count)
            
        await msg.channel.send(embed=emb)

    @commands.command(aliases=['av'], help='Shows user avatar')
    async def avatar(self,msg,*args):

        for user in msg.message.mentions:
            member = user

        if not msg.message.mentions:
            member = msg.author

        avatarurl = member.avatar_url
        memberimg = f'{member.id}.png'
        membernitro = f'{member.id}.gif'
        pth = os.getcwd()
        dst = os.path.join(str(os.getcwd()),'Data/images')
        src2 = os.path.join(dst,memberimg)
        src2g = os.path.join(dst,membernitro)
        src = os.path.join(str(pth),memberimg)
        srcg = os.path.join(str(pth),membernitro)
        images = os.listdir(dst)

        def checkfornitro(user):
            if user.is_avatar_animated():
                return True
            else:
                return False

        isnitro = checkfornitro(member)
        pull = requests.get(avatarurl, allow_redirects=True)

        if isnitro:
            if membernitro in images:
                shutil.move(src2g,pth)
                await msg.channel.send(file=discord.File(membernitro))
                shutil.move(srcg,dst)
                return
            else:
                open(f'{member.id}.gif', 'wb').write(pull.content)
                shutil.move(srcg,dst)

            shutil.move(src2g,pth)
            await msg.channel.send(file=discord.File(membernitro))
            shutil.move(srcg,dst)
            return
        else:
            if memberimg in images:
                shutil.move(src2,pth)
                await msg.channel.send(file=discord.File(memberimg))
                shutil.move(src,dst)
                return
            else:
                open(f'{member.id}.png', 'wb').write(pull.content)
                shutil.move(src,dst)

            shutil.move(src2,pth)
            await msg.channel.send(file=discord.File(memberimg))
            shutil.move(src,dst)

    @commands.command(help='Takes minecraft username and shows its head')
    async def mc(self,msg,*args):

        skin = " ".join(args)

        memberhead = f'{skin}.png'
        link=f'https://mc-heads.net/avatar/{skin}'

        pth = os.getcwd()
        dst = os.path.join(str(os.getcwd()),'Data/minecraft')
        src = os.path.join(str(pth),memberhead)
        src2 = os.path.join(dst,memberhead)
        heads = os.listdir(dst)
        pull = requests.get(link, allow_redirects=True)

        if memberhead in heads:
            shutil.move(src2,pth)
            await msg.channel.send(file=discord.File(memberhead))

            shutil.move(src,dst)
            return
        else:
            open(memberhead,'wb').write(pull.content)
            shutil.move(src,dst)

        shutil.move(src2,pth)
        await msg.channel.send(file=discord.File(memberhead))

        shutil.move(src,dst)

    @commands.command(aliases=['en','bigify','big'], help = 'enlarges any discord custom emoji')
    async def enlarge(self,msg,*emojis: discord.Emoji):

        if len(emojis) > 1:
            return await msg.channel.send('Please only user 1 emoji')

        dst = os.path.join(str(os.getcwd()),'Data/emojis')
        cached = os.listdir(dst)
        pth = os.getcwd()

        for emoji in emojis:

            emojfile = f'{emoji.id}.png'
            url = emoji.url
            src = os.path.join(str(os.getcwd()), f'{emoji.id}.png')
            src2 = os.path.join(dst,f'{emoji.id}.png')
            pull = requests.get(url, allow_redirects=True)

            if emojfile in cached:
                shutil.move(src2,pth)
                await msg.channel.send(file=discord.File(emojfile))
                shutil.move(src,dst)
                return
            else:
                open(emojfile, 'wb').write(pull.content)
                shutil.move(src,dst)

        shutil.move(src2,pth)
        await msg.channel.send(file=discord.File(emojfile))
        shutil.move(src,dst)

    @commands.command(help='shows user spotify status')
    async def spotify(self,msg):

        def chop_microseconds(delta):
            return delta - datetime.timedelta(microseconds=delta.microseconds)

        for user in msg.message.mentions:
            member = user

        if not msg.message.mentions:
            member = msg.author

        for activity in member.activities:

            if isinstance(activity, Spotify):
                dur = chop_microseconds(activity.duration)

                emb = discord.Embed(
                    title = f'{activity.title}',
                    description = f'By **{activity.artist}** on **{activity.album}**',
                    colour = activity.colour,
                    timestamp = activity.created_at
                )

                emb.set_thumbnail(url=activity.album_cover_url)
                emb.add_field(name='Duration', value=f'{dur}' )
                emb.set_footer(text=f'Started listening')

                await msg.channel.send(embed=emb)
                return

    @commands.command(aliases=['gey','gei'], help='Call a user gay (joke)')
    async def gay(self,msg):
        owner = ownerid
        bot = self.client.user.id
        chance = randrange(0,2)

        for user in msg.message.mentions:
            member = user

        if msg.author == member:
            await msg.channel.send('lmao u just called urslef gey')
            return

        if str(member.id) == owner:
            await msg.channel.send('No u')
            return

        if str(member.id) == bot:
            await msg.channel.send('No u')
            return

        if chance:
            await msg.channel.send(f'Hey <@{member.id}> {msg.author.name} Thinks ur mega gey ')
        else:
            await msg.channel.send('No u')

    @commands.command(aliases=['bab'], help='boop')
    async def boop(self,msg):

        member = ''

        for user in msg.message.mentions:
            member = user

        if msg.author == member:
            await msg.channel.send('thou shall not boop thyselef')
            return

        if msg.message.content.startswith('dr/bab'):
            await msg.channel.send(f'✅ Succesfully Babbed `{member.name}`!')
        else:
            await msg.channel.send(f'✅ Succesfully Booped `{member.name}`!')


    @commands.command(aliases=['m'],help='Sends a random meme from reddit')
    async def meme(self, msg:commands.Context):

        fetch:discord.Message = await msg.channel.send("fetching...")
        
    

        req = requests.request("GET",f'https://apis.duncte123.me/meme')

        meme = req.json()

        emb = discord.Embed()

        

        emb.set_image(url=meme["data"]["image"])
        emb.add_field(name="Quality meme", value=f'[{meme["data"]["title"]}]({meme["data"]["url"]})')

        await fetch.edit(embed=emb)


def setup(client):
    client.add_cog(fun(client))
