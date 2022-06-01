import imageio
from PIL import Image

外框 = Image.open("外框.PNG")
內圈 = Image.open("內圈.PNG")
Angle = 360/37 #角度

Groove = ["0","32","15","19","4","21","2","25","17","34","6","27","13","36","11","30","8","23","10"\
    ,"5","24","16","33","1","20","14","31","9","22","18","29","7","28","12","35","3","26"] #原本錶盤順序
Groove.remove   
index = Groove.index("13")
New_Groove = Groove[index+1:]
New_Groove.extend(Groove[:index+1]) #新錶盤順序
print(f"New_Groove:{New_Groove}")

def Create_PNG(Num,Parts):
    index = New_Groove.index(Num)  
    for i in range(Parts):
        Img = 內圈.rotate(index*Angle+Angle/Parts*i*-1)
        r,g,b,a = 外框.convert("RGBA").split()
        Img.paste(外框,(0,0),mask=a)
        # Img.show()
        Img=Img.resize((300,300))
        Img.save(f"Roulette_Num_300/{Num}_{Parts}_{i+1}.png")
for i in Groove:
    Create_PNG(i,3)

