import imp
from discord.ext import commands
from datetime import datetime, timedelta
import time
import discord
import asyncio


def getTwTimeNow():
    # now_timestamp = time.time()
    # offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    # print(datetime.utcnow())
    # print(offset)
    # return datetime.utcnow()
    return datetime.now() # - offset

def createEmbed(title:str, description:str, footerContent="", titleIconUrl="", thumbnailUrl="", imgUrl="", fields={}, inline=False, color=0xFCA12B):
    embed = discord.Embed(description=description, timestamp=getTwTimeNow(), color=color) 
    if len(titleIconUrl) > 0: embed.set_author(name=title, icon_url = titleIconUrl) 
    else: embed.set_author(name=title)
    if len(thumbnailUrl) > 0: embed.set_thumbnail(url=thumbnailUrl)
    if len(imgUrl) > 0: embed.set_image(url=imgUrl)
    for name in fields:
        embed.add_field(name=name, value=fields[name], inline=inline)
    footerContent = footerContent if len(footerContent) > 0 else "♚尼腓工作室"
    embed.set_footer(text=footerContent, icon_url="https://imgur.com/ehNt7VL.jpg")
    return embed

def getTotalSeconds(duration:str): #duration: 0s,1m, 2d, 3w, 4h, now
    orig_date = datetime(1970, 1, 1)
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    current_date = getTwTimeNow() - offset
    # current_datetime = datetime(current_date.year, current_date.month, current_date.day)
    # total_seconds = int((current_datetime - orig_date).total_seconds())
    date_format_str = "%Y-%m-%d %H:%M:%S.%f"
    current_datetime = datetime.strptime(str(current_date), date_format_str)
    total_seconds = int((current_datetime - orig_date).total_seconds())

    if duration == None or duration == "now":
        return total_seconds
    
    timeFormat = duration[-1]
    num = int(duration[:-1])
    delta = -1
    if timeFormat == "d": 
        delta = timedelta(days=num)
    elif timeFormat == "w": 
        delta = timedelta(weeks=num)
    elif timeFormat == "m": 
        delta = timedelta(minutes=num)
    elif timeFormat == "s": 
        delta = timedelta(seconds=num)
    elif timeFormat == "h": 
        delta = timedelta(hours=num)
    else: return -1
    
    total_seconds += delta.total_seconds()
    return int(total_seconds)

def getDiscordTime(total_seconds, type = 1):
    # total_seconds -= 8*60*60
    if type == 1: return f"<t:{total_seconds}:f>" # Ex. 2021年8月13日 08:00
    else: return f"<t:{total_seconds}:R>" # Ex. 2 天內

async def warnAndDel(ctx, warnMsg, num:int):
    await ctx.channel.purge(limit=num-1) # delete cmd
    await ctx.send(warnMsg, delete_after=5.0)

