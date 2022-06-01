import random
from MongoDB import *


Bet_List = []  #下注列表(ID、下注類型、下注金額、賠率)

Groove = ["00"] #槽 00,0 1 ~ 36 
for i in range(37):
    Groove.append(str(i))
# print(Groove)

Dict = {}

Dict["one"] = {"Name":"單個數字注（STRAIGHT UP BET）","Num":None,"odds":35}
Dict["two"] = {"Name":"兩個數位組合注（SPLIT BET）","Num":None,"odds":18}
Dict["three"] = {"Name":"三個數位組合注（STREET BET）","Num":None,"odds":11}
Dict["four"] = {"Name":"四個數位組合注（THE CORNER）","Num":None,"odds":8}
Dict["five"] = {"Name":"五個數位組合（THE TOP LINE）","Num":None,"odds":6}
Dict["six"] = {"Name":"六個數位組合（THE LINE BET）","Num":None,"odds":5}
Dict["big"] = {"Name":"大小數位注（大 HIGH）","Num":[],"odds":1}
Dict["small"] = {"Name":"大小數位注（小 LOW）","Num":[],"odds":1}
Dict["red"] = {"Name":"紅黑顏色注（紅區 RED）","Num":[1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36],"odds":1}
Dict["black"] = {"Name":"紅黑顏色注（黑區 BLACK）","Num":[2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35],"odds":1}
Dict["odd"] = {"Name":"單雙數字注（單數 ODD）","Num":[],"odds":1}
Dict["even"] = {"Name":"單雙數字注（雙數 EVEN)）","Num":[],"odds":1}
Dict["row1"] = {"Name":"第一直行注（1 COLUMN BETS）","Num":[],"odds":2}
Dict["row2"] = {"Name":"第二直行注（2 COLUMN BETS）","Num":[],"odds":2}
Dict["row3"] = {"Name":"第三直行注（3 COLUMN BETS）","Num":[],"odds":2}
Dict["1st"] = {"Name":"第一組合區（1st DOZEN）","Num":[],"odds":2}
Dict["2nd"] = {"Name":"第二組合區（2nd DOZEN）","Num":[],"odds":2}
Dict["3rd"] = {"Name":"第三組合區（3rd DOZEN）","Num":[],"odds":2}



for i in range(19,37):
    Dict["big"]["Num"].append(i)
for i in range(1,19):
    Dict["small"]["Num"].append(i)
for i in range(1,37):
    if i %2 == 1:
        Dict["odd"]["Num"].append(i)
for i in range(1,37):
    if i %2 == 0:
        Dict["even"]["Num"].append(i)
for i in range(1,37,3):
    Dict["row1"]["Num"].append(i)
for i in range(2,37,3):
    Dict["row2"]["Num"].append(i)
for i in range(3,37,3):
    Dict["row3"]["Num"].append(i)

for i in range(1,13):
    Dict["1st"]["Num"].append(i)
for i in range(13,25):
    Dict["2nd"]["Num"].append(i)
for i in range(25,37):
    Dict["3rd"]["Num"].append(i)

for i in Dict:
    print(Dict[i])
MongoDB().updateOneValue("casino","name","AzurTactics",f"games.0.bet",Dict)


def strtoint(msg:str):
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
print(strtoint("36,1,1,2,3,5"))




def Lottery(Num = None): #可指定開獎，無輸入代表隨機
    if len(Bet_List) >0:
        if Num == None:
            BetNum = random.choice(Groove)
        elif Num in Groove:
            BetNum = Num
        print(f"輪盤數字:{BetNum}")
        for i in Bet_List:
            if BetNum in i["BetList"]:
                Odds = 2  if i['Odds'] == 1 else i['Odds']
                Bonus = i['Money'] * Odds
                print(f"{i['UserId']} 恭喜中獎 類型:{i['BetType']} 獎金:{Bonus}")
    else:
        print("沒有玩家下注，無須開獎")
