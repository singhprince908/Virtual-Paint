import cv2
import numpy as np





cap = cv2.VideoCapture(0)


mycolors = [[92,93,67,110,255,255],[0,146,143,179,255,255],[26,60,42,72,255,223]]


mycolorvalues = [[255,0,0],[51,153,255],[0,255,0]]

myPoints = []

def findcolor(img,mycolors,mycolorvalues):
    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count=0
    newpoints=[]
    for color in mycolors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imghsv, lower, upper)
        x,y=getcontors(mask)
        cv2.circle(imgResult,(x,y),15,mycolorvalues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newpoints.append([x,y,count])
        count +=1
      #     cv2.imshow(str(color[0]),mask)
    return newpoints

def getcontors(img):
    contors,hierarchy= cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contors:
        area = cv2.contourArea(cnt)
        if area > 500:
            #cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h=cv2.boundingRect(approx)
    return x+w//2,y



def Drawoncanvas(mypoints,mycolorvalues):
     for point in mypoints:
         cv2.circle(imgResult, (point[0], point[1]), 10, mycolorvalues[point[2]], cv2.FILLED)



while True:
    success,img=cap.read()
    imgResult = img.copy()
    newpoints = findcolor(img,mycolors,mycolorvalues)
    if len(newpoints)!=0:
        for newP in newpoints:
            myPoints.append(newP)
    if len(myPoints) != 0:
        Drawoncanvas(myPoints,mycolorvalues)
    cv2.imshow("img",imgResult)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
