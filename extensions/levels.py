from PIL import Image, ImageDraw, ImageOps, ImageFont
from purgo_malum import client as purgoclient
from io import BytesIO
import os, sys, requests, datetime, random, pytz
from discord.ext import commands
from discord.utils import get
from blutapi import getuser, getprefix, getbackground, setbackground, leveluser,getleveldata,genleveldata,getaccent,setaccent,gettext,settext, query_database
import discord, pg8000, Setup

class levels(commands.Cog,name='Levels'):


    def __init__(self,client):

        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self,msg):
        
        ctx = await self.client.get_context(msg)

        if ctx.valid:
            if ctx.command:
                return 

        res = leveluser(msg.author, msg.guild)

    @commands.command()
    async def rank(self,ctx:commands.Context,*,user=None):

        support = get(self.client.guilds , id=629436501964619776)
        emoji = get(support.emojis, name="Blutonium_loading")
        emoji2 = get(support.emojis, name="BlutoX")
        emb = discord.Embed(title=f'{emoji} Generating rank card...')

        msg = await ctx.send(embed=emb)

        colors = (('green', '#27d600'), ('blue', '#0064d6'), ('red','#e30000'), ('white', '#ffffff'), ('black', '#000000'), ('gold','#ffd500'), ('pink', '#ff75fa'), ('purple', '#8400ff'))
        try:

            user = getuser(ctx,user)
            leveldata = getleveldata(user,ctx.guild)[0]

            masksize = (700,700)
            mask = Image.new('L', masksize, 0)

            Maskdraw = ImageDraw.Draw(mask)
            Maskdraw.ellipse((0,0) + masksize, fill='#fff')

            mask = ImageOps.fit(mask,(160,160))

            aurl = '.'.join(str(user.avatar_url).split('.')[:3]) + '.png'

            pfp = requests.get(aurl)
            link = getbackground(user)

            print(link)

            TINT_COLOR = (0, 0, 0)
            TRANSPARENCY = .60
            OPACITY = int(255 * TRANSPARENCY) 
            
            accent = getaccent(user)

            if accent is None:
                accent = '#FFF'

            for x in colors:

                if accent == x[0]:
                    accent = x[1]

            if ctx.guild.id == 264445053596991498:
                image = requests.get('https://img.wallpapersafari.com/desktop/1920/1080/89/4/6KjDH9.jpg')
            else:
                try:
                    image = requests.get(link)
                except:
                    image = requests.get('https://img.wallpapersafari.com/desktop/1920/1080/89/4/6KjDH9.jpg')

            profile = Image.open(BytesIO(pfp.content))
            circular = ImageOps.fit(profile, mask.size)
            circular.putalpha(mask)
            
            circular = circular.convert('RGBA')
            #image = Image.new('RGBA', (700,200), '#424242')
            image = Image.open(BytesIO(image.content))
            #image = image.resize((700,200))
            image = ImageOps.fit(image,(700,200))

            #draw.rectangle((10,10,690,190),fill=(0,0,0,200), outline='#fff',width=3)

            rec = Image.new('RGBA', image.size, TINT_COLOR+(0,))
            drew = ImageDraw.Draw(rec)
            drew.rectangle((10,10,690,190),fill=TINT_COLOR+(OPACITY,))

            image = image.convert('RGBA')
            image = Image.alpha_composite(image, rec)
        
            draw = ImageDraw.Draw(image)

            font = ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), 32)
            font2 = ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), 18)
            font3 = ImageFont.truetype(os.path.join('fonts', 'arial.ttf'), 25)

            image.paste(circular,(20,20,180,180),mask=mask)
            draw.text((200,50), f'{user}',align='center', font=font, fill=accent)

            text = gettext(user)

            if text is None:
                text = " "
            
            text = purgoclient.retrieve_filtered_text(text)

            draw.text((200,85), f'{text}',align='center', font=font3, fill=accent)
            
            draw.text((548,145), f'{leveldata[3]} / {leveldata[4]}xp',align='center', font=font2, fill=accent)
            draw.text((200,145), f'Level {leveldata[2]}',align='center', font=font2, fill=accent)

            recbox = (200,120,630,140)

            levelpercentage = round(((leveldata[3]/leveldata[4])*100))

            fill = ((levelpercentage*430)/100) + 200

            recboxfill = (200,120,fill,140)
            draw.rectangle(recbox)
            draw.rectangle(recboxfill, fill=accent)
        except Exception as err:

            if user is None:
                error = 'User not found!'
            else:
                error = err

            emb=discord.Embed(title=f'{emoji2} Rank card Failed: {error}')
            await msg.edit(embed=emb)

        path = f"/media/home/FS2/WEB/blutopia.ca/img/blutonium/{ctx.guild.id}/{user.id}.png"
        image.save(path, format='PNG')
        
        
        link = f'https://img.blutopia.ca/blutonium/{ctx.guild.id}/{user.id}.png'

        req = requests.get(link)

        img = BytesIO(req.content)
        img.name = f"{user.id}.png"
        
        file = discord.File(img)

        await msg.delete()
        await ctx.send(file=file)

 #   @rank.error
 #   async def rank_handler(self,ctx,error):
