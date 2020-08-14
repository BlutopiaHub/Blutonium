from discord.ext import commands
from discord.utils import get
import json, discord
import random , os
from Setup import TOKEN, ownerid
import asyncio
import blutapi

client = commands.Bot(command_prefix=blutapi.get_prefix)
client.remove_command('help')
client.load_extension('jishaku')
client.owner_id = int(ownerid)

exts = []

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

@client.event
async def on_message(msg):

    if msg.channel is discord.DMChannel:
        print(msg.content)

    prefix = blutapi.getprefix(msg.channel.guild)
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
            f'TIP: use `{prefix}cfg prefix (whatever u want)` to change your prefix'
            ]

            resonse = random.choice(responses)

            await msg.channel.send(resonse)


    bl = blutapi.get_blacklist()
    if msg.author.id not in bl:
        
        await client.process_commands(msg)

        author = msg.author

        def check(before, after):
            return before.content == msgc and before.author == author and after.content != before.content

        try:
            before, after = await client.wait_for('message_edit', timeout=5.0, check=check)
        except asyncio.TimeoutError:
            return
        else:
            return await client.process_commands(after)

    else:
        if msgc.startswith(prefix):

            await msg.channel.send("You have been blacklisted from using this bot")
        


client.run(TOKEN)