import time
from PIL import Image
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer,Float ,VARCHAR
from sqlalchemy import create_engine
 
#Json
def Json_Open():
    with open(f"User.json","r",encoding="utf8") as jfile:
        jdata = json.load(jfile)
        return jdata
def Json_Save():
    with open(f"User.json","w",encoding="utf8") as jfile:
        json.dump(jdata,jfile,indent=4)
try: #開啟json檔案
    jdata = Json_Open()
except: #若沒有則建立一個新的
    jdata = {"Username":"","Email":""}
    Json_Save()

#資料庫連線    
engine = create_engine('mysql+pymysql://nephidog_nephidog:asd123asd123@31.22.4.76/nephidog_happylive', echo=False)
Base = declarative_base()
class AppInfo_User(Base):
    __tablename__ = 'piwigo_users'
    id = Column('id', Integer, primary_key=True)
    username = Column(VARCHAR)
    mail_address = Column(VARCHAR)

class AppInfo_user_infos(Base):
    __tablename__ = 'piwigo_user_infos'
    id = Column('user_id', Integer, primary_key=True)
    status = Column("status",VARCHAR)  

Session = sessionmaker(bind=engine)
session = Session()
LoinCount = 0
# 登入驗證
while True:
    try:
        if jdata["Username"]!="" and jdata["Email"] != 0 and LoinCount == 0 :
            input_Username,input_Email = jdata["Username"],jdata["Email"]
        else:
            input_Username = input("請輸入使用者名稱: ")
            input_Email = input("請輸入註冊信箱: ")
        AppInfo = session.query(AppInfo_User).filter_by(username=input_Username , mail_address=input_Email).first()
        userid = AppInfo.id
        AppInfo_infos = session.query(AppInfo_user_infos).filter_by(id=userid).first()
        status = AppInfo_infos.status
        if status in ["webmaster","admin"]:
            print(f"登入成功歡迎:{AppInfo.username}")
            jdata["Username"] = input_Username
            jdata["Email"] = input_Email
            Json_Save()
            break
        else:
            print("當前用戶無使用權限，請聯繫 Nephi 取得權限，或更換帳戶")
            LoinCount += 1
    except:
        print("用戶信息不對，請重新輸入")
        LoinCount += 1

def OpenImg(): #開啟圖片
    while True:
        try:
            imgname = input("請輸入要拆分的圖片名稱: ")
            if imgname[-4:].lower() != ".png":
                imgname += ".png"
            img = Image.open(f"{imgname}").convert("RGBA")
            return img
        except:
            print(f"找不到 '{imgname}' 請再次確認")


def Check_Adjacent(Point,Bar,Blurry=0): #判斷傳進來的點是否相鄰
    # Blurry = (Blurry**2 + Blurry** 2 )*0.5
    x1,y1,x2,y2 = Bar
    x1 -= Blurry
    y1 -= Blurry
    x2 += Blurry
    y2 += Blurry
    if x1 <= Point[0] <= x2 and y1 <= Point[1] <= y2: #判斷點是否在範圍中
        return True
    else:
        return False

def Point_Min_Max(Bar,NewPoint): #回傳列表中左上角和右下角的點
    X_List,Y_List = [Bar[0],Bar[2],NewPoint[0]],[Bar[1],Bar[3],NewPoint[1]] 
    return (min(X_List),min(Y_List),max(X_List),max(Y_List))

def plan(Bar): #取得兩點距離
    x1,y1,x2,y2 = Bar
    return ((x1-x2)**2 + (y1-y2)**2)**0.5    

#拆圖
Run = True #程式執行開關
img = None

