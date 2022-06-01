from MongoDB import *
import json

from MongoDB import *
# with open("setting.json","r",encoding="utf8") as jfile:
#     jdata = json.load(jfile)
#查資料
# MData = MongoDB().queryItem("admin", "name", "AzurTactics")
# #
# adminlist = [MongoDB().queryItem("admin", "name", "AzurTactics","root")]
# print(adminlist)
# data = {"member_id":0,"gamble_coin":0}
# MongoDB().insertListValue("members","name","AzurTactics",f"users",data)
# MongoDB().updateOneValue("members","name","AzurTactics",f"users.{0}.gamble_coin",100)
#插入資料
# MongoDB().insertOneItem("casino",{"Game":[]})
# gamble_coin 賭幣名稱
# data = {
#     "game":"roulette",
#     "limit":None,
#     "count":0,
#     "income":0,
#     "expenses":0
# }

# print(MongoDB().checkInLst("members", [ {"name": "AzurTactics"}, {f"users.{0}.{'member_id'}": {"$in": [384581532251062274]}} ]))
# MongoDB().insertOneItem("admin","name","AzurTactics",f"users",)
# MongoDB().insertManyItem("admin",[{"guildsID":774858902964797461}])
# MongoDB().updateOneValue("admin","name","AzurTactics",f"roldlist",[])
# MongoDB().updateOneValue("admin","name","AzurTactics",f"zxc",774858902964797461)
# MongoDB().insertListValue("admin", "name", f"AzurTactics", f"roldlist",11)
# MongoDB().insertListValue("admin", "guildsID", f"{774858902964797461}", f"roldlist",11)
# print(MongoDB().queryItem("admin","guildsID",774858902964797461,"roldlist"))

# print(MongoDB().checkInLst("casion", [ {"name": "AzurTactics"}, {f"games": {"$in": [f"{game.roulette"]}} ]))
# print(MongoDB().checkInLst("admin", [ {"name": "AzurTactics"}, {f"roldlist": {"$in": [774866377419784224]}} ]))
# print(MongoDB().checkInLst("guilds", [ {"guildsID": 774858902964797461} ])) #, {"admin_list": {"$in": [250508597182595070]}}
Inside_Bet = ["one","two","three","four","five","six"]
Outside_Bet = ["big","small","red","black","odd","even","row1","row2","row3","1st","2nd","3rd"]
stats_list = ["count","win","win_money","lose_money"]
data = {}

casino = MongoDB().queryItem("casino", "name", "AzurTactics")
gamelist = [i["game"] for i in casino["games"]]
index ,gamename = -1,""
Guilddata = MongoDB().queryItem("guilds","guildsID",str(774858902964797461))
print("開始迴圈")
for i in gamelist:
    for j in range(len(Guilddata[i])):
        print("準備比對")
        if Guilddata[i][j]["channel_id"] == str(966670200516788235):
            gamename,index =  i,j 
            gamedata = Guilddata[i][j]
            break
print(gamename,index)