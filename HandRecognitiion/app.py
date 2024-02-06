import serial
import cv2
import mediapipe as mp
import time
import math
from google.protobuf.json_format import MessageToDict


#------------------------------------------

cameraIndex = 0
detectionConfidence = 0.8
trackingConfidence = 0.5
maxDetectedHands = 4
staticImageMode = False

cap = cv2.VideoCapture(cameraIndex)

#-------------------------------------------
    

mpHands = mp.solutions.hands
hands = mpHands.Hands(staticImageMode, max_num_hands=maxDetectedHands,
                      min_detection_confidence=detectionConfidence,
                      min_tracking_confidence=trackingConfidence)

mpDraw = mp.solutions.drawing_utils

fingerTips = [4, 8, 12, 16, 20]
distance = 0
thumbCurrentPosition = 0
handType = None

sr = serial.Serial("COM6", 19200, timeout=1)
time.sleep(2)

def getDistance( point_A, point_B ):

    x1 = point_A[0]
    x2 = point_B[0]

    y1 = point_A[1]
    y2 = point_B[1]

    return math.sqrt( math.pow( (x2 - x1), 2) + math.pow( (y2 - y1), 2) )
    

while True:

    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    results = hands.process(imgRGB)
    
    # DETECT IF HANDS ARE PRESENT
    if results.multi_hand_landmarks:

        for element in results.multi_handedness:
            handType = MessageToDict(element)['classification'][0]['label']

            if handType == 'Left':
                handType = 'Right'
            elif handType == 'Right':
                handType = 'Left'
        
        for handLandmarks in results.multi_hand_landmarks:
            for id, lm in enumerate(handLandmarks.landmark):

                
                height, width, center = img.shape
                fingerPointPosition = (int(lm.x*width), int(lm.y*height) )

                # GET THE CURRENT THUMB_TIP POSITION TO DRAW THE LINE
                if id == fingerTips[0]:
                    thumbCurrentPosition = fingerPointPosition

                # FOR ALL FINGERTIPS, DRAW A CIRLCE TO IDENTIFY THEM
                if id in fingerTips:
                    cv2.circle(img, fingerPointPosition, 12, (255, 0, 255), cv2.FILLED)

                # FOR AL FINGERTIPS, EXCEPT THE THUMB, DRAW A LINE TO THE THUMB
                if id in fingerTips and id != 4:

                    # STORE THE DISTANCE OF ALL FINGERSTIPS RELATIVE TO THE THUMB_TIP
                    distance = getDistance(fingerPointPosition, thumbCurrentPosition)
                    
                    if distance <= 30:
                        cv2.line(img,  fingerPointPosition, thumbCurrentPosition,(0, 255, 0), 9)

                        if handType == 'Right':
                            if id == 8:
                                sr.write(b'b')
                            elif id == 12:
                                sr.write(b's')
                            elif id == 16:
                                sr.write(b'e')
                            elif id == 20:
                                sr.write(b'w')
                                
                        elif handType == 'Left':

                            if id == 8:
                                sr.write( b'h' )
                            elif id == 12:
                                sr.write(b'i')
                            elif id == 16:
                                sr.write(b'j')
                            elif id == 20:
                                sr.write(b'k')
                                
            # DRAW THE CONNECTIONS FOR EACH POINT ON THE HAND 
            mpDraw.draw_landmarks(img, handLandmarks, mpHands.HAND_CONNECTIONS)

    # DISPLAY THE CAMERA IMAGE
    cv2.imshow("Lynxmotion Hand-Tracking", img)
    cv2.waitKey(1)








