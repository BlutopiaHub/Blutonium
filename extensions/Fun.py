import discord
from discord import Spotify
from discord.ext import commands
from discord.utils import get
import math, time, datetime, pytz
import os, requests, Setup, shutil
from random import randrange
import humanize as h

def getuser(msg,inp):

    try:
        member = get(msg.guild.members, id=int(inp))
            
    except:

        if inp:
            try:
                member = get(msg.guild.members, name=inp)
                    
            except:
                member = get(msg.guild.members, display_name=inp)

        if  inp is None:
            member : discord.Member = msg.author
        else:
            for men in msg.message.mentions:
                member = men
    return member
        


def request_song_info(song,artist):
    base_url= 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + 'SN6voxG4V5ITlMQAqYCmWZjdcTTzrPF8Vvx5O1g85pWk1ZbnUmdLcEaIeCnKEl0F'}
    search_url = base_url + '/search'
    data = {'q' : song+' '+artist}
    response = requests.get(search_url, data=data, headers=headers)

    return response



class fun(commands.Cog,name="Fun"):
    """
    Fun Commands for messing with friends and having a good time
    """
    def __init__(self, client):
        self.client=client
        self.hypix = Setup.HPapikey
    
    @commands.command(help='The ultimate judge')
    async def pp(self,ctx,*,usr=None): 

        user = getuser(ctx,usr)
        

        length = randrange(1, 25)

        pp = "8"+("="*length)+"D"

        if length > 22:
            lens = "Too long to measure"
            pp = "8====================================================================================D"
        else:
            lens = f'{length} inches'

        if user.id == Setup.ownerid:
            lens="too long to measure"
            pp = "8=========================================================================================D"

        emb= discord.Embed(title=f"{user}'s pp length'")

        emb.add_field(name=lens, value=f"**{pp}**")

        await ctx.channel.send(embed=emb)

    @commands.command(help='Get a users hypixel data')
    async def hypixel(self,msg,query):

        link=f'https://mc-heads.net/avatar/{query}'
        data = requests.request("GET", f"https://api.hypixel.net/player?key={self.hypix}&name={query}").json()

        if data["player"] is None:
            emb= discord.Embed(title='Player not found!!',description=f'Player does not have a hypixel profile or {str(self.client.user).split("#")[0]} failed to get the players information',timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern')))
            emb.set_thumbnail(url=link)
            return await msg.send(embed=emb)
         
        emb = discord.Embed(title=query)

        login = data["player"]["lastLogin"]

        emb.add_field(name='Rank',value=f'**{data["player"]["newPackageRank"]}**')
        #emb.add_field(name='Karma',value=f'**{data["player"]["karma"]}**')
        emb.add_field(name='Last Login',value=f"**{datetime.datetime.fromtimestamp(int(str(login)[:-3])).strftime('%Y-%m-%d %H:%M')}**")
        emb.set_thumbnail(url=link)
        
        await msg.send(embed=emb)

    @commands.command(aliases=['av'], help='Shows user avatar')
    async def avatar(self,msg,*,inp=None):

        member = getuser(msg,inp)

        avatarurl = str(member.avatar_url).split('size=1024')[0] + 'size=1024'
        memberimg = f'{member.id}.png'
        membernitro = f'{member.id}.gif'
        pth = os.getcwd()
        dst = os.path.join(str(os.getcwd()),'Data/images')
        src2 = os.path.join(dst,memberimg)
        src2g = os.path.join(dst,membernitro)
        src = os.path.join(str(pth),memberimg)
        srcg = os.path.join(str(pth),membernitro)
        images = os.listdir(dst)

        async def sendav(src,src2,usr):
            shutil.move(src2,pth)
            await msg.channel.send(file=discord.File(usr))
            shutil.move(src,dst)

        def checkfornitro(user):
            if user.is_avatar_animated():
                return True
            else:
                return False

        isnitro = checkfornitro(member)

        pull = requests.get(avatarurl, allow_redirects=True)

        if isnitro:
            if membernitro in images:
                await sendav(srcg,src2g,membernitro)
                return
            else:
                open(f'{member.id}.gif', 'wb').write(pull.content)
                shutil.move(srcg,dst)

            await sendav(srcg,src2g,membernitro)
            return
        else:
            if memberimg in images:
                await sendav(src,src2,memberimg)
                return
            else:
                open(f'{member.id}.png', 'wb').write(pull.content)
                shutil.move(src,dst)

            await sendav(src,src2,memberimg)
            return

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
    async def spotify(self,msg,*,inp=None):

        def chop_microseconds(delta):
            return delta - datetime.timedelta(microseconds=delta.microseconds)

        member = getuser(msg,inp)

        for activity in member.activities:

            if isinstance(activity, Spotify):
                dur = chop_microseconds(activity.duration)
                artist = activity.artist.split(';')[0]
                query = request_song_info(artist,activity.title)
                try:
                    genius = f'[Lyrics](https://genius.com{query.json()["response"]["hits"][0]["result"]["path"]})'
                except:
                    genius = "Failed to find Lyrics!"

                emb = discord.Embed(
                    title = f'{activity.title}',
                    description = f'By **{activity.artist}** on **{activity.album}**',
                    colour = activity.colour,
                    timestamp = activity.created_at
                )

                emb.set_thumbnail(url=activity.album_cover_url)
                emb.add_field(name='Duration', value=f'{dur}' )
                emb.add_field(name="Genius", value=genius)
                emb.set_footer(text=f'Started listening')

                await msg.channel.send(embed=emb)
                return

    @commands.command(aliases=['gey','gei'], help='Call a user gay (joke)')
    async def gay(self,msg,*,inp=None):
        owner = Setup.ownerid
        bot = self.client.user.id
        chance = randrange(0,2)

        member = getuser(msg,inp)

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
    async def boop(self,msg,*,inp=None):

        member = getuser(msg,inp)

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

        emb = discord.Embed(timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern')))
        emb.set_image(url=meme["data"]["image"])
        emb.add_field(name="Quality meme", value=f'[{meme["data"]["title"]}]({meme["data"]["url"]})')

        await fetch.edit(embed=emb)

def setup(client):
    client.add_cog(fun(client))
