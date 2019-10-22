/* 
*
*  Code for ball tracking robot for RIG WORKSHOP 2019
*  Organisation : Robotics Interest Group, NITC
*
*/

# Importing all required dependencies
import numpy as np
import requests
import cv2

# All variables we use 
ip_cam_url="http://192.168.43.1:8080/video"                 #  IP  from ipwebcam app 
nodemcu_url="http://192.168.43.2/"                          #  IP of NodeMcu

# Defining nothing function
def nothing (x):
    pass

# Creating a named window 
# Here all trackbars are put and image is displayed
cv2.namedWindow('image')

# Creating all Tackbars
cv2.createTrackbar('Low_L','image',0,255,nothing)
cv2.createTrackbar('Low_A','image',0,255,nothing)
cv2.createTrackbar('Low_B','image',0,255,nothing)

# Starting a video capture from the ip web cam
capture=cv2.VideoCapture(ip_cam_url)
# Capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# In an infinite loop we repeatedly sends the request 
# according to position of ball in the frame
while True:
    # Reading image from caputre 
    _,image=capture.read()
    
    # Doing gaussian blur 
    image=cv2.GaussianBlur(image,(21,21),0)
    # (21,21) is the size of the gaussian kernel

    # Converting from BGR to LAB 
    lab_image=cv2.cvtColor(image,cv2.COLOR_BGR2LAB)

    # Masking the image to get only the ball
    # Getting lower value
    lower=np.asarray([cv2.getTrackbarPos('Low_L','image'),cv2.getTrackbarPos('Low_A','image'),cv2.getTrackbarPos('Low_B','image')],dtype="uint8")
    upper=np.asarray([255,255,255],dtype="uint8")
    masked_image=cv2.inRange(lab_image,lower,upper)

    # Doing bitwise and to get only the image of the ball
    #output_image=cv2.bitwise_and(image,image,mask=masked_image)

    # Finding contours in the output image
    #gray_image=cv2.cvtColor(output_image,cv2.COLOR_BGR2GRAY)
    contours,heirarcy=cv2.findContours(masked_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 

    if len(contours)==0:
        requests.get(url=nodemcu_url+'halt')
        
    # Drawing all contours
    cv2.drawContours(image,contours,-1,(0,255,0),2)
    cv2.imshow("image",image)

    for c in contours:
        # Getting moments
        moment=cv2.moments(c)
        # Calculating area
        area=moment['m00']
        #print(area)
        if (area>90000):
            requests.get(url=nodemcu_url+'halt')
       
        elif (2000<area<90000):
            cx=int(moment['m10']/area)
            if (cx>340):
                requests.get(url=nodemcu_url+'right')
                #print("right")
                #print("right")
            elif  (cx<300):
                requests.get(url=nodemcu_url+'left') 
                #print("left")
                #print("left")
            elif (300<cx<340):
                requests.get(url=nodemcu_url+'forward')
                #print("forward")
                #print("forward")
        
    
    # Press q to quit
    if cv2.waitKey(1)==ord("q"):
        break
    
