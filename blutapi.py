import pg8000, os, time
import Setup,discord,datetime
from random import randrange
from discord.utils import get

def bkupgetlogdata(guild):
    
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
    
    data = data[0]
    conn.close()
    return data

def getlogdata(guild):

    db = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"select guildid,logs,logchannelid from guilddata where guildid = {guild.id} "

    data = db.run(sql)[0]

    if data[2] == 0:
        
        chan = get(guild.channels, name='logs')

        if chan is None:
            chan = get(guild.channels, name='Logs')

        if chan is None:

            sql = f'UPDATE guilddata set logs = False WHERE guildid = {guild.id}'
            db.run(sql)
            db.commit()
            data = (guild.id,False,0)
        else:

            sql = f'UPDATE guilddata set logchannelid = {chan.id} WHERE guildid = {guild.id}'
            db.run(sql)
            db.commit()
            data = (guild.id, True, chan.id)

    db.close()
    return data    

def get_prefix(client, message):

    guild = message.guild
    conn = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    prefix = getprefix(guild)

    conn.close()

    return prefix

async def genguilddata(guild):

    conn = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)
    sql = f'SELECT guildid from guilddata WHERE guildid = {guild.id}'

    res = conn.run(sql)

    if res:
        conn.commit()
        conn.close()
        return f"guild data for {guild} found!"


    logchan = get(guild.channels, name='logs')

    if logchan is None:
        logchan = get(guild.channels, name='Logs')
        
    if logchan is None:

        logchan = 0
        logs = False

    logs = True
    muterole = await getMuteRole(guild)

    prefix = 'b/'

    sql2 = f"INSERT INTO guilddata (guildid,adminroles,logs,muterole,prefix,logchannelid) VALUES ({guild.id},null,{logs},{muterole.id},'{prefix}',{logchan})"
    
    try:
        res = conn.run(sql2)
    except:
        conn.commit()
        conn.close()

        conn2 = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)
        
        sql3 = f"INSERT INTO guilddata (guildid,adminroles,logs,muterole,prefix,logchannelid) VALUES ({guild.id},null,{logs},{muterole.id},'b/',0)"

        res = conn2.run(sql3)

        conn2.commit()
        conn2.close()

        return f"guild data generated for in recovery mode {guild}"

    conn.commit()
    conn.close()
    
    path = f"/media/home/FS2/WEB/blutopia.ca/img/blutonium/{guild.id}"
    if not os.path.exists(path):
    
        os.mkdir(path)

    return f"guild data generated for {guild}"

def getprefix(guild):

    guildid = guild.id
    conn = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"SELECT prefix FROM guilddata WHERE guildid={guildid}"  
    prefix = conn.run(sql)

    conn.close()
    return prefix[0][0]

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

    sql = f"UPDATE guilddata SET prefix = '{prefix}' WHERE guildid = {guild.id}"

    conn.run(sql)
    conn.commit()
    conn.close()

def setlogchannel(guild,channelid):

    logdata = getlogdata(guild)

    conn = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"UPDATE guilddata set logchannelid = {channelid} where guildid = {guild.id}"

    conn.run(sql)

    conn.commit()
    conn.close()

    return 0

def togglelogs(guild):

    conn = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"SELECT logs from guilddata where guildid = {guild.id}" 

    q = conn.run(sql)[0][0]

    if q:
        sql = f"UPDATE guilddata SET logs = False WHERE guildid = {guild.id}"
        conn.run(sql)
        conn.commit()
        conn.close()
        return 0
    else:
        sql = f"UPDATE guilddata SET logs = True WHERE guildid = {guild.id}"
        conn.run(sql)
        conn.commit()
        conn.close()
        return 1

async def getMuteRole(guild):

    class fakerole():

        def __init__(self):
            self.id=00000000000000000000

    conn = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"SELECT muterole FROM guilddata WHERE guildid = {guild.id}"

    try:
        role = conn.run(sql)[0][0]
    except:
        role = None
    
    if not role:

        muterole = get(guild.roles, name='Muted')

        if muterole is None:
            muterole = get(guild.roles, name='muted')
        
        if muterole is None:

            try:
                role = await guild.create_role(name="muted")
            except:
                print(f"unable to create muterole for {guild}")
                muterole = fakerole()
                
                sql = f"UPDATE guilddata set muterole = {muterole.id} where guildid = {guild.id}"
                conn.run(sql)

                conn.commit()
                conn.close()

                return muterole

            for channel in guild.text_channels:

                await channel.set_permissions(role, send_messages=False, read_messages=True)

            sql = f"UPDATE guilddata set muterole = {role.id} where guildid = {guild.id}"
            conn.run(sql)

            conn.commit()
            conn.close()
            return role
        
        sql = f"UPDATE guilddata set muterole = {muterole.id} where guildid = {guild.id}"
        conn.run(sql)

        conn.commit()
        conn.close()
        return muterole
    
    try:
        muterole = get(guild.roles, id=role)
    except:
        muterole = None

    conn.commit()
    conn.close()

    return muterole

def setMuteRole(guild,roleid):

    conn = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"UPDATE guilddata SET muterole = {roleid} WHERE guildid = {guild.id}"
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

def query_database(sql):

    db = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    try:
        res = db.run(sql)
    except Exception as err:
        return err
        
    db.commit()
    db.close()
    return res

def genuserdata(user):

    db = pg8000.connect(Setup.dbuname, database = 'betonium', password=Setup.dbpassword)

    sql = f'INSERT INTO userdata (userid,points,messages,cmduses,claimed,rankimage,ranktext,rankaccent) VALUES ({user.id},0,0,0,null,null,null,null)'

    db.run(sql)

    db.commit()
    db.close()

    return print(f'userdata generated! for {user}')

