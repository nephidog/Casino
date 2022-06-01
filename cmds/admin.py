import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json,asyncio,datetime,pytz,random
# from MongoDB import *
from cmds.admin import * 
class Admin(Cog_Extension):
    
    @commands.command()
    async def check_admin(self,ctx): #檢查是否有權限
        Guild = ctx.guild
        rolelist = [] #使用者身分組ID
        for role in ctx.author.roles:
            rolelist.append(role.id)
        if ctx.author.id == self.bot.db.queryItem("bot", "name", "AzurTactics","root"):
            # await ctx.send("歡迎管理員(root)")
            return True
        elif self.bot.db.checkInLst("guilds", [ {"guildsID": Guild.id}]):
           
            if len(set(self.bot.db.queryItem("admin","guildsID",Guild.id,"roldlist")) & set(rolelist) )>0:
                # await ctx.send("歡迎管理員(role)")
                return True
            msg = await ctx.send(f"{ctx.author.mention} 無法使用此密令 ❌")
            await asyncio.sleep(3)
            await msg.delete()
            return False
        else:
            msg = await ctx.send(f"{ctx.author.mention} 無法使用此密令 ❌，伺服器{Guild.mention}沒有設置管理員，請聯繫開發者。")
            return False
 
    @commands.command()
    async def setadmin(self,ctx,roles:commands.Greedy[discord.Role]): #增加伺服器管理員(身分組)
        Guild = ctx.guild
        member_id = ctx.author.id
        if member_id == self.bot.db.queryItem("bot", "name", "AzurTactics","root"):
            content = ""
            #檢查伺服器是否存在
            for role in roles:
                mode = 1
                if mode == 1 and not self.bot.db.checkInLst("guilds", [ {"guildsID": Guild.id}, {f"roldlist": {"$in": [role.id]}} ]):
                    self.bot.db.insertListValue("guilds", "guildsID", Guild.id, f"roldlist",role.id)
                else: 
                    mode = 2
                    self.bot.db.deleteListValue("guilds", "guildsID", Guild.id, f"roldlist",role.id)
                modeResult = "加入" if mode == 1 else "刪除"
                modeEmoji = "✅" if mode == 1 else "❌"
                content += f"{ctx.author.mention} 成功將身分組 {role.mention} {modeResult}管理員 {modeEmoji}\n"
            await ctx.send(content)
        else:
            await ctx.send("您並非管理員無法使用此指令")

async def setup(bot):
    await bot.add_cog(Admin(bot))