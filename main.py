import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import*

model=YOLO('yolov8s.pt')



def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        colorsBGR = [x, y]
        print(colorsBGR)
        

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

cap=cv2.VideoCapture('C:/Users/asus/Desktop/obj detect Project/veh.mp4')


my_file = open("C:/Users/asus/Desktop/obj detect Project/coco.txt", "r")
data = my_file.read()
class_list = data.split("\n") 

count=0

tracker=Tracker()

cy1=323
cy2=367
offset=6
vh_down={}
counter=[]
vh_up={}
counter1=[]

while True:    
    ret,frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue
    frame=cv2.resize(frame,(1020,500))
   

    results=model.predict(frame)
 #   print(results)
    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")
#    print(px)
    list=[]
             
    for index,row in px.iterrows():
#        print(row)
 
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        c=class_list[d]
        if 'car' in c:
            list.append([x1,y1,x2,y2])
    bbox_id=tracker.update(list)
    for bbox in bbox_id:
        x3,y3,x4,y4,id=bbox
        cx=int(x3+x4)//2
        cy=int(y3+y4)//2
        if cy1<(cy+offset) and cy1 > (cy-offset):
            vh_down[id]=cy
        if id in vh_down:
            if cy2<(cy+offset) and cy2 > (cy-offset):
                cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                if counter.count(id)==0:
                    counter.append(id)

        if cy2<(cy+offset) and cy2 > (cy-offset):
            vh_up[id]=cy
        if id in vh_up:
            if cy1<(cy+offset) and cy1 > (cy-offset):
                cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                if counter1.count(id)==0:
                    counter1.append(id)


    cv2.line(frame,(267,cy1),(829,cy1),(255,255,255),1)
    cv2.putText(frame,('1st Line'),(274,318),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
     
    cv2.line(frame,(177,cy2),(927,cy2),(255,255,255),1)
    cv2.putText(frame,('2st Line'),(181,363),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
    d=(len(counter))
    cv2.putText(frame,('Going Down->')+str(d),(60,40),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
     
    u=(len(counter1))
    cv2.putText(frame,('Going Up->')+str(u),(60,120),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)     

    print(counter)
    cv2.imshow("RGB", frame)
    if cv2.waitKey(1)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()