def getusers():

    db = pg8000.connect(Setup.dbuname,password=Setup.dbpassword)

    sql = f'SELECT userid FROM points'
    res = db.run(sql)

    ids = []

    for x in res:
        ids.append(x[0])
    
    db.close()
    return ids

def getpoints(user):

    db = pg8000.connect(Setup.dbuname,password=Setup.dbpassword)

    sql = f"SELECT points FROM userdata WHERE userid = {user.id}"

    res = db.run(sql)

    if res:
        
        points = res[0][0]
    
    else:

        points = 0
        genuserdata(user)

    db.close()
    return points

def setpoints(user, ammount):

    db = pg8000.connect(Setup.dbuname,password=Setup.dbpassword)
    sql = f'UPDATE userdata SET points = {ammount} WHERE userid = {user.id}'

    res = db.run(sql)

    db.commit()
    db.close()
    return

import pg8000

def getclaimed(user):

    db = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f'SELECT claimed FROM userdata WHERE userid = {user.id}'

    res = db.run(sql)
    
    if res[0][0] is None:

        sql = f'UPDATE userdata SET claimed = now() WHERE userid = {user.id}'
        db.run(sql)
        db.commit()

        sql = f'SELECT claimed FROM userdata WHERE userid = {user.id}'
        res = db.run(sql)

        nextclaim = datetime.timedelta(hours=24) + res[0][0]

        db.close()
        return (True, nextclaim)

    else:

        now = datetime.datetime.now()
        claimed = res[0][0]
        nextclaim = claimed + datetime.timedelta(hours=24)

        if now < nextclaim:
            print('You cant')
            db.close()
            return (False, nextclaim)
        else:
            print('you can')
        
            sql = f'UPDATE userdata set claimed = now() WHERE userid = {user.id}'
            db.run(sql)
            db.commit()
            db.close()
            return (True, nextclaim)

def getleaderboard(guild):

    ids = []

    for user in guild.members:

        ids.append(user.id)

    ids = str(ids).replace('[', '(')

    ids = ids.replace(']',')')

    db = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f'SELECT userid,points FROM userdata WHERE userid IN {ids} ORDER BY points DESC LIMIT 10'

    res = db.run(sql)

    return res


def getbackground(user):

    db = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"SELECT rankimage FROM userdata WHERE userid = {user.id}"

    res = db.run(sql)

    db.close()

    return res[0][0]

def setbackground(user, link):

    db = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"UPDATE userdata SET rankimage = '{link}' WHERE userid = {user.id}"

    db.run(sql)

    db.commit()
    db.close()

    return

def gettext(user):

    db = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"SELECT ranktext FROM userdata WHERE userid = {user.id}"

    res = db.run(sql)

    db.close()

    return res[0][0]

def settext(user, text):

    db = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"UPDATE userdata SET ranktext = '{text}' WHERE userid = {user.id}"

    db.run(sql)

    db.commit()
    db.close()

    return

def getaccent(user):

    db = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"SELECT rankaccent FROM userdata WHERE userid = {user.id}"

    res = db.run(sql)

    db.close()

    return res[0][0]

def setaccent(user, color):

    db = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"UPDATE userdata SET rankaccent = '{color}' WHERE userid = {user.id}"

    db.run(sql)

    db.commit()
    db.close()

    return

def getuser(client,inp):

    members = client.get_all_members()

    try:
        member = get(members, id=int(inp))
            
    except:

        if inp:
            
            member = get(members, name=inp)
                    
            if member is None:

                member = get(members, display_name=inp)
            
            if member is None:
                try:
                    bro = inp.split('#')

                    member = get(members, name=bro[0], discriminator=bro[1] )
                except:
                    pass

        if  inp is None:
            member : discord.Member = msg.author
        else:
            for men in msg.message.mentions:
                member = men
    return member

def getleveldata(user,guild):

    db = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    sql = f"SELECT * FROM levels WHERE userid = {user.id} AND guildid = {guild.id}"

    res = db.run(sql)

    db.close()

    return res

def genleveldata(user,guild):

    db = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)

    now = time.time()

    sql = f"INSERT INTO levels (guildid,userid, currentlevel, currentxp, requiredxp, lastxp ) VALUES ({guild.id}, {user.id}, 0, 0, default, {now})"

    db.run(sql)

    db.commit()
    db.close()

    return


def leveluser(user,guild):

    db = pg8000.connect(Setup.dbuname, password=Setup.dbpassword)
    # get initial level data
    res = getleveldata(user,guild)

    try:
        cooldown = res[0][5] + 60.0
    except:
        pass

    leveldup = (0,0)

    # if theres no level data generate it
    if not res:
        return genleveldata(user,guild)
    # if cooldown is over    
    
    elif float(time.time()) > cooldown:

        res = res[0]
        xpGained = randrange(5,10)
        newxp = int(res[3]) + xpGained
        now = time.time()

        # if the xp is over or equal to the required xp increment the level
        if newxp >= int(res[4]):
            
            vnewxp = xpGained - (res[4] - int(res[3]))

            newlevel = int(res[2]) + 1

            leveldup = (1,newlevel)

            db.run(f"UPDATE levels SET (currentxp,lastxp,currentlevel) = ({vnewxp},{now},{newlevel}) WHERE userid = {user.id} AND guildid = {guild.id}")
        else:
            db.run(f"UPDATE levels SET (currentxp,lastxp) = ({newxp}, {now}) WHERE userid = {user.id} AND guildid = {guild.id}")

    db.commit()    
    db.close()
    
    return leveldup


    
        