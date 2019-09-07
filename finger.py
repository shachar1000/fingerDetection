import cv2
import numpy as np


bgSubtractor = cv2.createBackgroundSubtractorMOG2()
cap = cv2.VideoCapture(0)
while (True):
    ret, frame = cap.read()
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayFrame = cv2.GaussianBlur(frame, (5, 5), 0)
    withoutBg = bgSubtractor.apply(grayFrame)
    kernal = np.ones((4, 4), np.uint8)

    mask = cv2.morphologyEx(withoutBg, cv2.MORPH_OPEN, kernal, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernal, iterations=2)
    final = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("frame", final)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()


