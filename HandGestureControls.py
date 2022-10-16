import cv2
import pyautogui as control
from cvzone.HandTrackingModule import HandDetector
import time
import mouse
import numpy as np

# Global Variables
WIDTH, HEIGHT = 1920, 1080
gestureThreshold = 600
Range = [0, 0]

# Creation of a camera object
cap = cv2.VideoCapture(0)
cap.set(3, WIDTH)
cap.set(4, HEIGHT)

# Hand Detector
detector = HandDetector(detectionCon=0.9, maxHands=1)

while True:
    
    # Taking in camera feed
    success, img = cap.read()
    img = cv2.flip(img, 1)
    key = cv2.waitKey(1)
    
    # Hand Detector Model
    hands, img = detector.findHands(img)
    
    # Draw a boundary line
    cv2.line(img, (0, gestureThreshold), (WIDTH, gestureThreshold), (0, 255, 0), 3)
    
    # If we detect a hand
    if hands:
        
        # Ironic variables
        left = 'Right'
        right = 'Left'
        
        # Get the landmarks of the hand, and number of fingers up
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        
        # If center of hand is above that line then continue
        if cy <= gestureThreshold:
            
            # Now check the gestures
            
            # KEYBOARD OPERATIONS by Right hand
            
            # LEFT
            if fingers == [1, 0, 0, 0, 0] and hand['type'] == right:
                control.keyDown('left')
                control.keyUp('left')
                time.sleep(0.5)
            
            # RIGHT
            if fingers == [0, 1, 1, 1, 1] and hand['type'] == right:
                control.keyDown('right')
                control.keyUp('right')
                time.sleep(0.5)
                     
            # CUSTOM - SPACEBAR
            if fingers == [0, 1, 1, 0, 0] and hand['type'] == right:
                control.keyDown('space')
                control.keyUp('space')
                time.sleep(0.5)
                
            # MOUSE OPERATIONS by Left hand
            
            # MOUSE DRAG
            if fingers == [0, 1, 0, 0, 0] and hand['type'] == left:
                prev_pos = np.array(mouse.get_position())
                curr_pos = np.array(hand['center'])
                scaled_pos = curr_pos - np.array([1100 // 2, gestureThreshold // 2])
                new_position = tuple(prev_pos + 0.4 * scaled_pos)
                control.moveTo(new_position, duration=0)
                
            if fingers == [0, 1, 1, 0, 0] and hand['type'] == left:
                mouse.click('left')
                time.sleep(0.1)
                
            if fingers == [1, 1, 1, 0, 0] and hand['type'] == left:
                mouse.click('right')
                time.sleep(0.1)
    
    # Display
    cv2.imshow("Image", img)
    
    # Allow to exit the loop
    if key == ord('q') or hands and fingers == [0, 1, 0, 0, 1]:
        break

cap.release()
cv2.destroyAllWindows()