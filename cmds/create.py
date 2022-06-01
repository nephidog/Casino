import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json,asyncio,datetime,pytz,random
from cmds.admin import * 
from core.modules import *


class Create(Cog_Extension):
    
    @commands.command()
    async def createguild(self,ctx): #檢查是否有權限
        Guild = ctx.guild
        if self.bot.db.checkInLst("guilds", [ {"guildsID": Guild.id} ]):
            await ctx.send(f"{Guild} 已經存在")
        else:
            GuildData = getNewGuildData(Guild.id)
            self.bot.db.insertOneItem("guilds",GuildData)
            await ctx.send(f"{Guild} 成功新建")

    @commands.command() 
    async def add_member_user(self,ctx,member_id=None): #增加遊戲使用者
        if member_id == None:
            member_id = ctx.author.id
        if not self.bot.db.checkInLst("members",[ {"member_id": str(member_id)}]):
            memberdata = getNewMemberData(member_id)
            self.bot.db.insertOneItem("members",memberdata)

async def setup(bot):
    await bot.add_cog(Create(bot))