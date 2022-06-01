from trace import Trace
import discord
from discord.ext import commands
from pandas import read_pickle
from core.classes import Cog_Extension
import json,asyncio,datetime,pytz,random
from MongoDB import *
from cmds.admin import *
from cmds.create import * 
from cmds.roulette import *
from core.modules import *
from core.helper import *
# with open("setting.json","r",encoding="utf8") as jfile:
#     jdata = json.load(jfile)
# MData = MongoDB().queryItem("game", "name", "AzurTactics")

# 賭場遊戲列表
games = ["roulette"]
class Casino(Cog_Extension):
    # def __init__(self, *args,**kwargs):
    #     super().__init__(*args,**kwargs) # 重讀取父類別
    #     async def Auto_Check_Game():
    #         await self.bot.wait_until_ready()
    #         while not self.bot.is_closed(): # 若機器人啟動中
    #             current_time_seconds = getTotalSeconds("now")
    #             guilds_datas = self.bot.db.queryTable("guilds")
    #             for guilds_data in guilds_datas: #伺服器
    #                 guildsID = guilds_data['guildsID']
    #                 for game in games: #遊戲名稱
    #                     for index in range(len(guilds_data[games])): #遊戲頻道
    #                         gamedata_channel = guilds_data[game][index]
    #                         if gamedata_channel["GameState"] == True and gamedata_channel['EndTime'] < current_time_seconds:
    #                             if game == "roulette":
    #                                 await Roulette.End_Roulette(self,gamedata_channel,guildsID)


                # await asyncio.sleep(10) #10秒檢查一次
    @commands.command() 
    async def get_member_gamble_coin(self,ctx): #回傳玩家賭幣數量
        await Create.add_member_user(self,ctx)
        member_id = str(ctx.author.id)
        gamble_coin = self.bot.db.queryItem("members","member_id",member_id,"gamble_coin")
        return gamble_coin
    
    @commands.command()   
    async def get_channel_game(self,ctx): # 取得頻道中遊戲
        Guild = ctx.guild 
        #取得賭場中遊戲名稱
        casino = self.bot.db.queryItem("casino", "name", "AzurTactics") #賭場資料
        Guilddata = self.bot.db.queryItem("guilds","guildsID",str(Guild.id)) #伺服器資料
        index=-1
        for num_,i in enumerate(games):
            for j in range(len(Guilddata[i])):
                if Guilddata[i][j]["channel_id"] == str(ctx.channel.id):
                    gamedata_casino = casino[i]
                    gamedata_channel = Guilddata[i][j]
                    index = j
                    return gamedata_casino,gamedata_channel,index           
        return None
        
    @commands.command() 
    async def showdata(self,ctx,member:discord.Member=None): #Show出資產
        if member == None:
            member_id = str(ctx.author.id)
            mention = ctx.author.mention
        else:
            member_id = str(member.id)
            mention = member.mention
        await Create.add_member_user(self,ctx,member_id)
        memberdata = self.bot.db.queryItem("members","member_id",member_id)
        await ctx.send(f"{mention} 資產 : {memberdata['gamble_coin']} <:material_gamble_coin:967714841013915649>")


    @commands.command() 
    async def systemgive(self,ctx,member:discord.Member,gamble_coin:int): #管理者修改(新增/減少)賭幣
        admin = await Admin.check_admin(self,ctx)
        if admin : 
            member_id = str(member.id)
            mention = member.mention
            self.bot.db.checkInLst("members",[ {"member_id": member_id}])
            if gamble_coin >0:
                msg = "給予"
            else:
                msg = "扣除"
            await self.add_member_user(ctx,member_id)
            olddata = self.bot.db.queryItem("members","member_id",member_id,"gamble_coin")
            self.bot.db.updateOneValue("members","member_id",member_id,"gamble_coin",olddata+gamble_coin)
            await ctx.send(f"成功{msg} {mention} {gamble_coin} <:material_gamble_coin:967714841013915649>")
        
    @commands.command()   
    async def setgame(self,ctx,GameName): # 設定遊戲頻道
        admin = await Admin.check_admin(self,ctx)
        if admin :
            Guild = ctx.guild        
            GameName = GameName.lower()
            casino = self.bot.db.queryItem("casino", "name", "AzurTactics")
            
            if GameName in casino:

                mode = 1
                content = ""
                roulette = self.bot.db.queryItem("guilds","guildsID",str(Guild.id),"roulette")
                if len(roulette) == 0 or str(ctx.channel.id) not in [i["channel_id"] for i in roulette]:
                    mode = 1
                    print("z")
                    gamedata = getRoulettemode(ctx.channel.id)
                    print("x")
                    self.bot.db.insertListValue("guilds", "guildsID", str(Guild.id), f"roulette",gamedata)
                else:
                    mode = 2
                    index = [i["channel_id"] for i in roulette].index(str(ctx.channel.id))
                    self.bot.db.deleteListValue("guilds", "guildsID", str(Guild.id), f"roulette",roulette[index])

                modeResult = "加入" if mode == 1 else "刪除"
                modeEmoji = "✅" if mode == 1 else "❌"
                content += f"{ctx.author.mention} 成功 {ctx.channel.mention} {modeResult}{casino[GameName]['cn']} {modeEmoji}\n"
                await ctx.send(content)
            
    @commands.command() #在已經有遊戲的平到中設定遊戲
    async def set(self,ctx,*msg):
        admin = await Admin.check_admin(self,ctx)
        if admin :
            gamedata_casino,gamedata_channel,index = await self.get_channel_game(ctx)
            Guild = ctx.guild 
            if index >-1:
                count = 0
                timecount = 0
                timelist= ["Duration","CreateTime"]
                
                while count < len (msg):
                    newmsg = msg[count].lower()

                    if newmsg == "playtime":
                        count +=1
                        timecount = 0
                        newmsg = msg[count].lower()

                    if newmsg == "createtime":
                        count +=1
                        timecount = 1
                        newmsg = msg[count].lower()

                    if newmsg == "false":
                        gamedata_channel["AutoCreate"] = False
                        count+=1
                    elif newmsg == "true":
                        gamedata_channel["AutoCreate"] = True
                        count+=1
                    elif newmsg[-1] in ["s","m","h","d","w"]:
                        gamedata_channel[timelist[timecount]] = newmsg
                        count+=1
                        if timecount==0:
                            timecount +=1
                        else:
                            timecount=0
                    else:
                        gamedata_channel[timelist[timecount]] = newmsg+"m"
                        count+=1
                        if timecount==0:
                            timecount +=1
                        else:
                            timecount=0
                self.bot.db.updateOneValue("guilds","guildsID",str(Guild.id),f"roulette.{index}",gamedata_channel)
                embed=discord.Embed(title=f" 設定成功", color=0x24ffda,timestamp = datetime.datetime.now())
                embed.add_field(name=f"設定頻道:", value=f"{ctx.message.channel.mention}", inline=False)
                embed.add_field(name=f"更改遊戲:", value=f"{gamedata_casino['cn']}", inline=True)
                embed.add_field(name=f"遊戲時間:", value=f"{gamedata_channel['Duration']}", inline=True)
                embed.add_field(name="\u200b", value="\u200b", inline=True)
                embed.add_field(name=f"自動創建:", value=f"{gamedata_channel['AutoCreate']}", inline=True)
                embed.add_field(name=f"時間間隔:", value=f"{gamedata_channel['CreateTime']}", inline=True)
                embed.add_field(name="\u200b", value="\u200b", inline=True)
                msg = await ctx.send(embed=embed)    
            else:
                await ctx.send(f"{ctx.channel.mention} 並沒有加入遊戲 ")     

    @commands.command()   
    async def create(self,ctx,time=""): # 創建遊戲房間
        # member_id = ctx.author.id
        # await self.add_member_user(member_id)
        admin = await Admin.check_admin(self,ctx)
        if admin :
            gamedata_casino,gamedata_channel,index = await self.get_channel_game(ctx)
            Guild = ctx.guild 
            if index > -1: #有找到遊戲
                if gamedata_channel["GameState"] == False:
                    gamedata_channel["GameState"] = True
                    if time=="":
                        print("創造遊戲 沒寫時間，預設10分鐘")
                        EndTime = getTotalSeconds("10m")
                    else:
                        EndTime = getTotalSeconds(time)
                    gamedata_channel["EndTime"] = EndTime
                    if gamedata_casino['game'] == "roulette":
                        print("呼叫emnb")
                        embed = await Roulette.Steat_Roulette_Embed(self,gamedata_channel,gamedata_casino)
                        print("aaa")
                        msg = await ctx.send(embed=embed)
                        gamedata_channel["message_id"] = msg.id
                        self.bot.db.updateOneValue("guilds","guildsID",str(Guild.id),f"{gamedata_casino['game']}.{index}",gamedata_channel)
                else:
                    await ctx.send(f"遊戲進行中，無法重複建造 ❌", delete_after=5.0)
                    # await warnAndDel(ctx,f"{ctx.author.mention} 遊戲進行中，無法重複建造 ❌")
            else:
                print("沒有設定遊戲")
                # await warnAndDel(ctx,f"{ctx.author.mention} 當前頻到中沒有設定遊戲 ❌")
                await ctx.send(f"當前頻到中沒有設定遊戲")

        
async def setup(bot):
    await bot.add_cog(Casino(bot))

