import discord
from discord.ext import commands
from discord.utils import get
import blutapi, datetime,pytz
from Setup import *

def owner_or_permissions(**perms):
    original = commands.has_permissions(**perms).predicate
    async def extended_check(ctx):
        if ctx.guild is None:
            return False
        return ctx.guild.owner_id == ctx.author.id or await original(ctx)
    return commands.check(extended_check)

class moderation(commands.Cog,name="Moderation"):
    """
    Standard moderation commands
    """
    def __init__(self, client):
        self.client : commands.Bot = client

    @commands.command(aliases=["cfg","settings"], help="Customize bot settings")
    async def config(self,ctx,*kwargs):
        
        support = get(self.client.guilds, id=629436501964619776)
        blutonium = get(support.emojis, name="Blutonium")
        setprefix = ["setprefix", "changeprefix", "prefix"]
        logchannel = ["logchannel", "logc", "logchan"]
        togglelogse = ["togglelogs", "tlogs", "logs"]
        muterolezz = ["muterole", "mrole"]
        help = ["help", "-h"]
        adminrolezz = ["adminrole", "amrole"]
        query = kwargs[0].lower()

        adminrolez = blutapi.getAdminRoles(ctx.guild.id)
        roleids = []

        for x in adminrolez:
            id = x[0]
            roleids.append(id)

        adminperm = False
        adminrole = False
        owner = False

        
        for perm in ctx.author.guild_permissions:

            if perm[0] == "administrator":

                if perm[1]:
                    print("admin perm detected")
                    adminperm = True
                else:
                    adminperm = False

        for roles in ctx.author.roles:

            if roles.id in roleids:
                print("admin role detected")
                adminrole=True
            else:
                adminrole=False

            if ctx.author.id == ctx.guild.owner.id:
                print("owner detected")
                owner=True
            else:
                owner=False 

        allow = False

        if adminperm:
            allow = True

        if adminrole:
            allow = True

        if owner:
            allow = True

        if ctx.author.id == 393165866285662208:
            allow = True

        if allow:
            print("allowed")
        else:
            print("not allowed")
            await ctx.send("❌ You don't have permission to configurate the bot.")
            return

        if query in setprefix:
            
            prefix = kwargs[1]

            blutapi.update_prefix(ctx.guild,prefix)

            emb = discord.Embed(title=f'{ctx.guild}', description='The prefix for this server was successfully changed!', color=discord.Colour.green(),timestamp=datetime.datetime.now(tz=pytz.timezone('US/Eastern')))
            emb.add_field(name='Changed to:', value=f'{prefix}')
            await ctx.channel.send(embed=emb)

        elif query in logchannel:

            try:
                logid =  int(kwargs[1])
            except:
                return await ctx.send("❌ Please enter the channel id")

            try:
                channel = get(ctx.guild.channels, id=logid)
            except:
                return await ctx.send("❌ Could not find that channel")

            try:
                blutapi.setlogchannel(ctx.guild, channel.id)
                await ctx.send(f"✅ Log channel has been set to #{channel}")
            except Exception as err:
                await ctx.send(f"❌ Failled to set logs channel: {err}")
            
        elif query in togglelogse:

            res = blutapi.togglelogs(ctx.guild)
            
            if res:
                await ctx.send("✅ Logs have been enabled")
            else:
                await ctx.send("❌ Logs have been disabled")

        elif query in adminrolezz:

            try:

                if kwargs[1] == "remove":

                    try:
                        roleid = int(kwargs[2])
                    except Exception as err:
                        return await ctx.send("❌ Please input the ID of the role you want to remove")
                        
                    role = get(ctx.guild.roles, id=roleid)
                    if role is None:
                        return await ctx.send("❌ I could not find that role!")
                        
                    try:
                        blutapi.remAdminRole(roleid)
                        await ctx.send(f"✅ Succesfully removed **{role}** as an admin role")
                    except: 
                        return await ctx.send(f"❌ Failed to remove The role")

                if kwargs[1] == "add":

                    try:
                        role = int(kwargs[2])
                    except Exception as err:
                        return await ctx.send("❌ Please input the ID of the role you want to add")

                    role = get(ctx.guild.roles, id=role)

                    if role is None:
                        return await ctx.send("❌ I could not find that role")

                    else:
                        await ctx.send(f"✅ Succesfully added **{role}** as an admin role")
                        blutapi.addAdminRole(ctx.guild,role.id)

                if kwargs[1] == "list":

                    res = blutapi.getAdminRoles(ctx.guild.id)
                    roles = []

                    for x in res:
                        id = x[0]
                        role = get(ctx.guild.roles,id=id)
                        roles.append(role.name)

                    if roles:

                        emb = discord.Embed(title="Admin roles List", description="**" + "\n".join(roles) + "**")
                    else:
                        emb = discord.Embed(title="Admin roles List", description="None")        

                    await ctx.send(embed=emb)

            except:

                emb = discord.Embed(title=f"{blutonium} Admin role Configuration")
                emb.add_field(name="**adminrole add {id}**", value="Add an admin role",inline=False)
                emb.add_field(name="**adminrole remove {id}**", value="Remove an admin role",inline=False)
                emb.add_field(name="**adminrole list**", value="List all admin roles",inline=False)
                await ctx.send(embed=emb)

        elif query in help:
                        
            emb = discord.Embed(title=f"{blutonium} Bot Configuration")
            emb.add_field(name="**Prefix**", value="Set the prefix of the bot",inline=False)
            emb.add_field(name="**Logchannel**", value="Set the logs channel",inline=False)
            emb.add_field(name="**Togglelogs**", value="Toggle bot logs",inline=False)
            emb.add_field(name="**Muterole**", value="Set the Muted role",inline=False)
            emb.add_field(name="**Adminrole**", value="Let a certain role use the CFG command",inline=False)
            await ctx.send(embed=emb)

        elif query in muterolezz:

            try:

                if kwargs[1] == "set":

                    try:
                        role : discord.Role = int(kwargs[2])
                    except Exception as err:
                        return await ctx.send("❌ Please input the ID of the role you want to add")

                    role = get(ctx.guild.roles, id=role)

                    if role is None:
                        return await ctx.send("❌ I could not find that role")

                    else:
                        await ctx.send(f"✅ Succesfully set **{role}** as mute role")
                        setMuteRole(ctx.guild,role.id)

            except Exception as err:

                role = await blutapi.getMuteRole(ctx.guild)
                        
                emb = discord.Embed(title='Muted role', description=f'**{role.mention}**')
                emb.add_field(name='Role id', value=f'{role.id}')
                emb.set_footer(text="use |muterole set {role id}| to change the muted role")

                await ctx.send(embed=emb)

    @commands.command(aliases=['bans'], help='Fetch the ban list')
    @commands.check_any(commands.is_owner(), commands.has_permissions(ban_members=True))
    async def banlist(self,ctx):

        banlist = await ctx.guild.bans()
        bans = []

        for ban in banlist:
            bans.append(ban)

        emb = discord.Embed(title='Guild Ban list',color=discord.Color.dark_red(), description="")
        emb.set_thumbnail(url=ctx.guild.icon_url)
        
        for ban in bans:

            emb.add_field(name=f"{ban[1]} - {ban[1].id}", value=f"{ban[0]}", inline=False)
        
        await ctx.send(embed=emb)

    @commands.command(aliases=["clear", "clr"],help="Clear a specified number of messages")
    @commands.check_any(commands.is_owner(), commands.has_permissions(manage_messages=True))
    async def purge(self,ctx,*kwargs):

        support = get(self.client.guilds , id=629436501964619776)
        emoji = get(support.emojis, name="BlutoCheck")
        query = kwargs[0]

        if query == "-s":

            channel : discord.TextChannel = ctx.channel

            try:
                await channel.purge(limit=int(kwargs[1])+1)
            except Exception as err:
                return
            
        else:
            channel : discord.TextChannel = ctx.channel
            try:
                await channel.purge(limit=int(kwargs[0])+1)
                await ctx.send(f"{emoji} Successfully purged ``{int(kwargs[0])}`` messages",delete_after=20)
            except Exception as err:
                return
                
    @commands.command(help="Strike the BAN hammer")
    @commands.check_any(commands.is_owner(), commands.has_permissions(ban_members=True))
    async def ban(self,ctx,*kwargs):
    
        support = get(self.client.guilds , id=629436501964619776)
        emoji = get(support.emojis, name="BlutoCheck")
        emoji2 = get(support.emojis, name="BlutoX")
        reason = " ".join(kwargs[1:])

        inp = kwargs[0]

        try:
            member:discord.Member = get(ctx.guild.members, id=int(inp))
                
        except:

            if inp:
                try:
                    member = get(ctx.guild.members, name=inp)
                        
                except:
                    member = get(ctx.guild.members, display_name=inp)

            if  inp is None:
                member : discord.Member = ctx.author
            else:
                for men in ctx.message.mentions:
                    member = men

        try:

            if kwargs[1] == "-s":
                return await member.ban()
        except:
            pass
            
        
        try:
            msg : discord.Message = await member.send(f"You've been Banned in {ctx.guild} for: ``{reason}``")
        except:
            print("could not dm member")

        try:
            ban = await member.ban(reason=reason)
        except Exception as err:
            try:
                await msg.delete()
            except:
                pass
            emb = discord.Embed(title = f"{emoji2} Member could not be banned!" )
            emb.add_field(name="Error",value=f"``{err}``")
            await ctx.send(embed=emb)
            return

        try:
            banembed = discord.Embed(title=f"{emoji} Member banned succesfully", description=f"{member.mention}")
            banembed.add_field(name="Reason",value=reason,inline=True)
            banembed.add_field(name="ID",value=member.id,inline=True)
            banembed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=banembed)
        except Exception as err: 
            reason = "None"
            banembed = discord.Embed(title=f"{emoji} Member banned succesfully", description=f"{member.mention}")
            banembed.add_field(name="Reason",value=reason,inline=True)
            banembed.add_field(name="ID",value=member.id,inline=True)
            banembed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=banembed)

    @commands.command(help="Kick a specified user from the server")
    @commands.check_any(commands.is_owner(), commands.has_permissions(kick_members=True))
    async def kick(self,ctx,*kwargs):

        support = get(self.client.guilds , id=629436501964619776)
        emoji = get(support.emojis, name="BlutoCheck")
        emoji2 = get(support.emojis, name="BlutoX")
        reason = " ".join(kwargs[1:])
        
        inp = kwargs[0]

        try:
            member:discord.Member = get(ctx.guild.members, id=int(inp))
                
        except:

            if inp:
                try:
                    member = get(ctx.guild.members, name=inp)
                        
                except:
                    member = get(ctx.guild.members, display_name=inp)

            if  inp is None:
                member : discord.Member = ctx.author
            else:
                for men in ctx.message.mentions:
                    member = men

        try:
            if kwargs[1] == "-s":
                await member.kick()
                return
        except:
            pass
            
        
        try:
            msg : discord.Message = await member.send(f"You've been kicked in {ctx.guild} for: ``{reason}``")
        except:
            print("could not dm member")

        try:
            kick = await member.kick(reason=reason)
        except Exception as err:
            try:
                await msg.delete()
            except:
                pass
            emb = discord.Embed(title = f"{emoji2} Member could not be kicked!" )
            emb.add_field(name="Error",value=f"``{err}``")
            await ctx.send(embed=emb)
            return

        try:
            kickembed = discord.Embed(title=f"{emoji} Member kicked succesfully", description=f"{member.mention}")
            kickembed.add_field(name="Reason",value=reason,inline=True)
            kickembed.add_field(name="ID",value=member.id,inline=True)
            kickembed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=kickembed)
        except Exception as err: 
            reason = "None"
            kickembed = discord.Embed(title=f"{emoji} Member kicked succesfully", description=f"{member.mention}")
            kickembed.add_field(name="Reason",value=reason,inline=True)
            kickembed.add_field(name="ID",value=member.id,inline=True)
            kickembed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=kickembed)

    @commands.command(help="Mute a member in text chat")
    @commands.check_any(commands.is_owner(), commands.has_permissions(manage_roles=True))
    async def mute(self,ctx,*kwargs):

        support = get(self.client.guilds , id=629436501964619776)
        emoji = get(support.emojis, name="BlutoCheck")
        emoji2 = get(support.emojis, name="BlutoX")
        reason = " ".join(kwargs[1:])
        muterole = await blutapi.getMuteRole(ctx.guild)
        
        inp = kwargs[0]

        try:
            member:discord.Member = get(ctx.guild.members, id=int(inp))
                
        except:
            pass

            if inp:
                try:
                    member = get(ctx.guild.members, name=inp)
                        
                except:
                    member = get(ctx.guild.members, display_name=inp)

            if  inp is None:
                member : discord.Member = ctx.author
            else:
                for men in ctx.message.mentions:
                    member = men

        if member is None:

            await ctx.send(f"{emoji2} User not found!")
            return

        try:

            if kwargs[1] == "-s":
                await member.add_roles(muterole,reason=reason)
                return
        except:
            pass

        try:
            msg : discord.Message = await member.send(f"You've been muted in {ctx.guild} for: ``{reason}``")
        except:
            print("could not dm member")

        try:
            mute = await member.add_roles(muterole,reason=reason)
        except Exception as err:
            try:
                await msg.delete()
            except:
                pass
            emb = discord.Embed(title = f"{emoji2} Member could not be muted!" )
            emb.add_field(name="Error",value=f"``{err}``")
            await ctx.send(embed=emb)
            return


        try:
            muteembed = discord.Embed(title=f"{emoji} Member muted succesfully", description=f"{member.mention}")
            muteembed.add_field(name="Reason",value=reason,inline=True)
            muteembed.add_field(name="ID",value=member.id,inline=True)
            muteembed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=muteembed)
        except Exception as err: 
            reason = "None"
            muteembed = discord.Embed(title=f"{emoji} Member muted succesfully", description=f"{member.mention}")
            muteembed.add_field(name="Reason",value=reason,inline=True)
            muteembed.add_field(name="ID",value=member.id,inline=True)
            muteembed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=muteembed)

    @commands.command(aliases=["umute"], help="Unmute a member in text chat")
    @commands.check_any(commands.is_owner(), commands.has_permissions(manage_roles=True))
    async def unmute(self,ctx,*kwargs):

        support = get(self.client.guilds , id=629436501964619776)
        emoji = get(support.emojis, name="BlutoCheck")
        emoji2 = get(support.emojis, name="BlutoX")
        reason = " ".join(kwargs[1:])
        muterole = await blutapi.getMuteRole(ctx.guild)
        
        inp = kwargs[0]

        try:
            member:discord.Member = get(ctx.guild.members, id=int(inp))
                
        except:
            pass

            if inp:
                try:
                    member = get(ctx.guild.members, name=inp)
                        
                except:
                    member = get(ctx.guild.members, display_name=inp)

            if  inp is None:
                member : discord.Member = ctx.author
            else:
                for men in ctx.message.mentions:
                    member = men

        if member is None:

            await ctx.send(f"{emoji2} User not found!")
            return

        try:

            if kwargs[1] == "-s":
                await member.remove_roles(muterole,reason=reason)
                return
        except:
            pass

        try:
            msg : discord.Message = await member.send(f"You've been unmuted in {ctx.guild} for: ``{reason}``")
        except:
            print("could not dm member")

        try:
            mute = await member.remove_roles(muterole,reason=reason)
        except Exception as err:
            try:
                await msg.delete()
            except:
                pass
            emb = discord.Embed(title = f"{emoji2} Member could not be unmuted!" )
            emb.add_field(name="Error",value=f"``{err}``")
            await ctx.send(embed=emb)
            return


        try:
            muteembed = discord.Embed(title=f"{emoji} Member unmuted succesfully", description=f"{member.mention}")
            muteembed.add_field(name="Reason",value=reason,inline=True)
            muteembed.add_field(name="ID",value=member.id,inline=True)
            muteembed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=muteembed)
        except Exception as err: 
            reason = "None"
            muteembed = discord.Embed(title=f"{emoji} Member unmuted succesfully", description=f"{member.mention}")
            muteembed.add_field(name="Reason",value=reason,inline=True)
            muteembed.add_field(name="ID",value=member.id,inline=True)
            muteembed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=muteembed)

    @commands.command(aliases=["uban"], help="Un-strike the BAN hammer")
    @commands.check_any(commands.is_owner(), commands.has_permissions(ban_members=True))
    async def unban(self,ctx,*kwargs):

        support = get(self.client.guilds , id=629436501964619776)
        emoji = get(support.emojis, name="BlutoCheck")
        emoji2 = get(support.emojis, name="BlutoX")
        reason = " ".join(kwargs[1:])

        inp = kwargs[0]


        bans = []
        banlist = await ctx.guild.bans()

        for ban in banlist:

            bans.append(ban[1])
        

        try:
            member:discord.Member = get(bans, id=int(inp))
                
        except:
            await ctx.send(f"{emoji2} Could not find the user! only use the ID")
            return

        for user in bans:

            if (member.name, member.discriminator) == (user.name, user.discriminator):

                unbanuser : discord.Member = user

        try:

            if kwargs[1] == "-s":
                return await ctx.guild.unban(unbanuser,reason=reason)
        except:
            pass
            
        
        try:
            msg : discord.Message = await member.send(f"You've been Unbanned in {ctx.guild} for: ``{reason}``")
        except:
            print("could not dm member")

        try:
            ban = await ctx.guild.unban(unbanuser,reason=reason)
        except Exception as err:
            try:
                await msg.delete()
            except:
                pass
            emb = discord.Embed(title = f"{emoji2} Member could not be Unbanned!" )
            emb.add_field(name="Error",value=f"``{err}``")
            await ctx.send(embed=emb)
            return

        try:
            banembed = discord.Embed(title=f"{emoji} Member Unbanned succesfully", description=f"{member.mention}")
            banembed.add_field(name="Reason",value=reason,inline=True)
            banembed.add_field(name="ID",value=member.id,inline=True)
            banembed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=banembed)
        except Exception as err: 
            reason = "None"
            banembed = discord.Embed(title=f"{emoji} Member Unbanned succesfully", description=f"{member.mention}")
            banembed.add_field(name="Reason",value=reason,inline=True)
            banembed.add_field(name="ID",value=member.id,inline=True)
            banembed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=banembed)        
    
    @banlist.error
    async def banlist_error(self,ctx,error):
        if isinstance(error,commands.CheckAnyFailure):
            support = get(self.client.guilds , id=629436501964619776)
            emoji = get(support.emojis, name="BlutoCheck")
            emoji2 = get(support.emojis, name="BlutoX")

            await ctx.send(f"{emoji2} You don't have permission to use this command!")       

    @unban.error
    async def unban_handler(self,ctx,error):
        if isinstance(error,commands.CheckAnyFailure):
            support = get(self.client.guilds , id=629436501964619776)
            emoji = get(support.emojis, name="BlutoCheck")
            emoji2 = get(support.emojis, name="BlutoX")

            await ctx.send(f"{emoji2} You don't have permission to use this command!")

    @ban.error
    async def ban_handler(self,ctx,error):
        if isinstance(error,commands.CheckAnyFailure):
            support = get(self.client.guilds , id=629436501964619776)
            emoji = get(support.emojis, name="BlutoCheck")
            emoji2 = get(support.emojis, name="BlutoX")

            await ctx.send(f"{emoji2} You don't have permission to use this command!")

    @mute.error
    async def mute_handler(self,ctx,error):
        if isinstance(error,commands.CheckAnyFailure):
            support = get(self.client.guilds , id=629436501964619776)
            emoji = get(support.emojis, name="BlutoCheck")
            emoji2 = get(support.emojis, name="BlutoX")

            await ctx.send(f"{emoji2} You don't have permission to use this command!")

    @unmute.error
    async def unmute_handler(self,ctx,error):
        if isinstance(error,commands.CheckAnyFailure):
            support = get(self.client.guilds , id=629436501964619776)
            emoji = get(support.emojis, name="BlutoCheck")
            emoji2 = get(support.emojis, name="BlutoX")

            await ctx.send(f"{emoji2} You don't have permission to use this command!")

    @purge.error
    async def purge_handler(self,ctx,error):
        if isinstance(error,commands.CheckAnyFailure):
            support = get(self.client.guilds , id=629436501964619776)
            emoji = get(support.emojis, name="BlutoCheck")
            emoji2 = get(support.emojis, name="BlutoX")

            await ctx.send(f"{emoji2} You don't have permission to use this command!")

    @kick.error
    async def kick_handler(self,ctx,error):
        if isinstance(error,commands.CheckAnyFailure):
            support = get(self.client.guilds , id=629436501964619776)
            emoji = get(support.emojis, name="BlutoCheck")
            emoji2 = get(support.emojis, name="BlutoX")

            await ctx.send(f"{emoji2} Insuffecient perms")
            
def setup(client):
    client.add_cog(moderation(client))
