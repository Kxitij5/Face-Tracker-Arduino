#Run the following commands on the terminal to install the python packages
# pip install opencv-python serial pyserial

import cv2
import serial,time
face_cascade= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap=cv2.VideoCapture(0) # put the index of the connected webcam
#fourcc= cv2.VideoWriter_fourcc(*'XVID')
#change the com port based the port to which the arduino is connected, Check com in arduino ide
ArduinoSerial=serial.Serial('com4',9600,timeout=0.1)
#out= cv2.VideoWriter('face detection4.avi',fourcc,20.0,(640,480))
time.sleep(1)
global prevX,prevY,flag
prevX=0
prevY=0
flag=0
while cap.isOpened():
    ret, frame= cap.read()
    frame=cv2.flip(frame,1)  #mirror the image
    #print(frame.shape)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces= face_cascade.detectMultiScale(gray,1.1,6)  #detect the face
    for x,y,w,h in faces:
        #sending coordinates to Arduino
        currX = x+w//2
        currY = y+h//2
        if (currX-prevX)<3 and (currY-prevY)<3:
            flag=1
        else:
            flag=0
        string='X{0:d}Y{1:d}F{2:d}'.format((currX),(currY),(flag))
        print(string)
        prevX = currX
        prevY = currY
        ArduinoSerial.write(string.encode('utf-8'))
        #plot the forehead
        cv2.circle(frame,(x+w//2,y+h//5),2,(0,0,255),2)
        #plot the roi
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),3)
    #plot the squared region in the center of the screen
    # cv2.rectangle(frame,(640//2-30,480//2-30),
    #              (640//2+30,480//2+30),
    #               (255,255,255),3)
    #out.write(frame)
    cv2.imshow('img',frame)#remove this line if not using a monitor 
    #cv2.imwrite('output_img.jpg',frame)
    '''for testing purpose
    read= str(ArduinoSerial.readline(ArduinoSerial.inWaiting()))
    time.sleep(0.05)
    print('data from arduino:'+read)
    '''
    # press q to Quit
    if cv2.waitKey(10)&0xFF== ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
