import time
from PIL import Image
img = Image.open(f"道具.PNG").convert("RGBA")
L,H = img.size
box = [] #存放不透明座標
Barlist = [] #存放圖片座標列表 [(x1,y1,x2,y2).....]
Name = "道具"

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

PointListSum = 0
start = time.time()
print(f"開始組建圖片")
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
    # print(f"Bar:{Bar}")
    # img.crop(Bar).show()
# 氣泡排序
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
        print(f"存檔: {Name}{Num}.png Bar:{Barlist[i]}")
        new_img = img.crop(Barlist[i])
        new_img.save(f"{Name}_{Num}.png")
        Num += 1
end = time.time()
print(f"花費時間:{end - start:.2f}秒")
