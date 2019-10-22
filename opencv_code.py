import cv2
import numpy as np 
import requests

def nothing(x):
    pass

url='http://192.168.43.1:8080/video'
url2='http://192.168.43.217/'
cap=cv2.VideoCapture(url)
#cap.set(cv2.CAP_PROP_BUFFERSIZE,1)

cv2.namedWindow("image")
cX=0
Extreme=100000

cv2.createTrackbar("low_Y","image",46,255,nothing)
cv2.createTrackbar("low_Cr","image",79,255,nothing)
cv2.createTrackbar("low_Cb","image",96,255,nothing)
cv2.createTrackbar("high_Y","image",155,255,nothing)
cv2.createTrackbar("high_Cr","image",121,255,nothing)
cv2.createTrackbar("high_Cb","image",121,255,nothing)


while True:
    cap=cv2.VideoCapture(url)

   #  print("Frame count:",cv2.CAP_PROP_FRAME_COUNT)
    
    ret,img=cap.read()
    
    img_blur=cv2.GaussianBlur(img,(21,21),0)
    img_ycrcb=cv2.cvtColor(img_blur,cv2.COLOR_BGR2YCrCb)

    low_y=cv2.getTrackbarPos("low_Y","image")
    low_cr=cv2.getTrackbarPos("low_Cr","image")
    low_cb=cv2.getTrackbarPos("low_Cb","image")
    high_y=cv2.getTrackbarPos("high_Y","image")
    high_cr=cv2.getTrackbarPos("high_Cr","image")
    high_cb=cv2.getTrackbarPos("high_Cb","image")

    lower=np.array([low_y,low_cr,low_cb],dtype=np.uint8)
    upper=np.array([high_y,high_cr,high_cb],dtype=np.uint8)
    mask=cv2.inRange(img_ycrcb,lower,upper)

    contours,heirarchy=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if (len(contours)==0):
       
        requests.get(url2+"left")
        print("searching....")
    if(len(contours)!=0):
        c=max(contours,key=cv2.contourArea)
        cv2.drawContours(img,[c],-1,(0,0,255),3)
        M=cv2.moments(c)
        area=cv2.contourArea(c)
        if(area!=0):
           if(area>100):
            cX = int(M["m10"] / area)
       
            if(area>Extreme):
               print("stop")
               requests.get(url2+"halt")
            elif(cX>390):
               print("right")
               requests.get(url2+"right") 
               # t.sleep(1)
            elif(cX<310):
               
               print("left")
               requests.get(url2+"left") 
            elif(310<cX<390):
                print("forward")          
                requests.get(url2+"forward") 
    
    
    cv2.imshow("image",img)
    cv2.imshow("image",mask)
    k=cv2.waitKey(1)
    if k==27:
        break
