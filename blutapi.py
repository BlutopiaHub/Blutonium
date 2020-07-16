import pg8000
import Setup
import discord
from discord.utils import get

def getlogdata(guild):

    logchan = get(guild.channels, name='logs')

    if chan is None:
        chan = get(guild.channels, name='Logs')

    if chan is None:
        logdata = (guild.id, False, 0000000000000000000000)
        return logdata

    logdata = (guild.id, True, chan.id)
    return logdata

def get_prefix(client, message):

    prefix = Setup.defprefix

    return prefix


def getprefix(guild):

    prefix = Setup.defprefix

    return prefix

def get_blacklist():

    ## ENTER USER ID's FOR BLACKLIST HERE!
    blacklist = []

    return blacklist

async def getMuteRole(guild):

    muterole = get(guild.roles, name='Muted')

    if muterole is None:
        muterole = get(guild.roles, name='muted')
        
    if muterole is None:

        muterole = await guild.create_role(name="muted")

        for channel in guild.text_channels:

            await channel.set_permissions(muterole, send_messages=False, read_messages=True)

        return role
        
    return muterole

