import urllib
from urllib.request import Request
import aiohttp
import discord
import requests
import openpyxl
import asyncio
import datetime
from bs4 import BeautifulSoup
from captcha.image import ImageCaptcha
import bs4
import psutil
import random

client = discord.Client()
token = 'NzU3MTg1MzYyNTEzODg3MjMz.X2ct0g.F6LLNlpvHZUiBNzCVHYP_1TgFkc'

@client.event
async def on_ready():
    print('=====================================')
    print("ready")
    print(client.user.id)
    print(client.user.name)
    print('=====================================')
    now=datetime.datetime.now()

@client.event
async def my_background_task():
    await client.wait_until_ready()
    while not client.is_closed():
        game = discord.Game(f"?도움말 를 이용해서 명령어를 알아보자")
        await client.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(5)
        game = discord.Game(f'서버:{len(client.guilds)}개')
        await client.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(5)
        game = discord.Game(f'유저:{len(client.users)}명')
        await client.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(5)
        game = discord.Game(f'봇의 핑: {round(client.latency * 1000)}ms')
        await client.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(5)
client.loop.create_task(my_background_task())

@client.event
async def on_guild_join(guild):
    guildname = {guild.name}
    webhook = 'https://ptb.discordapp.com/api/webhooks/763737852961226762/LL4g2iV5-ZlnxK5nK06rnVM055izW2VUH-5xLGDNFWb_r_opvXBAaJGeYzpCXL1seLln'
    requests.post(webhook, {'content':f'{guild.name}({guild.id})에 봇 초대됨. owner = {guild.owner}({guild.owner.id})<a:yes:707786803414958100>\n서버수:{len(client.guilds)}개'})
    embed = discord.Embed(title=f"봇 초대됨", color=0xfc00f4, timestamp=message.created_at)

@client.event
async def on_guild_remove(guild):
    webhook = 'https://ptb.discordapp.com/api/webhooks/763737852961226762/LL4g2iV5-ZlnxK5nK06rnVM055izW2VUH-5xLGDNFWb_r_opvXBAaJGeYzpCXL1seLln'
    requests.post(webhook, {'content':f'{guild.name}({guild.id})에 봇 추방됨. owner = {guild.owner}({guild.owner.id})<a:no:761038850046033980>\n서버수:{len(client.guilds)}개'})

