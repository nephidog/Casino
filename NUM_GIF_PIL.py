import imageio
from PIL import Image
#逆時鐘
Groove = ["0","32","15","19","4","21","2","25","17","34","6","27","13","36","11","30","8","23","10"\
    ,"5","24","16","33","1","20","14","31","9","22","18","29","7","28","12","35","3","26"]
#順時鐘
Parts = 3 #分鏡的角度
Groove.reverse()
Num_Dict = {}
for i in range(37):
    Num_Dict[str(i)] = []
    for j in range(1,Parts+1):
        Num_Dict[str(i)].append(Image.open(f"Roulette_Num_300\\{i}_{Parts}_{j}.PNG"))



def CreateNum(Num):
    # 開頭動畫
    Roulette_Box = []
    Run = 2
    for i in range (10): #停止畫面
        Roulette_Box.append(Num_Dict["0"][2])
    for i in range(Run): #開始轉動
        for j in Groove:
            for parts in range(Parts):
                Roulette_Box.append(Num_Dict[j][parts])
        if i == Run-1 and j == Num:
            break
    index = Groove.index(Num)
    New_Groove = Groove[index+1:]
    New_Groove.extend(Groove[:index+1])
    Num_A(Roulette_Box,New_Groove,Num)
    save_name = f'{Num}_{parts}.gif'  
    Roulette_Box[0].save(save_name, save_all=True,append_images=Roulette_Box,loop=1,duration=20)#fps=10
    print("輸出完成")

def Num_A(Roulette_Box:list,New_Groove,Num): #自然停止
    gif_images = Roulette_Box
    Count_1= 1
    Count_2 = 0
    Max = 2
    for i in range(Max):
        for j in range(len(New_Groove)):
            if i == Max-1 :
                index = New_Groove.index(New_Groove[j])
                Count_2 = int(index//30)
            for parts in range(Parts):    
                for fps in range(Count_1+Count_2):
                    gif_images.append(Num_Dict[New_Groove[j]][parts])
                if i==Max-1 and j == len(New_Groove)-1:
                    save_name = f'{Num}_{parts}.gif'  
                    Roulette_Box[0].save(save_name, save_all=True,append_images=Roulette_Box,loop=1,duration=20)#fps=10
                    print(f"{Num}_{parts}輸出完成")
        Count_1 += 1

   
CreateNum("1")
# for i in Groove:
#     CreateNum(i)    
