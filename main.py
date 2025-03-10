import cv2
import mediapipe as mp
import time
import numpy as np
from control_key_file import right_pressed,left_pressed,up_pressed,down_pressed
from control_key_file import KeyOn, KeyOff
#import pyautogui

left_key_pressed=left_pressed
right_key_pressed=right_pressed
up_key_pressed=up_pressed
down_key_pressed=down_pressed

time.sleep(2.0)
current_key_pressed = set()

mp_draw=mp.solutions.drawing_utils
mp_hand=mp.solutions.hands

tipIds=[4,8,12,16,20]

video=cv2.VideoCapture(0)


def get_label(index, hand, results):
    output = None
    for idx, classification in enumerate(results.multi_handedness):
        if classification.classification[0].index == index:
            # Process results
            label = classification.classification[0].label
            score = classification.classification[0].score
            text = '{} {}'.format(label, round(score, 2))

            # Extract Coordinates
            coords = tuple(np.multiply(
                np.array((hand.landmark[mp_hand.HandLandmark.WRIST].x, hand.landmark[mp_hand.HandLandmark.WRIST].y)),
                [640, 480]).astype(int))

            output = text, coords

    return output
with mp_hand.Hands(min_detection_confidence=0.5,
               min_tracking_confidence=0.5) as hands:
    while True:
        keyPressed = False
        break_pressed=False
        jump_pressed=False
        dunk_pressed=False
        accelerator_pressed=False
        key_count=0
        key_pressed=0
        ret,image=video.read()
        image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable=False
        results=hands.process(image)
        image.flags.writeable=True
        image=cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lmList=[]
        text=''
        if results.multi_hand_landmarks:
            for idx, classification in enumerate(results.multi_handedness):
                if classification.classification[0].index == idx:
                    label = classification.classification[0].label
                    text = '{}'.format(label)
                else:
                    label = classification.classification[0].label
                    text = '{}'.format(label)
            for hand_landmark in results.multi_hand_landmarks:
                myHands=results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h,w,c=image.shape
                    cx,cy= int(lm.x*w), int(lm.y*h)
                    lmList.append([id,cx,cy])
                mp_draw.draw_landmarks(
                    image, 
                    hand_landmark, 
                    mp_hand.HAND_CONNECTIONS,
                    mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),  # Green landmarks
                    mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)   # Red connections
                )
        fingers=[]

        if len(lmList)!=0:
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1,5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total=fingers.count(1)
            if total==4 and text=="Right":
                # Get frame dimensions
                h, w, c = image.shape  

                # Define box dimensions and position (top-right corner)
                box_width, box_height = 250, 100  
                top_left = (w - box_width - 20, 20)  # 20 pixels padding from the right and top
                bottom_right = (w - 20, 20 + box_height)

                # Draw black rectangle at the top-right corner
                cv2.rectangle(image, top_left, bottom_right, (0, 0, 0), cv2.FILLED)

                # Center text inside the box
                font_scale = 2
                thickness = 5
                (text_width, text_height), baseline = cv2.getTextSize("LEFT", cv2.FONT_HERSHEY_TRIPLEX, font_scale, thickness)

                text_x = top_left[0] + (box_width - text_width) // 2
                text_y = top_left[1] + (box_height + text_height) // 2

                # Replace "LEFT" dynamically with other directions when needed
                cv2.putText(image, "LEFT", (text_x, text_y), cv2.FONT_HERSHEY_TRIPLEX, font_scale, (255,255,0), thickness)
                # cv2.rectangle(image, (100, 300), (200, 425), (255, 255, 255), cv2.FILLED)
                # cv2.putText(image, text, (100, 375), cv2.FONT_HERSHEY_SIMPLEX,
                #             2, (0, 0, 255), 5)
                KeyOn(left_key_pressed)
                break_pressed=True
                current_key_pressed.add(left_key_pressed)
                key_pressed=left_key_pressed
                keyPressed = True
                key_count=key_count+1
                #pyautogui.press("left")
            elif total==5 and text=="Left":
                # Get frame dimensions
                h, w, c = image.shape  

                # Define box dimensions and position (top-right corner)
                box_width, box_height = 250, 100  
                top_left = (w - box_width - 20, 20)  # 20 pixels padding from the right and top
                bottom_right = (w - 20, 20 + box_height)

                # Draw black rectangle at the top-right corner
                cv2.rectangle(image, top_left, bottom_right, (0, 0, 0), cv2.FILLED)

                # Center text inside the box
                font_scale = 2
                thickness = 5
                (text_width, text_height), baseline = cv2.getTextSize("LEFT", cv2.FONT_HERSHEY_TRIPLEX, font_scale, thickness)

                text_x = top_left[0] + (box_width - text_width) // 2
                text_y = top_left[1] + (box_height + text_height) // 2

                # Replace "LEFT" dynamically with other directions when needed
                cv2.putText(image, "RIGHT", (text_x, text_y), cv2.FONT_HERSHEY_TRIPLEX, font_scale, (255, 182, 193), thickness)
                # cv2.rectangle(image, (100, 300), (200, 425), (255, 255, 255), cv2.FILLED)
                # cv2.putText(image, text, (100, 375), cv2.FONT_HERSHEY_SIMPLEX,
                #             2, (0, 0, 255), 5)

                KeyOn(right_key_pressed)
                key_pressed=right_key_pressed
                accelerator_pressed=True
                keyPressed = True
                current_key_pressed.add(right_key_pressed)
                key_count=key_count+1
                #pyautogui.press("right")

            elif total==1:
                # Get frame dimensions
                h, w, c = image.shape  

                # Define box dimensions and position (top-right corner)
                box_width, box_height = 250, 100  
                top_left = (w - box_width - 20, 20)  # 20 pixels padding from the right and top
                bottom_right = (w - 20, 20 + box_height)

                # Draw black rectangle at the top-right corner
                cv2.rectangle(image, top_left, bottom_right, (0, 0, 0), cv2.FILLED)

                # Center text inside the box
                font_scale = 2
                thickness = 5
                (text_width, text_height), baseline = cv2.getTextSize("LEFT", cv2.FONT_HERSHEY_TRIPLEX, font_scale, thickness)

                text_x = top_left[0] + (box_width - text_width) // 2
                text_y = top_left[1] + (box_height + text_height) // 2

                # Replace "LEFT" dynamically with other directions when needed
                cv2.putText(image, "UP", (text_x, text_y), cv2.FONT_HERSHEY_TRIPLEX, font_scale, (255,255,255), thickness)

                KeyOn(up_key_pressed)
                key_pressed=up_key_pressed
                jump_pressed=True
                keyPressed = True
                current_key_pressed.add(up_key_pressed)
                key_count=key_count+1
            elif total==0:
                # Get frame dimensions
                h, w, c = image.shape  

                # Define box dimensions and position (top-right corner)
                box_width, box_height = 250, 100  
                top_left = (w - box_width - 20, 20)  # 20 pixels padding from the right and top
                bottom_right = (w - 20, 20 + box_height)

                # Draw black rectangle at the top-right corner
                cv2.rectangle(image, top_left, bottom_right, (0, 0, 0), cv2.FILLED)

                # Center text inside the box
                font_scale = 2
                thickness = 5
                (text_width, text_height), baseline = cv2.getTextSize("LEFT", cv2.FONT_HERSHEY_TRIPLEX, font_scale, thickness)

                text_x = top_left[0] + (box_width - text_width) // 2
                text_y = top_left[1] + (box_height + text_height) // 2

                # Replace "LEFT" dynamically with other directions when needed
                cv2.putText(image, "Down", (text_x, text_y), cv2.FONT_HERSHEY_TRIPLEX, font_scale, (0,255,255), thickness)

                KeyOn(down_key_pressed)
                key_pressed=down_key_pressed
                down_pressed=True
                keyPressed = True
                current_key_pressed.add(down_key_pressed)
                key_count=key_count+1

        if not keyPressed and len(current_key_pressed) != 0:
            for key in current_key_pressed:
                KeyOff(key)
            current_key_pressed = set()
        elif key_count==1 and len(current_key_pressed)==2:    
            for key in current_key_pressed:             
                if key_pressed!=key:
                    KeyOff(key)
            current_key_pressed = set()
            for key in current_key_pressed:
                KeyOff(key)
            current_key_pressed = set()


            # if lmList[8][2] < lmList[6][2]:
            #     print("Open")
            # else:
            #     print("Close")
        cv2.imshow("Frame",image)
        k=cv2.waitKey(1)
        if k == ord('q'):
            break
video.release()
cv2.destroyAllWindows()