#
 #       if isinstance(error, ValueError):
#
  #          ctx.send('Invalid Image color space! please change your background.')
 #       else:
 #           print(error)

    @commands.command()
    async def rankcard(self,ctx,*kwargs):


        try:
            
            if kwargs[0] == "--background":

                
                if ctx.guild.id == 264445053596991498:
                    return await ctx.send('Backgrounds are disabled in this server')

                link = kwargs[1]

                setbackground(ctx.author,link)

                await ctx.send('Successfully set background')
            
            elif kwargs[0] == "--accent":

                colors = ['green','blue','red', 'white', 'black', 'gold', 'pink','purple']

                try:

                    if kwargs[1].startswith('#'):
                        if len(kwargs[1]) > 7:
                            return await ctx.send('Invalid HEX code')
                        
                        if len(kwargs[1]) < 7:

                            if len(kwargs[1]) == 4:
                                pass
                            else:
                                return await ctx.send('Invalid HEX code')
                        
                        setaccent(ctx.author, kwargs[1])
                        return await ctx.send('Accent color successfully changed')
                    elif kwargs[1].lower() in colors:

                        setaccent(ctx.author,kwargs[1].lower())
                        return await ctx.send('Accent color successfully changed')
                    else:
                        raise KeyError
                        
                except:
                    
                    return await ctx.send(f'Invalid color! Options are ``{", ".join(colors)} `` or a HEX code')

            elif kwargs[0] == "--text":

                text = ' '.join(kwargs[1:])
                if len(text) > 30:
                    return await ctx.send("text too long")
                
                settext(ctx.author,text)
                return await ctx.send('Text successfully changed')
            else:
                raise KeyError

        except Exception as err:

            print(err)
            accent = getaccent(ctx.author)
            prefix = getprefix(ctx.guild)
            text = gettext(ctx.author)
            text = purgoclient.retrieve_filtered_text(text)
            bg = getbackground(ctx.author)

            emb = discord.Embed(title=f'{ctx.author} rank card configuration',timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern')),colour=0x36393F)

            emb.add_field(name='Background',value=f'\n**Current:** {bg}\n**Usage:** {prefix}rankcard --background [img link]', inline=False)
            emb.add_field(name='Accent Color',value=f'\n**Current:** {accent}\n**Usage:** {prefix}rankcard --accent [color]\n leave the color blank to see all the options', inline=False)
            emb.add_field(name='Custom Text',value=f'\n**Current:** {text}\n**Usage:** {prefix}rankcard --text [text]', inline=False)
            emb.set_thumbnail(url=ctx.author.avatar_url)

            await ctx.send(embed=emb)


    @commands.command()
    async def levels(self,ctx,glbl=None):
        
        if glbl is None:
            levels = query_database(f"SELECT userid,currentlevel,currentxp,requiredxp FROM levels WHERE guildid = {ctx.guild.id} ORDER BY currentlevel DESC, currentxp DESC LIMIT 10")
            emb = discord.Embed(title=f'{ctx.guild} Leaderboard',timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern')),colour=0x36393F)
        if glbl == 'global':
            emb = discord.Embed(title=f'Global Leaderboard',timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern')),colour=0x36393F)
            levels = query_database(f"SELECT userid,currentlevel,currentxp,requiredxp FROM levels ORDER BY currentlevel DESC, currentxp DESC LIMIT 10")
       
        emb.set_thumbnail(url=ctx.guild.icon_url)

        q = 1

        for x in levels:
            
            user = getuser(ctx,x[0])
            
            if x[1] == 0:
                pass
            else:

                emb.add_field(name=f'#{q} - {user.mention}', value=f"Level {x[1]} | {x[2]}/{x[3]}xp", inline=False)

            q += 1
        
        await ctx.send(embed=emb)


        

def setup(client):
    client.add_cog(levels(client))