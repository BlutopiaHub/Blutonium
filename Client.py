import discord
from discord.ext import commands
import json
import os
import sqlite3
from Setup import *

conn = sqlite3.connect('Data.db')
c = conn.cursor()

def Checker(**permissions):
    original = commands.has_permissions(**permissions).predicate
    async def extended(ctx):
        if ctx.guild is None:
            return False
        return commands.is_owner() or await original(ctx)
    return commands.check(extended)

def get_prefix(client, message):
    guildid = str(message.guild.id)
    sql = f"SELECT * FROM prefixes WHERE id={guildid}"
  
    c.execute(sql)

    return c.fetchone()[1]

client = commands.Bot(command_prefix=get_prefix)
client.remove_command('help')
client.load_extension('jishaku')
client.owner_id = int(ownerid)

exts = []

for f in os.listdir('./commands'):
    if f.endswith('.py'):
        d = f.replace('.py','')
        exts.append(d)

@client.event
async def on_ready():
    print('Drizzi is Ready!')
    print(f'logged in as {client.user}')

    x = []

    for guild in client.guilds:
        x.append(guild)


    for guild in x:

        guildid = str(guild.id)
        sqlite = f"SELECT * FROM prefixes WHERE id={guildid}"
        c.execute(sqlite)

        bruh = c.fetchone()

        if bruh is None:

            sql = f"INSERT INTO prefixes VALUES ({guild.id},{defprefix})"
            c.execute(sql)
            conn.commit()
            print(f'Sucsessfully set prefix in {guild.name}')
        else:
            print(f"Guild '{guild.name}' has a prefix: {bruh[1]}")

@client.event
async def on_guild_join(guild):
    c.execute(f"INSERT INTO prefixes VALUES ({guild.id}, 'dr/')")
    conn.commit()

@client.command(aliases=['setprefix'], help='Changes the prefix for the server',cog='moderation' )
@commands.check(Checker(administrator=True))
async def changeprefix(msg,*,prefix):

    c.execute(f"UPDATE prefixes SET prefix = '{prefix}' WHERE id = {msg.guild.id}" )
    conn.commit()

    emb = discord.Embed(title=f'{msg.guild}', description='The prefix for this server was successfully changed!', color=discord.Colour.green())
    emb.add_field(name='Changed to:', value=f'{prefix}')
    await msg.channel.send(embed=emb)

@client.event
async def on_message(msg):

    messagec : str = msg.content

    if msg.guild is None:
        return print(f'{msg.author}-{messagec}')

    if messagec.startswith('<@'):

        if client.user in msg.mentions:
            await msg.add_reaction('❤️')
            return await msg.channel.send(f'Hi! My prefix for this server is ``{get_prefix(client,msg)}``')

    await client.process_commands(msg)

if __name__ == '__main__':

    for ext in exts:
        try:
            client.load_extension(f'commands.{ext}')
            print(ext)
        except Exception as error:
            print(f'[CONSOLE] {ext} CANT BE LOADED: {error}')

client.run(TOKEN)