while Run:
    if img == None:
        img = OpenImg()
    L,H = img.size
    box = [] #存放不透明座標
    Barlist = [] #存放圖片座標列表 [(x1,y1,x2,y2).....]
    #尋找不透明像素
    print("----- 尋找非透明圖層 -----")
    Min_distance = None #最小X間距
    distance_list = []
    for h in range(H):#
        distance = 0 #圖片的間距
        for l in range(L): #
            dot = (l,h)
            if img.getpixel(dot)[-1] != 0:
                box.append(dot)
                distance += 1
            elif distance != 0:
                #if Min_distance == None or distance < Min_distance:
                #     Min_distance = distance
                distance_list.append(distance)
                distance = 0
    avg_distance = int(sum(distance_list)/len(distance_list))
    print(f"平均偏差:{avg_distance}")

    while True:
        try:
            Blurry = int(input(f"請輸入允許值 1~{avg_distance} (愈低愈精確) :"))
            if Blurry>=0:
                if Blurry < 1 :
                    Blurry = 1
                # Blurry = (Blurry**2+Blurry**2)**0.5
                print(f"兩點距離 {Blurry} 內將視為同一張圖片")
                break
        except:
            print("Error 請輸入數字")
    
    print(f"開始分析圖片")
    PointListSum = 0
    start = time.time()        
    while len(box)>0:
        PointList = [box[0]]
        Bar = (box[0][0],box[0][1],box[0][0],box[0][1])        
        while True:
            Count = 0
            for i in box:
                if Check_Adjacent(i,Bar,Blurry):
                    Bar = Point_Min_Max(Bar,i)
                    PointList.append(i)
                    PointListSum += 1
                    box.remove(i)
                    Count += 1
                    print(f"\r圖片:{len(Barlist)+1} 範圍:{Bar} 像素:{len(PointList)} 進度:{PointListSum}/{PointListSum+len(box)} ({PointListSum/(PointListSum+len(box)):.2%})",end="")
            if Count == 0: # 沒找到相鄰座標跳出迴圈，存放當前座標 
                print(f"\r圖片:{len(Barlist)+1} 範圍:{Bar} 像素:{len(PointList)} 進度:{PointListSum}/{PointListSum+len(box)} ({PointListSum/(PointListSum+len(box)):.2%})")
                break  
        Barlist.append(Bar) #存放當前座標
    while True:
        choose = input(f"分析完成，分出{len(Barlist)}張圖 ， 1.輸出檔案 2.重新分析 3.結束程式 : ")
        if choose == "1":
            while True:
                ImgName = input("請輸入輸出檔名: ")
                checkname = input(f"若有多張圖將依此序命名 {ImgName}1 ,{ImgName}2,{ImgName}3... ，請再次確認 (Y/N): ")
                if checkname.lower() == "y":
                    break
            list_length = len(Barlist)  
            for i in range(0, list_length):  
                for j in range(0, list_length-i-1): 
                    if Barlist[j][0]>Barlist[j+1][0] :
                        Barlist[j],Barlist[j+1] = Barlist[j+1],Barlist[j]
                    elif Barlist[j][0] == Barlist[j+1][0] and Barlist[j][1] > Barlist[j+1][1]:
                        Barlist[j],Barlist[j+1] = Barlist[j+1],Barlist[j]
            # 檔案輸出
            print("----- 排序 & 輸出 -----")
            Num = 1
            for i in range(len(Barlist)):
                x1,y1,x2,y2 = Barlist[i] 
                if (x1-x2)*(y1-y2) > 50: #排除太小的圖
                    print(f"存檔: {ImgName}{Num}.png Bar:{Barlist[i]}")
                    new_img = img.crop(Barlist[i])
                    new_img.save(f"{ImgName}{Num}.png")
                    Num += 1
            end = time.time()
            print(f"存檔完成，花費時間:{end - start:.2f}秒")
            # 是否再次運行
            choose = input(f"是否再次運行 1.重新分析本圖片 2.分析下一張圖片 3.結束程式: ")
            if choose == "1":
                break
            if choose == "2":
                img = None
                break
            if choose == "3":
                Run = False
                break
        if choose == "2":
            break
        if choose == "3":
            Run = False
            break
for i in range(5,-1,-1):
    print(f"\r感謝使用本程式 {i} 秒後將自動關閉",end="")
    time.sleep(1)
        
