import discord
from discord.ext import commands
import json
import os
import MySQLdb
from Setup import *
import random


def get_prefix(client, message):
    db = MySQLdb.connect(host=sqhost, user=squname, passwd=sqpassword, db=sqdbname)
    cursor = db.cursor()

    guildid = str(message.guild.id)
    sql = f"SELECT * FROM prefixes WHERE id={guildid}"  
    cursor.execute(sql)
    prefix = cursor.fetchone()[1]
    db.close()
    return prefix

def getprefix(guild):
    db = MySQLdb.connect(host=sqhost, user=squname, passwd=sqpassword, db=sqdbname)
    cur = db.cursor()

    guildid = str(guild.id)
    sql = f"SELECT * FROM prefixes WHERE id={guildid}"  
    cur.execute(sql)
    prefix = cur.fetchone()[1]
    db.close()

    return prefix

def get_blacklist():
    db = MySQLdb.connect(host=sqhost, user=squname, passwd=sqpassword, db=sqdbname)
    cursor = db.cursor()

    sql = "SELECT * FROM blacklist"
    cursor.execute(sql)
    query = cursor.fetchall()
    blacklist = []
    for x in query:
        blacklist.append(x[0])
    db.close()
    return blacklist


client = commands.Bot(command_prefix=get_prefix)
client.remove_command('help')
client.load_extension('jishaku')
client.owner_id = int(ownerid)

exts = []

@client.event
async def on_message(msg):

    if msg.channel is discord.DMChannel:
        print(msg.content)

    prefix = getprefix(msg.channel.guild)
    msgc:str=msg.content


    if msgc.startswith('<@'):

        if client.user in msg.mentions:

            responses = [
            f'Hey! my prefix for this server is `{prefix}` ',
            f'No `{prefix}`',
            f'WHAT DO YOU WA- .. uhh i mean hi. my prefix is `{prefix}`',
            f'Oi mate heres ya prefix, cheers! `{prefix}`',
            f'We\'re sorry, {client.user} is unavalible right now. Please use this prefix `{prefix}`',
            f'imagine forgeting your prefix, `{prefix}`',
            f'TIP: use `{prefix}setprefix (whatever u want)` to change your prefix'
            ]

            resonse = random.choice(responses)

            await msg.channel.send(resonse)


    bl = get_blacklist()
    if msg.author.id in bl:
        if msgc.startswith(f"{prefix}"):
            return await msg.channel.send("You have been blacklisted from using this discord bot!")
    else:
        await client.process_commands(msg)

for f in os.listdir('./extensions'):
    if f.endswith('.py'):
        d = f.replace('.py','')
        exts.append(d)

if __name__ == '__main__':

    for ext in exts:
        try:
            client.load_extension(f'extensions.{ext}')
            print(ext)
        except Exception as error:
            print(f'[CONSOLE] {ext} CANT BE LOADED: {error}')            

client.run(TOKEN)