#檢查下注
def Check_repeat(Zero:bool=True,*BetList): #返還不重複的下注列表，
    if Zero : #有包含 0,00
        return list (set(Groove) & set(list(BetList)))
    else:
        return list (set(Groove) & set(list(BetList)) - set(["0"]))

#下注類型
def STRAIGHT_UP_BET(UserId,Money,*BetNum): # 單押 賠率35
    BetList = Check_repeat(BetNum)
    BetType = "單押"
    if len(BetList) == 1 :
        print(f"{UserId} 下注成功 {BetType}:{BetList} 金額:{Money}")
        Dict = {"UserId":UserId,"BetType":BetType,"BetList":BetList,"Money":Money,"Odds":35}
        Bet_List.append(Dict)
    else:
        print(f"下注失敗")

def SPLIT_BET(UserId,Money,*Num): # 雙押 賠率17
    BetList = Check_repeat(Num)
    BetType = "雙押"
    if len(BetList) == 2:
            print(f"{UserId} 下注成功 {BetType}:{BetList}金額:{Money}")
            Dict = {"UserId":UserId,"BetType":BetType,"BetList":BetList,"Money":Money,"Odds":17}
            Bet_List.append(Dict)
    else:
        print(f"下注失敗")
        
def Street_Bet(UserId,Money,*Num):# 三押 賠率11
    BetList = Check_repeat(Num)
    BetType = "三押"
    if len(BetList) == 3:
        print(f"{UserId} 下注成功 {BetType}:{BetList}金額:{Money}")
        Dict = {"UserId":UserId,"BetType":BetType,"BetList":BetList,"Money":Money,"Odds":11}
        Bet_List.append(Dict)
    else:
        print(f"下注失敗")
   
def Corner_Bet(UserId,Money,*Num):# 四押 賠率8
    BetList = Check_repeat(Num)
    BetType = "四押"
    if len(BetList) == 4:
        print(f"{UserId} 下注成功 {BetType}:{BetList}金額:{Money}")
        Dict = {"UserId":UserId,"BetType":BetType,"BetList":BetList,"Money":Money,"Odds":8}
        Bet_List.append(Dict)
    else:
        print(f"下注失敗")

def First_Five_Bet(UserId,Money,*Num): #五押 賠率6
    BetList = Check_repeat(Num)
    BetType = "五押"
    if len(BetList) == 5:
        print(f"{UserId} 下注成功 {BetType}:{BetList}金額:{Money}")
        Dict = {"UserId":UserId,"BetType":BetType,"BetList":BetList,"Money":Money,"Odds":6}
        Bet_List.append(Dict)
    else:
        print(f"下注失敗")

def Line_Bet(UserId,Money,*Num): #六押 賠率5
    BetList = Check_repeat(Num)
    BetType = "六押"
    if len(BetList) == 6:
        print(f"{UserId} 下注成功 {BetType}:{BetList}金額:{Money}")
        Dict = {"UserId":UserId,"BetType":BetType,"BetList":BetList,"Money":Money,"Odds":5}
        Bet_List.append(Dict)
    else:
        print(f"下注失敗")

def Big_Bet(UserId,Money): #大 賠率1
    BetList = []
    for i in range(19,37):
        BetList.append(str(i))
    BetType = "大"
    print(f"{UserId} 下注成功 {BetType}:{BetList}金額:{Money}")
    Dict = {"UserId":UserId,"BetType":BetType,"BetList":BetList,"Money":Money,"Odds":1}
    Bet_List.append(Dict)

def Smail_Bet(UserId,Money):#小 賠率1
    BetList = []
    for i in range(1,19):
        BetList.append(str(i))
    BetType = "小"
    print(f"{UserId} 下注成功 {BetType}:{BetList}金額:{Money}")
    Dict = {"UserId":UserId,"BetType":BetType,"BetList":BetList,"Money":Money,"Odds":1}
    Bet_List.append(Dict)

def Red_Bet(UserId,Money): #紅 賠率1
    BetList = ["1","3","5","7","9","12","14","16","18","19","21","23","25","27","30","32","34","36"]
    BetType = "紅"
    print(f"{UserId} 下注成功 {BetType}:{BetList}金額:{Money}")
    Dict = {"UserId":UserId,"BetType":BetType,"BetList":BetList,"Money":Money,"Odds":1}
    Bet_List.append(Dict)

