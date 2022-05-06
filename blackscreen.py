import cv2
import time
import numpy as np


fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi', fourcc, 20.0, (480, 640))


cap = cv2.VideoCapture(0)


time.sleep(2)
bg = 0


for i in range(60):
    ret, bg = cap.read()

bg = np.flip(bg, axis=1)


while (cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
   
    img = np.flip(img, axis=1)

    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

 
    lower_black = np.array([0, 120, 50])
    upper_black = np.array([10, 255,255])
    black_1 = cv2.inRange(hsv, lower_black, upper_black)

    lower_black = np.array([170, 120, 70])
    upper_black = np.array([180, 255, 255])
    black_2 = cv2.inRange(hsv, lower_black, upper_black)

    black_1 = black_1 + black_2


    black_1 = cv2.morphologyEx(black_1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    black_1 = cv2.morphologyEx(black_1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    black_2 = cv2.bitwise_not(black_1)

    res_1 = cv2.bitwise_and(img, img, black=black_2)

    res_2 = cv2.bitwise_and(bg, bg, black=black_1)

    
    final_output = cv2.addWeighted(res_1, 1, res_2, 1, 0)
    output_file.write(final_output)
    
    cv2.imshow("BlackScreen", final_output)
    cv2.waitKey(1)
