import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json,asyncio,datetime,pytz,random

from cmds.casino import *
from cmds.create import *  
from core.helper import createEmbed,getDiscordTime,getTotalSeconds


Inside_Bet = ["one","two","three","four","five","six"] #內圈0~36
Outside_Bet = ["big","small","red","black","odd","even","row1","row2","row3","1st","2nd","3rd"] #外圍
stats_list = ["count","win","win_money","lose_money"] #紀錄狀況


def get_Bet_num(msg:str): #將字串轉換為數字
    print(f"msg:{msg}")
    bet_list = []
    msglist = msg.split(",")
    for i in msglist:
        try:
            num = int(i)
            if 0 <= num <= 36 and num not in bet_list:
                bet_list.append(num) 
        except:
            pass
    bet_list.sort() 
    return bet_list    


#在頻道中建立的遊戲模板
def getRoulettemode(channel_id):
    gamedata = {
    "channel_id": str(channel_id),
    "message_id": "",
    "WaitEmbed": "",
    "GameState": False,
    "Duration": "5m",
    "AutoCreate": False,
    "CreateTime": "1h",
    "EndTime": None,
    "Num": None,
    "TotalAmount": 0,
    "GamePlayer": {}
    }
    return gamedata


class Roulette(Cog_Extension):

    @commands.command()   # gamble_coin 賭幣 <:material_gamble_coin:967714841013915649>
    async def Steat_Roulette_Embed(self,gamedata_channel,gamedata_casino):
        limit = gamedata_casino["limit"]
        emoji = "<:material_gamble_coin:967714841013915649>"
        if limit == None:
            limit_msg = f"無上限"
        else:
            limit_msg = f"{limit}"

        content = f"**內圍投注:** 0~36間的數字任意選擇，獲勝機率較低但有較高的賠率。\n\n"
        content += f"**數字注:** 1~6 個數字 ( 1賠 35/17/11/8/6/5 )\n下注格式 : `~Bet <數字> <賭金>` (多數字用 ',' 隔開)\n\n"
        content += f"**週邊投注:** 有更好的獲勝機率，但是它們的賠率較低"
        content += "**直行注:** 押注在12個數位組成的直行 ( 1賠2 )\n下注格式 : `~Bet <Row1/Row2/Row3> <賭金>`\n\n"
        content += "**數位組合區:** 押注在12個數位組成的直行 ( 1賠2 )\n下注格式 : `~Bet <1st/2nd/3rd> <賭金>`\n\n"
        content += "**大小數位注:** 大「19-36」小「1-18」( 1賠1 )\n下注格式 : `~Bet <Big/Smail> <賭金>`\n\n"
        content += "**紅黑顏色注:** 押注在紅色或黑色區 ( 1賠1 )\n下注格式 : `~Bet <Red/Black> <賭金>`\n\n"
        content += "**單雙數字注:** 押注在單數或雙數 ( 1賠1 )\n下注格式 : `~Bet <Odd/Even> <賭金>`\n\n"
        footerContent = f"「一券在手，希望無窮」"
        # embed=discord.Embed(title="輪盤遊戲", color=0xffae00,description=description,timestamp = datetime.datetime.now())
        # embed.set_thumbnail(url="https://imgur.com/iZDJz1s.jpg")
        # embed.add_field(name="**內圍投注**", value=f"獲勝機率較低但有較高的賠率。", inline=False)
        # embed.add_field(name="**數字注:** 1~6 個數字 ( 1賠 35/17/11/8/6/5 )", value=f"下注格式 : `~Bet <數字> <賭金>` (多數字用 ',' 隔開) ", inline=False)
        # embed.add_field(name="**週邊投注**", value=f"有更好的獲勝機率，但是它們的賠率較低 。",inline=False)
        # embed.add_field(name="**直行注:** 押注在12個數位組成的直行 ( 1賠2 )", value=f"下注格式 : `~Bet <Row1/Row2/Row3> <賭金>` ",inline=False)
        # embed.add_field(name="**數位組合區:** 押注在某12個數位組合區 ( 1賠2 )",value=f"下注格式 : `~Bet <1st/2nd/3rd> <賭金>` ",inline=False)
        # embed.add_field(name="**大小數位注:** 大「19-36」小「1-18」( 1賠1 )", value=f"下注格式 : `~Bet <Big/Smail> <賭金>` ",inline=False)
        # embed.add_field(name="**紅黑顏色注:** 押注在紅色或黑色區 ( 1賠1 )", value=f"下注格式 : `~Bet <Red/Black> <賭金>` ",inline=False)
        # embed.add_field(name="**單雙數字注:** 押注在單數或雙數 ( 1賠1 )", value=f"下注格式 : `~Bet <Odd/Even> <賭金>` ",inline=False)
        embed = createEmbed("輪盤遊戲",content,footerContent=footerContent,color=0xffae00)
        embed.add_field(name="**下注限制** ", value=f"{emoji} **{limit_msg}**",inline=True)
        embed.add_field(name="**參與玩家** ", value=f":busts_in_silhouette: **{len(gamedata_channel['GamePlayer'])}**",inline=True)
        embed.add_field(name="**總下注金額** ", value=f"{emoji} **{gamedata_channel['TotalAmount']:,}**",inline=True)
        embed.add_field(name="**結束時間**",value=f"<a:shiny_check_yellow:980501686516846592> **{getDiscordTime(gamedata_channel['EndTime'], 1)} {getDiscordTime(gamedata_channel['EndTime'], 2)}**",inline=True)
        embed.set_image(url="https://imgur.com/dd8MoKP.png")
        # embed.set_image(url="attachment://image.png") 
        # file = discord.File("pngwing.png", filename="image.png")
        # await ctx.send(file=file,embed=embed)
        # return embed,file
        return embed

    @commands.command()   # gamble_coin 賭幣 <:material_gamble_coin:967714841013915649>
    async def Roulette_Num_random(self,gamedata_channel,guildsID):
        if gamedata_channel['Num'] == None:
            gamedata_channel['Num'] = random.randint(0,36)
            channel_id = gamedata_channel['channel_id']
            gamelist = self.bot.db.queryItem("guilds","guildsID",guildsID,f"roulette")
            index = [i["channel_id"] for i in gamelist].index(channel_id)
            self.bot.db.updateOneValue("guilds","name","AzurTactics",f"roulette.{index}",gamedata_channel)



    @commands.command()   # gamble_coin 賭幣 <:material_gamble_coin:967714841013915649>
    async def testt(self,ctx):
        Guild = ctx.guild
        gamedata_casino,gamedata_channel,index = await Casino.get_channel_game(self,ctx) #取得遊戲資料
        print("呼叫")
        await self.Roulette_Num_random(gamedata_channel,str(Guild.id))


    @commands.command()   # gamble_coin 賭幣 <:material_gamble_coin:967714841013915649>
    async def End_Roulette(self,gamedata_channel,guildsID):
        gamedata_casino = self.bot.db.queryItem("casino","name","AzurTactics","roulette")
        limit = gamedata_casino["limit"]
        emoji = "<:material_gamble_coin:967714841013915649>"
        for name in gamedata_channel["GamePlayer"]:
            for userdata in gamedata_channel["GamePlayer"][name]:
                pass
        winlist = []
        loselist = []




    @commands.command()   # gamble_coin 賭幣 <:material_gamble_coin:967714841013915649>
    async def tec(self,ctx):
        embed=discord.Embed(title=f"***{ctx.author.name}***", url="")
        embed.set_thumbnail(url="https://scontent.ftpe8-3.fna.fbcdn.net/v/t39.30808-6/280657696_3086554951609127_8229215256338723452_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=730e14&_nc_ohc=KEpkzPvL2QwAX-dtzC3&tn=ac7LSwrMJBtzbNkh&_nc_ht=scontent.ftpe8-3.fna&oh=00_AT-hHz-1EGnwNpJ-yvIzhjtLIyrC48MFTqYqz25srhIzaQ&oe=628D6F35")
        embed.set_author(name="智能手錶式投影屏SB703", icon_url="https://scontent.ftpe8-4.fna.fbcdn.net/v/t39.30808-6/280567728_3086555784942377_7260846321047164045_n.jpg?stp=dst-jpg_p843x403&_nc_cat=102&ccb=1-7&_nc_sid=730e14&_nc_ohc=etwrD6S0D3MAX8Y9Ear&_nc_ht=scontent.ftpe8-4.fna&oh=00_AT9MQRShZG3fsqn_aAWdw-ic9TJiM7nClG16Sl0sJ6EMhA&oe=628C5244")
        embed.add_field(name="關於我", value="總熟練度：\n稱號：\n成就總數：\n", inline=False)
        embed.add_field(name="您的身體素質", value="防禦DEF：\n敏捷DEX：\n智慧INT：\n幸運值：", inline=False)
        embed.add_field(name="您的社交圈", value="派系所屬：\n派系加成：\n領地所屬：\n領地身分：", inline=False)
        embed.set_footer(text="輸入ai.smartband(sb)開啟個人狀態頁．前好難傳團隊發行")
        file = discord.File("pngwing.png", filename="image.png")
        # embed.set_image(url="https://scontent.ftpe8-3.fna.fbcdn.net/v/t39.30808-6/280657696_3086554951609127_8229215256338723452_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=730e14&_nc_ohc=KEpkzPvL2QwAX-dtzC3&tn=ac7LSwrMJBtzbNkh&_nc_ht=scontent.ftpe8-3.fna&oh=00_AT-hHz-1EGnwNpJ-yvIzhjtLIyrC48MFTqYqz25srhIzaQ&oe=628D6F35")
        await ctx.send(embed=embed)

    @commands.command()  #在使用者資料中創建輪盤數據
    async def add_member_roulette(self,ctx,member_id):
  
        if not self.bot.db.checkInLst("members",[ {"member_id":"384581532251062274"}, {"start": {"$in": ["roulette"]}} ]):
            data = {}
            for bet in Inside_Bet+Outside_Bet:
                data[bet]={}
                for stats in stats_list:
                    data[bet][stats] = 0
            self.bot.db.insertListValue("members","member_id","384581532251062274",f"stats.roulette",data)


    @commands.command() 
    async def Bet(self,ctx,bet:str,gamble_coin:int):
        await ctx.message.delete()
        bet = bet.lower()
        member_id = str(ctx.author.id)
        user_gamble_coin = await Casino.get_member_gamble_coin(self,ctx) #取得玩家資料
        gamedata_casino,gamedata_channel,index = await Casino.get_channel_game(self,ctx) #取得遊戲資料
        limit = gamedata_casino["limit"]
        emoji = "<:material_gamble_coin:967714841013915649>"

        #下注時間需小於結算時間
        # if getTotalSeconds("now") >  gamedata_channel["EndTime"]: 
        #     await ctx.send(f"** 輪盤結算中暫不支持下注**", delete_after=5.0)
        #     return 

        #玩家擁有賭幣要大於下注金額
        if user_gamble_coin >= gamble_coin: 
            if limit != None :
                bet_old = 0
                if member_id in gamedata_channel["GamePlayer"]:
                    #計算外圍
                    for i in Outside_Bet:
                        if i in gamedata_channel["GamePlayer"][member_id]:
                            bet_old += gamedata_channel["GamePlayer"][member_id][i]["gamble_coin"]
                    #計算內圈
                    for i in Inside_Bet:
                        if i in gamedata_channel["GamePlayer"][member_id]:
                            for j in gamedata_channel["GamePlayer"][member_id][i]:
                               bet_old += j["gamble_coin"]

                if bet_old+gamble_coin > limit: #下注總和超出限制
                    content = f"**累計下注: {emoji} {bet_old}**\n"
                    content += f"**本次下注: {emoji} {gamble_coin}**\n"
                    content += f"**賭局限制: {emoji} {limit}**\n"
                    embed = createEmbed("超出限制 ",content,color=0xff0000)
                    # await ctx.send(f"{content} ", delete_after=6.0)
                    await ctx.send(embed=embed, delete_after=8.0)
                    
                    return 
             
            #取得玩家下注資料
            Dict = {}
            Type = None
            betlist = []
            if member_id in gamedata_channel["GamePlayer"]:
                Dict = gamedata_channel["GamePlayer"][member_id]

            #判斷是否外圍 "big","small","red","black","odd","even","row1","row2","row3","1st","2nd","3rd"
            if bet in Outside_Bet:
                Type = bet
                betlist = gamedata_casino['bet'][Type]['Num']
                if bet not in Dict: #下注不存在時新增欄位
                    Dict[bet] = {"Num":betlist,"gamble_coin":gamble_coin}
                else: #已存在時增加賭金
                    Dict[bet]["gamble_coin"] += gamble_coin
                                        
            #判斷是否為數字注 "one","two","three","four","five","six"         
            else: 
                betlist = get_Bet_num(bet)
                if len(betlist) == 1 :
                    Type = "one"
                if len(betlist) == 2 :
                    Type = "two"
                if len(betlist) == 3 :
                    Type = "three"
                if len(betlist) == 4 :
                    Type = "four"
                if len(betlist) == 5 :
                    Type = "five"
                if len(betlist) == 6 :
                    Type = "six"

                if Type not in Dict:
                    Dict[Type] = [{"Num":betlist,"gamble_coin":gamble_coin}]
                else:
                    print("已存在")
                    for i in range(len(Dict[Type])):
                        if Dict[Type][i]["Num"] == betlist:
                            print("相同Type 相同數字")
                            Dict[Type][i]["gamble_coin"] += gamble_coin
                            break
                        elif i == len(Dict[Type])-1:
                            print("相同Type 不同數字")
                            Dict[Type].append({"Num":betlist,"gamble_coin":gamble_coin})

            #若有成功下注發送訊息
            if Type != None:
                Guild = ctx.guild
                print("更新MongoDB")
                # Dict["TotalAmount"] += gamble_coin
                self.bot.db.updateManyValueMode("$inc", "guilds", f"roulette.{index}.TotalAmount", gamble_coin, "guildsID",str(Guild.id))
                self.bot.db.updateOneValue("guilds","name","AzurTactics",f"roulette.{index}.GamePlayer.{member_id}",Dict)
                self.bot.db.updateManyValueMode("$inc", "members", "gamble_coin", -gamble_coin, "member_id", member_id)
                msg = ""
                for i,j in enumerate(betlist):
                    msg += str(j)
                    if i < len(betlist)-1:
                        msg += "/"

                # content = f"**下注類型: {gamedata_casino['bet'][Type]['Name']} 1賠{gamedata_casino['bet'][Type]['odds']} **\n"
                content = ""
                content += f"**獲勝條件 : {msg}** \n"
                content += f"**本次下注 : {emoji} {gamble_coin:,}**\n"
                content += f"**預計收益 : {emoji} {gamble_coin+gamble_coin*gamedata_casino['bet'][Type]['odds']:,}**\n"
                footerContent = f"{ctx.author.name} 下注成功，祝您幸運中獎"
                embed = createEmbed(f"{gamedata_casino['bet'][Type]['Name']} 1 賠 {gamedata_casino['bet'][Type]['odds']}",content,footerContent=footerContent,color=0x00ff62)

                await ctx.send(embed=embed) # , delete_after=10.0
            else:
                content = f"**下注格式錯誤，無法判斷**\n"
                embed = createEmbed(f"下注失敗",content,color=0xff0000)
                await ctx.send(embed=embed, delete_after=8.0)
                
                 
            #提示使用者訊息
            embed = await self.Steat_Roulette_Embed(gamedata_channel,gamedata_casino)
            try: #找舊訊息並替換
                message = await ctx.channel.fetch_message(int(gamedata_channel["message_id"])) 
                await message.edit(embed=embed) #,file=file
            except: #找不到就訊系時重新發送
           
                msg = await ctx.send(embed=embed)
                gamedata_channel["message_id"] = msg.id
                self.bot.db.updateOneValue("guilds","guildsID",str(Guild.id),f"{gamedata_casino['game']}.{index}",gamedata_channel)
        else:
            content = f"**下注金額高於有擁資產**\n"
            content += f"**持有賭幣: {emoji} {user_gamble_coin}**\n"
            content += f"**本次下注: {emoji} {gamble_coin}**\n"
            embed = createEmbed(f"賭幣不足",content,color=0xff0000)
            # embed.add_field(name="**持有賭幣:**", value=f"{emoji} {user_gamble_coin}", inline=False)
            await ctx.send(embed=embed, delete_after=8.0)
            # await ctx.send(f"{ctx.author.mention} 下注金額高於有擁資產，下注失敗\n**當前資產 : **{user_gamble_coin}{emoji}\n**下注金額 : ** {gamble_coin}{emoji}", delete_after=8.0)


    @commands.command()  #設定開獎號碼 
    async def RandomNum(self,ctx,num=None):
        pass

async def setup(bot):
    await bot.add_cog(Roulette(bot))