@client.event
async def on_message(message):
    global roles
    if message.content.startswith("?DM"):
        author = message.guild.get_member(int(message.content.split(' ')[1][3:21]))
        msg = message.content[26:]
        embed = discord.Embed(color=0xfc00f4,
                              title='DM이 도착했어요!',
                              description=msg,
                              timestamp=message.created_at)
        embed.set_footer(text=f"{message.author} 님이 DM",
                         icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
        await author.send(embed=embed)
        embed = discord.Embed(color=0xfc00f4,
                              title='<a:yes:761038848947126323>DM 전송됨<a:yes:761038848947126323>',
                              description=msg,
                              timestamp=message.created_at)
        embed.set_footer(text=f"{message.author} 님이 DM 요청",
                         icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
        await message.channel.send(embed=embed)

    elif message.content.startswith(f"?추방"):
        if message.guild.get_member(client.user.id).guild_permissions.kick_members == True:
            if message.author.guild_permissions.kick_members:
                try:
                    try:
                        user = message.guild.get_member(int(message.content.split('<@')[1].split('>')[0]))
                    except:
                        user = message.guild.get_member(int(message.content.split('<@!')[1].split('>')[0]))
                    if user.id == message.author.id:
                        embed = discord.Embed(title=f"추방", color=0xfc00f4, timestamp=message.created_at)
                        embed.add_field(name="<a:no:761038850046033980>에러<a:no:761038850046033980>", value=("루피봇 에러발생\n에러 내용이 <@556300258716418050>님에게 전송됨\n에러내용 : Unable to kick"), inline=False)
                        embed.set_footer(text=f"{message.author} 님이 요청", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
                        await message.channel.send(embed=embed)
                    else:
                        try:
                            reason = message.content.split('&')[1]
                        except:
                            reason = "사유 없음"
                        await message.guild.kick(user, reason=f"{reason}")
                        try:
                            embed = discord.Embed(title=f"<a:yes:761038848947126323>{user} 추방<a:yes:761038848947126323>", color=discord.Colour.red(),
                                                  timestamp=message.created_at)
                            embed.add_field(name=" 처리자", value=f"<@{message.author.id}> ({message.author})",
                                            inline=False)
                            embed.add_field(name=" 유저", value=f'<@{user.id}> ({user})', inline=False)
                            embed.set_footer(text=f"{message.author}처리자", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
                            await message.channel.send(embed=embed)
                            embed = discord.Embed(title=f"추방", color=0xfc00f4, timestamp=message.created_at)
                            await user.send(f'> {user}님 {message.guild.name}서버에 __추방__ 되었습니다')
                        except:
                            pass
                except IndexError:
                    embed = discord.Embed(title=f"추방", color=0xfc00f4, timestamp=message.created_at)
                    embed.add_field(name="<a:no:761038850046033980>에러<a:no:761038850046033980>", value=("루피봇 에러발생\n에러 내용이 <@556300258716418050>님에게 전송됨\n에러내용 : Format is wrong"), inline=False)
                    embed.set_footer(text=f"{message.author} 님이 요청", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
                    await message.channel.send(embed=embed)
                except:
                    embed = discord.Embed(title=f"추방", color=0xfc00f4, timestamp=message.created_at)
                    embed.add_field(name="<a:no:761038850046033980>에러<a:no:761038850046033980>", value=("루피봇 에러발생\n에러 내용이 <@556300258716418050>님에게 전송됨\n에러내용 : The person to be deported has too high privileges or does not exist on this server."), inline=False)
                    embed.set_footer(text=f"{message.author} 님이 요청", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
                    await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(title=f"추방", color=0xfc00f4, timestamp=message.created_at)
                embed.add_field(name="<a:no:761038850046033980>에러<a:no:761038850046033980>", value=("루피봇 에러발생\n에러 내용이 <@556300258716418050>님에게 전송됨\n에러내용 : You have no permission."), inline=False)
                embed.set_footer(text=f"{message.author} 님이 요청", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
                await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title=f"추방", color=0xfc00f4, timestamp=message.created_at)
            embed.add_field(name="<a:no:761038850046033980>에러<a:no:761038850046033980>", value=("루피봇 에러발생\n에러 내용이 <@556300258716418050>님에게 전송됨\n에러내용 : Bot has no permission."), inline=False)
            embed.set_footer(text=f"{message.author} 님이 요청", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
            await message.channel.send(embed=embed)

    elif message.content.startswith(f"?차단"):
        if message.guild.get_member(client.user.id).guild_permissions.ban_members == True:
            if message.author.guild_permissions.ban_members:
                try:
                    try:
                        user = int(message.content.split('<@')[1].split('>')[0])
                    except:
                        user = int(message.content.split('<@!')[1].split('>')[0])
                    print(user)
                    if user == message.author.id:
                        embed = discord.Embed(title=f"차단", color=0xfc00f4, timestamp=message.created_at)
                        embed.add_field(name="<a:no:761038850046033980>에러<a:no:761038850046033980>", value=("Unable to ban."), inline=False)
                        embed.set_footer(text=f"{message.author} 님이 요청", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
                        await message.channel.send(embed=embed)
                    else:
                        try:
                            reason = message.content.split('&')[1]
                        except:
                            reason = "사유 없음"
                            un = await client.fetch_user(user)
                            await message.guild.ban(await client.fetch_user(user), reason=f"{reason}")
                        embed = discord.Embed(title=f"<a:yes:761038848947126323>{un} 차단<a:yes:761038848947126323>", color=discord.Colour.red(),
                                              timestamp=message.created_at)
                        embed.add_field(name=" 처리자", value=f"<@{message.author.id}> ({message.author})", inline=False)
                        embed.add_field(name=" 유저", value=f'<@{un.id}> ({un})', inline=False)
                        embed.set_footer(text=f"{message.author}처리자", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
                        await message.channel.send(embed=embed)
                        embed = discord.Embed(title=f"차단", color=0xfc00f4, timestamp=message.created_at)
                        await un.send(f'> {un}님 {message.guild.name}서버에 __차단__ 되었습니다')
                except IndexError:
                    embed = discord.Embed(title=f"차단", color=0xfc00f4, timestamp=message.created_at)
                    embed.add_field(name="<a:no:761038850046033980>에러<a:no:761038850046033980>", value=("루피봇 에러발생\n에러 내용이 <@556300258716418050>님에게 전송됨\n에러내용 : Format is wrong."), inline=False)
                    embed.set_footer(text=f"{message.author} 님이 요청", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
                    await message.channel.send(embed=embed)
                except Exception as ex:
                    embed = discord.Embed(title=f"차단", color=0xfc00f4, timestamp=message.created_at)
                    embed.add_field(name="<a:no:761038850046033980>에러<a:no:761038850046033980>", value=("루피봇 에러발생\n에러 내용이 <@556300258716418050>님에게 전송됨\n에러내용 : The person to be deported has too high privileges or does not exist on this server."), inline=False)
                    embed.set_footer(text=f"{message.author} 님이 요청", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
                    await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(title=f"차단", color=0xfc00f4, timestamp=message.created_at)
                embed.add_field(name="<a:no:761038850046033980>에러<a:no:761038850046033980>", value=("루피봇 에러발생\n에러 내용이 <@556300258716418050>님에게 전송됨\n에러내용 : You have no permission."), inline=False)
                embed.set_footer(text=f"{message.author} 님이 요청", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
                await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title=f"차단", color=0xfc00f4, timestamp=message.created_at)
            embed.add_field(name="<a:no:761038850046033980>에러<a:no:761038850046033980>", value=("루피봇 에러발생\n에러 내용이 <@556300258716418050>님에게 전송됨\n에러내용 : Bot has no permission."), inline=False)
            embed.set_footer(text=f"{message.author} 님이 요청", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
            await message.channel.send(embed=embed)

    elif message.content.startswith(f"?정보"):
        if str(message.content[5:]) == '':
            user = message.author
            date = datetime.datetime.utcfromtimestamp(((int(user.id) >> 22) + 1420070400000) / 1000)
            status_dict: dict = {discord.Status.online: '<:status_online:760798459543683102> 온라인',
                                 discord.Status.offline: '<:status_offline:760798578301599744>  오프라인',
                                 discord.Status.idle: "<:status_idle:760798459497414676> 자리비움",
                                 discord.Status.do_not_disturb: "<:status_DND:760798459497676810> 방해금지"}
            user_status = status_dict[user.status]
            if not len(message.author.roles) == 1:
                roles = [role for role in user.roles]
                embed = discord.Embed(colour=user.color, timestamp=message.created_at)
            else:
                embed = discord.Embed(colour=0xfc00f4, timestamp=message.created_at, title=f"유저정보 - {user}")
            embed.set_author(name=f"유저정보 - {user}")
            embed.set_thumbnail(url=user.avatar_url)
            embed.set_footer(text=f"{message.author} 님이 요청", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
            embed.add_field(name="아이디", value=user.id, inline=False)
            embed.add_field(name="닉네임", value=user.display_name, inline=False)
            embed.add_field(name="계정 생성 시간", value=user.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                            inline=False)
            embed.add_field(name="가입 시간", value=user.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
            embed.add_field(name=f"가진 역할들 ({len(roles)})", value=" ".join([role.mention for role in roles]),
                            inline=False)
            embed.add_field(name="가장 높은 역할", value=user.top_role.mention, inline=False)
            embed.add_field(name="상태", value=f'{user_status}', inline=False)
            embed.add_field(name="봇", value=user.bot, inline=False)
            if 'Custom Status' in str(user.activity):
                embed.add_field(name='하는 게임& 상태메시지', value=user.activity.state, inline=False)
            else:
                embed.add_field(name='하는 게임& 상태메시지', value=user.activity, inline=False)
            await message.channel.send(embed=embed)
        else:
            try:
                user = message.guild.get_member(int(message.content.split('<@!')[1].split('>')[0]))
                if user.bot == False:
                    date = datetime.datetime.utcfromtimestamp(((int(user.id) >> 22) + 1420070400000) / 1000)
                    status_dict: dict = {discord.Status.online: '<:status_online:760798459543683102> 온라인',
                                         discord.Status.offline: '<:status_offline:760798578301599744>  오프라인',
                                         discord.Status.idle: "<:status_idle:760798459497414676> 자리비움",
                                         discord.Status.do_not_disturb: "<:status_DND:760798459497676810> 방해금지"}
                    user_status = status_dict[user.status]
                    if not len(user.roles) == 1:
                        roles = [role for role in user.roles]
                        embed = discord.Embed(colour=0xfc00f4, timestamp=message.created_at, title=f"유저정보 - {user}")
                    else:
                        embed = discord.Embed(colour=user.color, timestamp=message.created_at, title=f"유저정보 - {user}")
                    embed.set_author(name=f"유저정보 - {user}")
                    embed.set_thumbnail(url=user.avatar_url)
                    embed.set_footer(text=f"{message.author} 님이 요청", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
                    embed.add_field(name="아이디", value=user.id, inline=False)
                    embed.add_field(name="닉네임", value=user.display_name, inline=False)
                    embed.add_field(name="계정 생성 시간", value=user.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                                    inline=False)
                    embed.add_field(name="가입 시간", value=user.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                                    inline=False)
                    embed.add_field(name=f"가진 역할들 ({len(roles)})", value=" ".join([role.mention for role in roles]),
                                    inline=False)
                    embed.add_field(name="가장 높은 역할", value=user.top_role.mention, inline=False)
                    embed.add_field(name="상태", value=f'{user_status}', inline=False)
                    embed.add_field(name="봇", value=user.bot, inline=False)
                    if 'Custom Status' in str(user.activity):
                        embed.add_field(name='하는 게임& 상태메시지', value=user.activity.state, inline=False)
                    else:
                        embed.add_field(name='하는 게임& 상태메시지', value=user.activity, inline=False)
                    await message.channel.send(embed=embed)
                else:
                    date = datetime.datetime.utcfromtimestamp(((int(user.id) >> 22) + 1420070400000) / 1000)
                    status_dict: dict = {discord.Status.online: '<:status_online:760798459543683102> 온라인',
                                         discord.Status.offline: '<:status_offline:760798578301599744>  오프라인',
                                         discord.Status.idle: "<:status_idle:760798459497414676> 자리비움",
                                         discord.Status.do_not_disturb: "<:status_DND:760798459497676810>  방해금지"}
                    user_status = status_dict[user.status]
                    if not len(user.roles) == 1:
                        roles = [role for role in user.roles]
                        embed = discord.Embed(colour=user.color, timestamp=message.created_at,
                                              title=f"봇정보<:bot:761965280556744744> - {user}")
                    else:
                        embed = discord.Embed(colour=0xfc00f4, timestamp=message.created_at,
                                              title=f"봇정보<:bot:761965280556744744> - {user}")
                    embed.set_author(name=f"유저정보 - {user}")
                    embed.set_thumbnail(url=user.avatar_url)
                    embed.set_footer(text=f"{message.author} 님이 요청", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
                    embed.add_field(name="아이디", value=user.id, inline=False)
                    embed.add_field(name="닉네임", value=user.display_name, inline=False)
                    embed.add_field(name="계정 생성 시간", value=user.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                                    inline=False)
                    embed.add_field(name="가입 시간", value=user.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                                    inline=False)
                    embed.add_field(name=f"가진 역할들 ({len(roles)})", value=" ".join([role.mention for role in roles]),
                                    inline=False)
                    embed.add_field(name="가장 높은 역할", value=user.top_role.mention, inline=False)
                    embed.add_field(name="상태", value=f'{user_status}', inline=False)
                    embed.add_field(name="봇", value=user.bot, inline=False)
                    if 'Custom Status' in str(message.author.activity):
                        embed.add_field(name='하는 게임& 상태메시지', value=user.activity.state, inline=False)
                    else:
                        embed.add_field(name='하는 게임& 상태메시지', value=user.activity, inline=False)
                    embed.add_field(name="봇 초대링크 (관리자 권한)",
                                    value=f"[초대하기](https://discordapp.com/oauth2/authorize?client_id={user.id}&scope=bot&permissions=8)",
                                    inline=False)
                    await message.channel.send(embed=embed)
            except:
                user = message.guild.get_member(int(message.content.split('<@')[1].split('>')[0]))
                if user.bot == False:
                    date = datetime.datetime.utcfromtimestamp(((int(user.id) >> 22) + 1420070400000) / 1000)
                    status_dict: dict = {discord.Status.online: '<:status_online:760798459543683102> 온라인',
                                         discord.Status.offline: '<:status_offline:760798578301599744>  오프라인',
                                         discord.Status.idle: "<:status_idle:760798459497414676> 자리비움",
                                         discord.Status.do_not_disturb: "<:status_DND:760798459497676810>  방해금지"}
                    user_status = status_dict[user.status]
                    if not len(user.roles) == 1:
                        roles = [role for role in user.roles]
                        embed = discord.Embed(colour=0xfc00f4, timestamp=message.created_at, title=f"유저정보 - {user}")
                    else:
                        embed = discord.Embed(colour=user.color, timestamp=message.created_at, title=f"유저정보 - {user}")
                    embed.set_author(name=f"유저정보 - {user}")
                    embed.set_thumbnail(url=user.avatar_url)
                    embed.set_footer(text=f"{message.author} 님이 요청 ", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
                    embed.add_field(name="아이디", value=user.id, inline=False)
                    embed.add_field(name="닉네임", value=user.display_name, inline=False)
                    embed.add_field(name="계정 생성 시간", value=user.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                                    inline=False)
                    embed.add_field(name="가입 시간", value=user.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                                    inline=False)
                    embed.add_field(name=f"가진 역할들 ({len(roles)})", value=" ".join([role.mention for role in roles]),
                                    inline=False)
                    embed.add_field(name="가장 높은 역할", value=user.top_role.mention, inline=False)
                    embed.add_field(name="상태", value=f'{user_status}', inline=False)
                    embed.add_field(name="봇", value=user.bot, inline=False)
                    if 'Custom Status' in str(user.activity):
                        embed.add_field(name='하는 게임& 상태메시지', value=user.activity.state, inline=False)
                    else:
                        embed.add_field(name='하는 게임& 상태메시지', value=user.activity, inline=False)
                    await message.channel.send(embed=embed)
                else:
                    date = datetime.datetime.utcfromtimestamp(((int(user.id) >> 22) + 1420070400000) / 1000)
                    status_dict: dict = {discord.Status.online: '<:status_online:760798459543683102> 온라인',
                                         discord.Status.offline: '<:status_offline:760798578301599744>  오프라인',
                                         discord.Status.idle: "<:status_idle:760798459497414676> 자리비움",
                                         discord.Status.do_not_disturb: "<:status_DND:760798459497676810>  방해금지"}
                    user_status = status_dict[user.status]
                    if not len(user.roles) == 1:
                        roles = [role for role in user.roles]
                        embed = discord.Embed(colour=user.color, timestamp=message.created_at,
                                              title=f"봇정보<:bot:761965280556744744> - {user}")
                    else:
                        embed = discord.Embed(colour=0xfc00f4, timestamp=message.created_at,
                                              title=f"봇정보<:bot:761965280556744744> - {user}")
                    embed.set_author(name=f"유저정보 - {user}")
                    embed.set_thumbnail(url=user.avatar_url)
                    embed.set_footer(text=f"{message.author} 님이 요청", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
                    embed.add_field(name="아이디", value=user.id, inline=False)
                    embed.add_field(name="닉네임", value=user.display_name, inline=False)
                    embed.add_field(name="계정 생성 시간", value=user.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                                    inline=False)
                    embed.add_field(name="가입 시간", value=user.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                                    inline=False)
                    embed.add_field(name=f"가진 역할들 ({len(roles)})", value=" ".join([role.mention for role in roles]),
                                    inline=False)
                    embed.add_field(name="가장 높은 역할", value=user.top_role.mention, inline=False)
                    embed.add_field(name="상태", value=f'{user_status}', inline=False)
                    embed.add_field(name="봇", value=user.bot, inline=False)
                    if 'Custom Status' in str(user.activity):
                        embed.add_field(name='하는 게임& 상태메시지', value=user.activity.state, inline=False)
                    else:
                        embed.add_field(name='하는 게임& 상태메시지', value=user.activity, inline=False)
                    embed.add_field(name="봇 초대링크 (관리자 권한)",
                                    value=f"[초대하기](https://discordapp.com/oauth2/authorize?client_id={user.id}&scope=bot&permissions=8)",
                                    inline=False)
                    await message.channel.send(embed=embed)

    elif message.content.startswith("?채널정보"):
        if len(message.channel_mentions) == 0:
            channel = message.channel
        else:
            channel = message.channel_mentions[0]
        name = channel.name
        cid = channel.id
        topic = channel.topic
        if topic == "" or topic == None:
            topic = "없음"
        pos = str(channel.position + 1) + "번"
        ctype = str(channel.type)
        created = str(channel.created_at)
        embed = discord.Embed(title=f"{name} 채널정보", color=0xfc00f4, timestamp=message.created_at)
        embed.add_field(name="이름", value=name, inline=False)
        embed.add_field(name="채널 ID", value=cid, inline=False)
        embed.add_field(name="주제", value=topic, inline=False)
        embed.add_field(name="채널 순서", value=pos, inline=False)
        embed.add_field(name="채널 종류", value=ctype, inline=False)
        embed.add_field(name="채널 생성일", value=created, inline=False)
        embed.set_footer(text=f"{message.author}님이 요청", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
        await message.channel.send(embed=embed)

    elif message.content == "?미세먼지":
        channel = message.channel
        url = "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80"
        res = requests.get(url)
        html = res.text
        bs = bs4.BeautifulSoup(html, 'html.parser')
        mise = {}
        city = ['서울', '경기', '인천', '강원', '세종', '충북', '충남', '대전', '경북', '경남', '대구', '울산', '부산', '전북', '전남', '광주', '제주']
        num = 0
        for x in city:
            mise[x] = bs.select(
                "#main_pack > div.content_search.section._atmospheric_environment > div > div.contents03_sub > div > div > div.main_box > div.detail_box > div.tb_scroll > table > tbody > tr > td > span")[
                num].text
            num += 3
        level = {}
        for x in city:
            if int(mise[x]) <= 30:
                level[x] = "좋음"
            elif int(mise[x]) >= 31 and int(mise[x]) <= 80:
                level[x] = "보통"
            elif int(mise[x]) >= 81 and int(mise[x]) <= 150:
                level[x] = "**나쁨**"
            elif int(mise[x]) >= 151:
                level[x] = "**매우나쁨**"
            else:
                level[x] = "오류"
        time = bs.select(
            "#main_pack > div.content_search.section._atmospheric_environment > div > div.contents03_sub > div > div > div.info_box > div.guide_bx > div > span.update > em")[
            0].text
        embed = discord.Embed(title=f"PM10 미세먼지\n{time} 기준", color=0xfc00f4, timestamp=message.created_at)
        for i in city:
            embed.add_field(name="**" + i + "**", value=(mise[i] + "㎍/m³ | " + level[i]))
        embed.set_footer(text=f"{message.author} 님이 요청", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
        await message.channel.send(embed=embed)

    elif message.content == "?초미세먼지":
        channel = message.channel
        url = "https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&query=%EC%B4%88%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80"
        res = requests.get(url)
        html = res.text
        bs = bs4.BeautifulSoup(html, 'html.parser')
        mise = {}
        city = ['서울', '경기', '인천', '강원', '세종', '충북', '충남', '대전', '경북', '경남', '대구', '울산', '부산', '전북', '전남', '광주', '제주']
        num = 0
        for x in city:
            mise[x] = bs.select(
                "#main_pack > div.content_search.section._atmospheric_environment > div > div.contents03_sub > div > div > div.main_box > div.detail_box > div.tb_scroll > table > tbody > tr > td > span")[
                num].text
            num += 3
        level = {}
        for x in city:
            if int(mise[x]) <= 15:
                level[x] = "좋음"
            elif int(mise[x]) >= 16 and int(mise[x]) <= 35:
                level[x] = "보통"
            elif int(mise[x]) >= 36 and int(mise[x]) <= 75:
                level[x] = "**나쁨**"
            elif int(mise[x]) >= 76:
                level[x] = "**매우나쁨**"
            else:
                level[x] = "오류"
        time = bs.select(
            "#main_pack > div.content_search.section._atmospheric_environment > div > div.contents03_sub > div > div > div.info_box > div.guide_bx > div > span.update > em")[
            0].text
        embed = discord.Embed(title=f"PM2.5 초미세먼지\n{time} 기준", color=0xfc00f4, timestamp=message.created_at)
        for i in city:
            embed.add_field(name="**" + i + "**", value=(mise[i] + "㎍/m³ | " + level[i]))
        embed.set_footer(text=f"{message.author} 님이 요청", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
        await message.channel.send(embed=embed)

    elif message.content == '?재난문자':
        """최근에 발생한 재난문자를 보여줍니다"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    'http://m.safekorea.go.kr/idsiSFK/neo/ext/json/disasterDataList/disasterDataList.json') as r:
                data = await r.json()

        embed = discord.Embed(
            title="📢 재난문자",
            description="최근에 발송된 재난문자 5개를 보여줍니다!",
            color=0xfc00f4
        )

        for i in data[:5]:
            embed.add_field(name=i["SJ"], value=i["CONT"], inline=False)
        await message.channel.send(embed=embed)

    elif message.content == '?코로나':
        hdr = {'User-Agent': 'Mozilla/5.0'}
        url = 'http://ncov.mohw.go.kr/'
        req = Request(url, headers=hdr)
        html = urllib.request.urlopen(req)
        bsObj = bs4.BeautifulSoup(html, "html.parser")
        corona = bsObj.find('div', {'class': 'mainlive_container'})
        corona2 = corona.find('div', {'class': 'container'})
        corona3 = corona2.find('div', {'class': 'liveboard_layout'})
        corona4 = corona3.find('div', {'class': 'live_left'})
        corona4 = corona3.find('div', {'class': 'liveNum'})
        corona5 = corona4.find('ul', {'class': 'liveNum'})
        corona6 = corona5.find_all('li')
        coronacount = corona6[0]
        coronacount2 = coronacount.find('span', {'class': 'num'})
        coronacount3 = coronacount2.text.strip()
        coronacountp = corona6[0]
        coronacount2p = coronacountp.find('span', {'class': 'before'})
        coronacount3p = coronacount2p.text.strip()
        coronafin = corona6[1]
        coronafin2 = coronafin.find('span', {'class': 'num'})
        coronafin3 = coronafin2.text.strip()
        coronafinp = corona6[1]
        coronafin2p = coronafinp.find('span', {'class': 'before'})
        coronafin3p = coronafin2p.text.strip()
        coronadoc = corona6[2]
        coronadoc2 = coronadoc.find('span', {'class': 'num'})
        coronadoc3 = coronadoc2.text.strip()
        coronadocp = corona6[2]
        coronadoc2p = coronadocp.find('span', {'class': 'before'})
        coronadoc3p = coronadoc2p.text.strip()
        coronarip = corona6[3]
        coronarip1 = coronarip.find('span', {'class': 'num'})
        coronarip2 = coronarip1.text.strip()
        coronaripp = corona6[3]
        coronarip1p = coronaripp.find('span', {'class': 'before'})
        coronarip2p = coronarip1p.text.strip()
        embed = discord.Embed(title='코로나 바이러스 Covid-19', colour=discord.Colour.red())
        embed.set_thumbnail(
            url="https://i.pinimg.com/236x/2f/1d/5b/2f1d5b73d3db23c6bc72c3e46b6ca03a.jpg")
        embed.set_footer(text=f"{message.author} 님이 요청", icon_url=message.author.avatar_url)
        embed.add_field(name='확진된환자', value=coronacount3 + '명', inline=False)
        embed.add_field(name='완치', value=coronafin3 + '명', inline=False)
        embed.add_field(name='치료중', value=coronadoc3 + '명', inline=False)
        embed.add_field(name='사망자', value=coronarip2 + '명', inline=False)
        embed.add_field(name='**----------------------------------**\n**----------------------------------**', value='**전일대비 현황**',
                        inline=False)
        embed.add_field(name='확진환자(전일대비)', value=coronacount3p + '명', inline=False)
        embed.add_field(name='완치(전일대비)', value=coronafin3p + '명', inline=False)
        embed.add_field(name='치료중(전일대비)', value=coronadoc3p + '명', inline=False)
        embed.add_field(name='사망자(전일대비)', value=coronarip2p + '명', inline=False)
        await message.channel.send(embed=embed)

    elif message.content == '?야구':
        url = "https://sports.news.naver.com/kbaseball/record/index.nhn"
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
        result = soup.find("tbody", id="regularTeamRecordList_table")
        result2 = result.find_all("span") + result.find_all("strong")
        s = ""
        a = 0
        M = [[str(i) + "."] * 12 for i in range(11)]
        M[0] = ["\n**", " ", " |** ", "경기 ", "승 ", "패 ", "무 **|** 승률: ", " 게임차: ", " 연속: ", " 출루율: ", " 장타율: ",
                " 최근 10경기: "]
        for n in result2:
            a += 1
            if 1 <= a <= 100:
                M[(a - 1) // 10 + 1][(a - 1) % 10 + ((a - 1) % 10 > 4) + 1] = n.contents[0]
            elif a % 2 == 0:
                M[(a - 100) // 2][6] = n.contents[0]
        for i in range(10):
            for j in range(8):
                s += M[0][j]
                s += M[i + 1][j]
        embed = discord.Embed(title=f"2020 KBO리그 순위", description=s, color=0xfc00f4)
        embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/en/3/37/2020_KBO_League.png')
        await message.channel.send(embed=embed)

    elif message.content.startswith("?따라해"):
        args = message.content[5:]
        if args == "":
            embed = discord.Embed(
                title="주의", description="?봇 따라해 `할말`로 입력해주세요!\n아무 값도 받지 못했어요.",
            )
            await message.channel.send(embed=embed)
            return

        if "@everyone" in args or "@here" in args:
            embed = discord.Embed(
                title="<a:no:761038850046033980>경고<a:no:761038850046033980>",
                description="`@everyone`이나 `@here`은 다른 사용자에게 피해를 줘요..\n사용을 안할게요!",
            )
        if "씨발" in args or "새끼" in args or "애미" in args or "시발" in args or "지랄" in args or "ㅈㄹ" in args or "병신" in args:
            embed = discord.Embed(
                title="<a:no:761038850046033980>경고<a:no:761038850046033980>",
                description="욕설은 다른 사용자에게 피해를 줘요..\n사용을 안할게요!",
                )
            embed.set_footer(text=message.author, icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
            await message.channel.send(embed=embed)
        else:
            try:
                    embed = discord.Embed(color=0xfc00f4,
                                          title=args,
                                          description='',
                                          timestamp=message.created_at)
                    embed.set_footer(text=f"{message.author} 님이 따라하라고 하셨어요..!",
                                     icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
                    await message.channel.send(embed=embed)
            except:
                pass

    elif message.content == '?멜론차트':
        if __name__ == "__main__":
            RANK = 10
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
            req = requests.get('https://www.melon.com/chart/index.htm', headers=header)
            html = req.text
            parse = BeautifulSoup(html, 'html.parser')
            titles = parse.find_all("div", {"class": "ellipsis rank01"})
            songs = parse.find_all("div", {"class": "ellipsis rank02"})
            title = []
            song = []
            embed = discord.Embed(
                title="멜론차트 순위 입니다!",
                colour=0xfc00f4
            )
            for t in titles:
                title.append(t.find('a').text)
            for s in songs:
                song.append(s.find('span', {"class": "checkEllipsis"}).text)
            for i in range(RANK):
                embed.add_field(name='%3d위' % (i + 1), value='%s - %s' % (title[i], song[i]), inline=False)
            now = datetime.datetime.now()
            embed.set_footer(icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif',
                             text=f'  {str(message.author.display_name)} 님이 요청 ● {str(now.year)}년 {str(now.month)}월 {str(now.day)}일')
            embed.set_thumbnail(
                url="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSOamh5GSToy0_bMlZxsWMrJ1jgkLAjhSyKQg&usqp=CAU")
            await message.channel.send(embed=embed)

    elif message.content == '?핑':
        ping = round(client.latency * 1000)
        if ping >= 0 and ping <= 100:
            pings = "🔵아주 좋음"
            embed = discord.Embed(title=f" 퐁🏓", color=0xfc00f4, timestamp=message.created_at)
            embed.add_field(name="현재 봇 지연시간", value=f'{round(client.latency * 1000)}ms\n{pings}', inline=True)
            embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif")
            await message.channel.send(embed=embed)
        elif ping >= 101 and ping <= 200:
            pings = "🟢 좋음"
            embed = discord.Embed(title=f" 퐁🏓", color=0xfc00f4, timestamp=message.created_at)
            embed.add_field(name="현재 봇 지연시간", value=f'{round(client.latency * 1000)}ms\n{pings}', inline=True)
            embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif")
            await message.channel.send(embed=embed)
        elif ping >= 201 and ping <= 500:
            pings = "🟡 보통"
            embed = discord.Embed(title=f" 퐁🏓", color=0xfc00f4, timestamp=message.created_at)
            embed.add_field(name="현재 봇 지연시간", value=f'{round(client.latency * 1000)}ms\n{pings}', inline=True)
            embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif")
            await message.channel.send(embed=embed)
        elif ping >= 501 and ping <= 1000:
            pings = "🟠 위험"
            embed = discord.Embed(title=f" 퐁🏓", color=0xfc00f4, timestamp=message.created_at)
            embed.add_field(name="현재 봇 지연시간", value=f'{round(client.latency * 1000)}ms\n{pings}', inline=True)
            embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif")
            await message.channel.send(embed=embed)
        elif ping >= 1000:
            pings = "🔴 아주위험"
            embed = discord.Embed(title=f" 퐁🏓", color=0xfc00f4, timestamp=message.created_at)
            embed.add_field(name="현재 봇 지연시간", value=f'{round(client.latency * 1000)}ms\n{pings}', inline=True)
            embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif")
            await message.channel.send(embed=embed)

    elif message.content.startswith('?청소') or message.content.startswith('?삭제'):
        if message.author.guild_permissions.administrator or message.author.guild_permissions.manage_messages or message.author.id == 534214957110394881:
            varrr = message.content.split(' ')
            await message.channel.purge(limit=int(varrr[1]) + 1)
            now = datetime.datetime.now()
            msg = await message.channel.send(
                embed=discord.Embed(title=f'<a:yes:761038848947126323>메시지 {str(int(varrr[1]))}개 삭제 완료!<a:yes:761038848947126323>', descirption='루피가 삭제했어요!!',
                                    colour=0xfc00f4).set_footer(icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif',
                                                              text=f' | {str(message.author.display_name)} | {str(now.year)}년 {str(now.month)}월 {str(now.day)}일'))
        else:
            embed = discord.Embed(color=discord.Colour.red(),
                                  title=' <a:no:761038850046033980>사용불가<a:no:761038850046033980>  ',
                                  description='사용불가 명령어 입니다\n(서버 관리자 명령어)', timestamp=message.created_at)
            embed.set_footer(text=f"{message.author}", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
            await message.channel.send(embed=embed)



    elif message.content.startswith('?프사'):
        if str(message.content[5:]) == '':
            user = message.author
            date = datetime.datetime.utcfromtimestamp(((int(user.id) >> 22) + 1420070400000) / 1000)
            if not len(message.author.roles) == 1:
                roles = [role for role in user.roles]
                embed = discord.Embed(colour=user.color, timestamp=message.created_at)
            else:
                embed = discord.Embed(colour=0xfc00f4, timestamp=message.created_at)
            embed.add_field(name="유저정보", value=f'{user}님 프사', inline=True)
            embed.set_image(url=user.avatar_url)
            embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed)
        else:
            try:
                user = message.guild.get_member(int(message.content.split('<@!')[1].split('>')[0]))
                if user.bot == False:
                    date = datetime.datetime.utcfromtimestamp(((int(user.id) >> 22) + 1420070400000) / 1000)
                    if not len(user.roles) == 1:
                        roles = [role for role in user.roles]
                        embed = discord.Embed(colour=0xfc00f4, timestamp=message.created_at, title=f"유저정보 - {user}")
                    else:
                        embed = discord.Embed(colour=0xfc00f4, timestamp=message.created_at)
                    embed.add_field(name="유저정보", value=f'{user}님 프사', inline=True)
                    embed.set_image(url=user.avatar_url)
                    embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                    await message.channel.send(embed=embed)
                else:
                    date = datetime.datetime.utcfromtimestamp(((int(user.id) >> 22) + 1420070400000) / 1000)
                    if not len(user.roles) == 1:
                        roles = [role for role in user.roles]
                        embed = discord.Embed(colour=user.color, timestamp=message.created_at,
                                              title=f"봇정보 - {user}")
                    else:
                        embed = discord.Embed(colour=0xfc00f4, timestamp=message.created_at)
                    embed.add_field(name="봇정보", value=f'{user}님 프사', inline=True)
                    embed.set_image(url=user.avatar_url)
                    embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                    await message.channel.send(embed=embed)
            except:
                user = message.guild.get_member(int(message.content.split('<@')[1].split('>')[0]))
                if user.bot == False:
                    date = datetime.datetime.utcfromtimestamp(((int(user.id) >> 22) + 1420070400000) / 1000)
                    if not len(user.roles) == 1:
                        roles = [role for role in user.roles]
                        embed = discord.Embed(colour=0xfc00f4, timestamp=message.created_at, title=f"유저정보 - {user}")
                    else:
                        embed = discord.Embed(colour=0xfc00f4, timestamp=message.created_at)
                    embed.add_field(name="유저정보", value=f'{user}님 프사', inline=True)
                    embed.set_image(url=user.avatar_url)
                    embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                    await message.channel.send(embed=embed)
                else:
                    date = datetime.datetime.utcfromtimestamp(((int(user.id) >> 22) + 1420070400000) / 1000)
                    if not len(user.roles) == 1:
                        roles = [role for role in user.roles]
                        embed = discord.Embed(colour=user.color, timestamp=message.created_at,
                                              title=f"봇정보 - {user}")
                    else:
                        embed = discord.Embed(colour=0xfc00f4, timestamp=message.created_at)
                    embed.add_field(name="봇정보", value=f'{user}님 프사', inline=True)
                    embed.set_image(url=user.avatar_url)
                    embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                    await message.channel.send(embed=embed)

    if message.content.startswith("?패치노트"):
        embed = discord.Embed(color=0xfc00f4,
                              title=' 패치노트 ',
                              description='https://roopie.patchnote.r-e.kr\n(**패치노트는 위 링크에서 확인하세요!**)', timestamp=message.created_at)
        embed.set_footer(text=f"{message.author}", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
        await message.channel.send(embed=embed)

    if message.content.startswith("?공식디코"):
        embed = discord.Embed(color=0xfc00f4,
                              title=' 공식디코 ',
                              description='https://discord.gg/rNdcxae\n(**공식디코는 위 링크에서 들어가세요!**)', timestamp=message.created_at)
        embed.set_footer(text=f"{message.author}", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
        await message.channel.send(embed=embed)

    if message.content.startswith("?사이트"):
        embed = discord.Embed(color=0xfc00f4,
                              title=' 사이트 ',
                              description='http://roopiebot.kro.kr/\n(**사이트는 위 링크로 접속하세요!**)', timestamp=message.created_at)
        embed.set_footer(text=f"{message.author}", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
        await message.channel.send(embed=embed)

    if message.content.startswith("?초대링크"):
        embed = discord.Embed(color=0xfc00f4,
                              title=' 초대링크 ',
                              description='http://roopie.invite.r-e.kr/\n(**초대하려면 위 링크로 접속하세요!**)',
                              timestamp=message.created_at)
        embed.set_footer(text=f"{message.author}", icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
        await message.channel.send(embed=embed)

    elif message.content == '?명령어' or message.content == '?도움말' or message.content == '?도움' or message.content == '?명령' or message.content == '?명령어도움말':
        a = '**루피봇 관리 명령어** \n ?차단 @user = user를 차단한다.\n?추방 @user = user를 추방한다.\n?청소 (개수) = 개수만큼 메시지를 삭제한다.\n?DM @user text = user 의 유저한테 text를 보낸다.\n?정보 @user = 자신 또는 봇, 유저들의 정보를 알려준다.\n?채널정보 = 명령어를 적은 채널의 정보를 알려준다.\n?따라해 text = text를 따라한다.\n?프사 @user = user님의 프사를 보여준다.\n?공지 text = text 공지를 보낸다.\n\n**루피봇 개인 명령어**\n?초대링크 = 봇의 초대링크를 보낸다.\n?미세먼지 = 오늘의 미세먼지를 알려준다.\n?초미세먼지 = 오늘의 초미세먼지를 알려준다.\n?공식디코 = 루피봇 공식디코로 초대된다.\n?재난문자 = 최근의 발송된 재난문자 5개를 보여준다.\n?코로나 = 코로나 누적 확진자, 완치자, 치료자, 사망자 등등의 정보를 알려준다.\n?야구 = 2020 KBO 프로야구 순위를 알려준다. \n?핑 = 봇의 핑을 알려준다.\n?멜론차트 = 멜론 인기 노래곡을 보여준다.\n?봇상태 = 현재 봇의 상태를 알려준다.\n?마크 nick = nick 의 스킨을 보여준다. \n\n**봇 후원 문의** \n?후원 = 후원 문의 도움말이 DM으로 전송된다. '
        embed = discord.Embed(color=0xfc00f4,
                              title=' 도움말 ',
                              description=a,
                              timestamp=message.created_at)
        embed.set_footer(text=f"{message.author} 님이 요청",
                         icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
        await message.author.send(embed=embed)
        embed = discord.Embed(color=0xfc00f4,
                              title=' 도움말 ',
                              description='<a:yes:761038848947126323> 도움말이 DM으로 전송되었습니다! <a:yes:761038848947126323>',
                              timestamp=message.created_at)
        embed.set_footer(text=f"{message.author} 님이 요청",
                         icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
        await message.channel.send(embed=embed)

    if message.content.startswith("?공지"):
        announcement= message.content [4:]
        embed = discord.Embed(color=0xfc00f4,
                              title=' 공지 ',
                              description=announcement,
                              timestamp=message.created_at)
        embed.set_footer(text=f"{message.author} 님이 공지",
                         icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
        await message.channel.send(embed=embed)

    if message.content == '?봇상태':
        ping = {round(client.latency * 1000)}
        userco = {len(client.users)}
        servc = {len(client.guilds)}
        mycpu = psutil.cpu_percent()
        mb = psutil.virtual_memory().percent
        embed = discord.Embed(title=f"봇상태", color=0xfc00f4, timestamp=message.created_at)
        embed.add_field(name="서버 개수[개]", value=f'{servc} 개', inline=False)
        embed.add_field(name="서버의 모든 유저수[명]", value=f'{userco} 명', inline=False)
        embed.add_field(name="봇의 핑 [MS]", value=f'{ping} ms', inline=False)
        embed.add_field(name="사용하는 용량 [MB]", value=f'{mb} MB', inline=False)
        embed.add_field(name="사용하는 CPU [%]", value=f'{mycpu}%', inline=False)
        embed.set_footer(text=f"{message.author} 님이 요청",
                         icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
        await message.channel.send(embed=embed)

    if message.content == "?후원":
        embed = discord.Embed(color=0xfc00f4,
                              title=' 후원 ',
                              description='후원 문의 : <@556300258716418050> \n\n 이 금액으로 마스크를 기부할 예정입니다. \n 꼭 <@556300258716418050> 께 해주세요.\n다른 사람은 사기입니다!',
                              timestamp=message.created_at)
        embed.set_footer(text=f"{message.author} 님이 요청",
                         icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
        await message.author.send(embed=embed)
        embed = discord.Embed(color=0xfc00f4,
                              title=' 후원 문의 ',
                              description='<a:yes:761038848947126323> 후원 문의 도움말이 DM으로 전송되었습니다! <a:yes:761038848947126323>',
                              timestamp=message.created_at)
        embed.set_footer(text=f"{message.author} 님이 요청",
                         icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
        await message.channel.send(embed=embed)

    elif message.content.startswith(f"?캡챠"):
        author = message.author
        role = discord.utils.get(message.guild.roles, name="유저")
        lmage_captcha = ImageCaptcha()
        a = ""
        for i in range(6):
            a += str(random.randint(0, 9))
        name = str(message.author.id) + ".png"
        lmage_captcha.write(a, name)

        await message.channel.send(file=discord.File(name))

        def check(msg):
            return msg.author == message.author and msg.channel == message.channel

        try:
            msg = await client.wait_for("message", timeout=10, check=check)
        except:
            embed = discord.Embed(color=0xfc00f4,
                                  title='시간초과!',
                                  description='캡챠인증에 실패했습니다.',
                                  timestamp=message.created_at)
            embed.set_footer(text=f"{message.author} 님이 요청",
                             icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
            await message.channel.send(embed=embed)
            return

        if msg.content == a:
            embed = discord.Embed(color=0xfc00f4,
                                  title='성공!',
                                  description='캡챠인증에 성공했습니다.',
                                  timestamp=message.created_at)
            embed.set_footer(text=f"{message.author} 님이 요청",
                             icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
            await message.channel.send(embed=embed)
            try:
                role = discord.utils.get(message.guild.roles, name="유저")
                await author.add_roles(role)
            except:
                return
            await asyncio.sleep(3)
            await message.channel.purge(limit=4)
        else:
            embed = discord.Embed(color=0xfc00f4,
                                  title='실패!',
                                  description='캡챠인증에 실패했습니다.',
                                  timestamp=message.created_at)
            embed.set_footer(text=f"{message.author} 님이 요청",
                             icon_url='https://images-ext-1.discordapp.net/external/vJpRtzfm6vVqfY3YeLLtcO1U1DsxL2TG5CwgzWXInKg/%3Fitemid%3D15950157/https/media1.tenor.com/images/299cf0fe5129cecd4bb839a2dba7e07a/tenor.gif')
            await message.channel.send(embed=embed)
            await asyncio.sleep(3)
            await message.channel.purge(limit=4)

    elif message.content.startswith("?마크"):
        nickname = message.content[4:]
        channel = message.channel
        embed = discord.Embed(
            title=f'{nickname}님의 스킨',
            description=f'[[ 아바타 ]](https://minotar.net/helm/{nickname}/100.png) [[ 큐브 아바타 ]](https://minotar.net/cube/{nickname}/100.png) \n[[ 전신 ]](https://minotar.net/armor/body/{nickname}/100.png) [[ 반신 ]](https://minotar.net/armor/bust/{nickname}/100.png)\n[[ 스킨 다운로드 ]](https://minotar.net/download/{nickname})',
            color=0xfc00f4
        ).set_thumbnail(url=f"https://minotar.net/armor/bust/{nickname}/100.png")
        await message.channel.send(embed=embed)
client.run(token)