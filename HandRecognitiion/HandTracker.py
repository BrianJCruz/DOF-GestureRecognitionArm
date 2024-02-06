import cv2
import time
import math
from enum import Enum
import mediapipe as mp
from google.protobuf.json_format import MessageToDict
import serial

# Enumerate each finger based on the Land Mark Diagram provided in this report.
class FingerTips(Enum):
        
    THUMB_TIP = 4
    INDEX_TIP = 8
    MIDDLE_TIP = 12
    RING_TIP = 16
    PINKY_TIP = 20

# Main Class
class HandTracker():

    # Constructor
    def __init__(self,  
        staticImageMode = False, max_num_hands = 2, min_detection_confidence = 0.75, min_tracking_confidence = 0.75):

        # Configures the parameters defined in Mediapipe's method "Hands()"
        self.staticImageMode = staticImageMode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        # Main hand detection model used
        self.model = mp.solutions.hands

        # Draws and connects the diffrent hand land mark points
        self.drawer = mp.solutions.drawing_utils
        self.tracker = self.model.Hands(
            self.staticImageMode, 
            max_num_hands=self.max_num_hands, 
            min_detection_confidence=self.min_detection_confidence, 
            min_tracking_confidence=self.min_tracking_confidence
        )

        # Automatically detect the serial port in which the Arduino device is running
        self.sr = self.getSerialCom()

        # Automatically detect the camera index for the CV2 camera detection.
        # Default is 0 for most camera laptops
        self.getCamerasIndex()

    # Automatically detect the serial port in which the Arduino device is running
    def getSerialCom(self):
        for index in range(1, 30):
            try:
                val = serial.Serial(f"COM{index}", 19200, timeout=1)
                return val
            except:
                pass
    
    # Automatically detect the camera index for the CV2 camera detection.
    # Default is 0 for most camera laptops
    def getCamerasIndex(self):
        global video
        for cameraIndex in range(-1, 3):
            video = cv2.VideoCapture(cameraIndex)
            if video is None or not video.isOpened():
                pass
            else:
                return True
        return False
    
    # Used for detecting how near is each finger from the thumb
    # Distance Equation
    def getDistance(self, point_A, point_B ):
        x1 = point_A[0]
        x2 = point_B[0]
        y1 = point_A[1]
        y2 = point_B[1]

        return math.sqrt( math.pow( (x2 - x1), 2) + math.pow( (y2 - y1), 2) )

    # Retrieves wether the hand showed is left or right.
    # This property is already detected by Mediapipe's landmark dictionary
    # We just need to read it
    def getHandDirection(self, results):
        for hand in results.multi_handedness:
            direction = MessageToDict(hand)['classification'][0]['label']
            direction_map = {'Left': 'Right', 'Right': 'Left'}
            return direction_map.get(direction, direction)
            

            
    # Start the hand tracking
    def startCaptureCV2(self, windowTitle):
        global handDirection

        # Creates a list based on the FingerTips enumerator which includes all the indexes
        # of each fingertip
        finger_tips_list = [finger_tip.value for finger_tip in FingerTips]
        
        thumbCurrentPosition = 0
        distance = 0

        # While program is running:
        while True:

            status, image = video.read()
            colorRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.tracker.process(colorRGB)

            # if hand is detected:
            if results.multi_hand_landmarks:

                # Get wether is the left or right hand
                handDirection = self.getHandDirection(results)

                # For each hand point
                for handLandmarks in results.multi_hand_landmarks:

                    # Enumerate each hand point and store its id
                    for id, lm in enumerate(handLandmarks.landmark):

                        # Store hand's x, y
                        height, width, center = image.shape

                        # Get Hand Point position 
                        fingerPointPosition = ( 
                            int(lm.x*width), 
                            int(lm.y*height) 
                        )

                        # If the fingertip in the camera is the thumb one:
                        if id == FingerTips.THUMB_TIP.value:

                            # Get the thumb's current position
                            thumbCurrentPosition = fingerPointPosition

                        # Draw a purple cirlcle for each fingertip
                        if id in finger_tips_list:
                            cv2.circle(
                                image, 
                                fingerPointPosition, 
                                12, 
                                (255, 0, 255), 
                                cv2.FILLED
                            )

                        # For each fingertip that is not the thumb
                        if id in finger_tips_list and id !=4:

                            # calculate the distance relative to the thumb
                            distance = self.getDistance(
                                fingerPointPosition, 
                                thumbCurrentPosition
                            )

                            # if said distance is close enough:
                            if distance <= 30:

                                # Draw a green line
                                cv2.line(
                                    image, 
                                    fingerPointPosition, 
                                    thumbCurrentPosition, 
                                    (0, 255, 0), 
                                    9
                                )

                                # Serial messages to send to "ServoArmController.h"
                                right_hand_map = {8: b'b', 12: b's', 16: b'e', 20: b'w'}
                                left_hand_map = {8: b'h', 12: b'i', 16: b'j', 20: b'k'}

                                # Send the serial messages depending on the hand type
                                if handDirection == 'Right':
                                    message = right_hand_map.get(id)
                                elif handDirection == 'Left':
                                    message = left_hand_map.get(id)
                                if message:
                                    self.sr.write(message)
                                    
                    # Connect each point in the hand with a line        
                    self.drawer.draw_landmarks(image, handLandmarks, self.model.HAND_CONNECTIONS)

            # Show the camera window with a predefined title 
            cv2.imshow(windowTitle, image)
            cv2.waitKey(1)

# ------------Testing----------------
ht = HandTracker()
ht.startCaptureCV2("Lynxmotion-Hand Tracking")



                        

                                
                                
                        
                        
                        
                
                
                
            
        

    

    
            


    