def Black_Bet(UserId,Money):#黑 賠率1
    BetList = ["2","4","6","8","10","11","13","15","17","20","22","24","26","28","29","31","33","35"]
    BetType = "黑"
    print(f"{UserId} 下注成功 {BetType}:{BetList}金額:{Money}")
    Dict = {"UserId":UserId,"BetType":BetType,"BetList":BetList,"Money":Money,"Odds":1}
    Bet_List.append(Dict)

def Odd_Bet(UserId,Money): #單 賠率1
    BetList = []
    for i in range(1,37):
        if i %2 == 1:
            BetList.append(str(i))
    BetType = "單"
    print(f"{UserId} 下注成功 {BetType}:{BetList}金額:{Money}")
    Dict = {"UserId":UserId,"BetType":BetType,"BetList":BetList,"Money":Money,"Odds":1}
    Bet_List.append(Dict)

def Even_Bet(UserId,Money):#雙 賠率1
    BetList = []
    for i in range(1,37,3):
        if i %2 == 0:
            BetList.append(str(i))
    BetType = "雙"
    print(f"{UserId} 下注成功 {BetType}:{BetList}金額:{Money}")
    Dict = {"UserId":UserId,"BetType":BetType,"BetList":BetList,"Money":Money,"Odds":1}
    Bet_List.append(Dict)

def Row1_Bet(UserId,Money):#直行1 賠率1
    BetList = []
    for i in range(1,37,3):
        BetList.append(str(i))
    BetType = "直行1"
    print(f"{UserId} 下注成功 {BetType}:{BetList}金額:{Money}")
    Dict = {"UserId":UserId,"BetType":BetType,"BetList":BetList,"Money":Money,"Odds":1}
    Bet_List.append(Dict)

def Row2_Bet(UserId,Money):#直行2 賠率1
    BetList = []
    for i in range(2,37,3):
        BetList.append(str(i))
    BetType = "直行2"
    print(f"{UserId} 下注成功 {BetType}:{BetList}金額:{Money}")
    Dict = {"UserId":UserId,"BetType":BetType,"BetList":BetList,"Money":Money,"Odds":1}
    Bet_List.append(Dict)

def Row3_Bet(UserId,Money):#直行3 賠率1
    BetList = []
    for i in range(3,37,3):
        BetList.append(str(i))
    BetType = "直行3"
    print(f"{UserId} 下注成功 {BetType}:{BetList}金額:{Money}")
    Dict = {"UserId":UserId,"BetType":BetType,"BetList":BetList,"Money":Money,"Odds":1}
    Bet_List.append(Dict)

def One_ST_Bet(UserId,Money):#區域1 賠率1
    BetList = []
    for i in range(1,13):
        BetList.append(str(i))
    BetType = "1st"
    print(f"{UserId} 下注成功 {BetType}:{BetList}金額:{Money}")
    Dict = {"UserId":UserId,"BetType":BetType,"BetList":BetList,"Money":Money,"Odds":1}
    Bet_List.append(Dict)

def Two_ST_Bet(UserId,Money):#區域2 賠率1
    BetList = []
    for i in range(13,25):
        BetList.append(str(i))
    BetType = "2nd"
    print(f"{UserId} 下注成功 {BetType}:{BetList}金額:{Money}")
    Dict = {"UserId":UserId,"BetType":BetType,"BetList":BetList,"Money":Money,"Odds":1}
    Bet_List.append(Dict)

def Three_ST_Bet(UserId,Money):#區域3 賠率1
    BetList = []
    for i in range(25,37):
        BetList.append(str(i))
    BetType = "3rd"
    print(f"{UserId} 下注成功 {BetType}:{BetList} 金額:{Money}")
    Dict = {"UserId":UserId,"BetType":BetType,"BetList":BetList,"Money":Money,"Odds":1}
    Bet_List.append(Dict)    

