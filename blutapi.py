import pg8000
import Setup
import discord
from discord.utils import get

def getlogdata(guild):
    
    conn = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"SELECT * FROM logdata WHERE guildid = {guild.id}"
    data = conn.run(sql)
    

    if not data:

        chan = get(guild.channels, name='logs')

        if chan is None:
            chan = get(guild.channels, name='Logs')
        
        if chan is None:
            chanid = 0000000000000000000
        else:
            chanid = chan.id
        
        sql = f"INSERT INTO logdata (guildid, isenabled, channelid) VALUES ({guild.id}, True, {chanid})"
        conn.run(sql)
        conn.commit()

        data = (guild.id,True,chanid)
        conn.close()
        return data
    
    conn.close()

    data = data[0]
    return data

def get_prefix(client, message):

    guildid = message.guild.id
    conn = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"SELECT * FROM prefix WHERE id={guildid}"  
    prefix = conn.run(sql)

    if not prefix:
        sql = f"INSERT INTO prefix (id, prefix) VALUES ({guildid},'{Setup.defprefix}')"
        conn.run(sql)
        conn.commit()

        sql = f"SELECT * FROM prefix WHERE id={guildid}"  
        prefix = conn.run(sql)

    conn.close()

    return prefix[0][1]

def getprefix(guild):

    guildid = guild.id
    conn = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"SELECT * FROM prefix WHERE id={guildid}"  
    prefix = conn.run(sql)

    if not prefix:
        sql = f"INSERT INTO prefix (id, prefix) VALUES ({guildid},'b/')"
        conn.run(sql)
        conn.commit()

        sql = f"SELECT * FROM prefix WHERE id={guildid}"  
        prefix = conn.run(sql)

    conn.close()

    return prefix[0][1]

def get_blacklist():

    conn = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"SELECT * FROM blacklist"
    q = conn.run(sql)
    blacklist = []

    if q:
        for x in q:
            blacklist.append(x[0])

    conn.commit()
    conn.close()

    return blacklist

def blacklist_user(id):

    conn = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"INSERT INTO blacklist (userid) VALUES ({id})"
    conn.run(sql)

    conn.commit()
    conn.close()

def unblacklist_user(id):

    conn = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"DELETE FROM blacklist WHERE userid = {id}"
    conn.run(sql)

    conn.commit()
    conn.close()

def update_prefix(guild, prefix):

    conn = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"UPDATE prefix SET prefix = '{prefix}' WHERE id = {guild.id}"

    conn.run(sql)
    conn.commit()
    conn.close()

def setlogchannel(guild,channelid):

    logdata = getlogdata(guild)

    conn = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"UPDATE logdata set channelid = {channelid} where guildid = {guild.id}"

    conn.run(sql)

    conn.commit()
    conn.close()

    return 0

def togglelogs(guild):

    conn = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"SELECT isenabled from logdata where guildid = {guild.id}" 

    q = conn.run(sql)[0][0]

    if q:
        sql = f"UPDATE logdata SET isenabled = False WHERE guildid = {guild.id}"
        conn.run(sql)
        conn.commit()
        conn.close()
        return 0
    else:
        sql = f"UPDATE logdata SET isenabled = True WHERE guildid = {guild.id}"
        conn.run(sql)
        conn.commit()
        conn.close()
        return 1

async def getMuteRole(guild):

    conn = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"SELECT roleid FROM muterole WHERE guildid = {guild.id}"
    role = conn.run(sql)
    
    if not role:

        muterole = get(guild.roles, name='Muted')

        if muterole is None:
            muterole = get(guild.roles, name='muted')
        
        if muterole is None:

            role = await guild.create_role(name="muted")

            for channel in guild.text_channels:

                await channel.set_permissions(role, send_messages=False, read_messages=True)

            sql = f"INSERT INTO muterole (guildid, roleid) VALUES ({guild.id}, {role.id})"
            conn.run(sql)

            conn.commit()
            conn.close()
            return role
        
        sql = f"INSERT INTO muterole (guildid, roleid) VALUES ({guild.id}, {muterole.id})"
        conn.run(sql)

        conn.commit()
        conn.close()
        return muterole
    
    try:
        muterole = get(guild.roles, id=role[0][0])
    except:
        muterole = None

    conn.commit()
    conn.close()

    return muterole

def setMuteRole(guild,roleid):

    conn = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"UPDATE muterole SET roleid = {roleid} WHERE guildid = {guild.id}"
    conn.run(sql)

    conn.commit()
    conn.close()

def getAdminRoles(guild):

    conn = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"SELECT roleid FROM adminroles WHERE guildid = {guild}"
    res = conn.run(sql)

    conn.commit()
    conn.close()

    return res

def remAdminRole(roleid):

    conn = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"DELETE FROM adminroles WHERE roleid = {roleid}"
    res = conn.run(sql)

    conn.commit()
    conn.close()

def addAdminRole(guild, roleid):

    conn = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"INSERT INTO adminroles (guildid, roleid) VALUES ({guild.id}, {roleid})"
    res = conn.run(sql)

    conn.commit()
    conn.close()

