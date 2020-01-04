import cv2
import numpy as np
import math
import serial

ard = serial.Serial('/dev/ttyACM0', 9600)

#bgSubtractor = cv2.createBackgroundSubtractorMOG2()
#withoutBg = bgSubtractor.apply(grayFrame)
cap = cv2.VideoCapture(0)

faceCascade = cv2.CascadeClassifier("head.xml")

_, firstFrame = cap.read()
firstFrameGray = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
firstFrameBlurrred = cv2.GaussianBlur(firstFrameGray, (5, 5), 0)

# mask1 = [[[0 for k in range(3)] for j in range(len(firstFrame[i]))] for i in range(len(firstFrame))]
# for y in range(len(mask1)): #max saturation
#     for x in range(len(mask1[y])):
#         mask1[y][x][1] = 255

mask1 = np.zeros_like(firstFrame)
# Sets image saturation to maximum
mask1[..., 1] = 255

def largestContour(contours):
    maxIndex = 0
    maxSize = 0
    for i in range(len(contours)):
        maxContour = contours[i]
        size = cv2.contourArea(maxContour)
        if size > maxSize:
            maxSize = size
            maxIndex = i
    return contours[maxIndex]

while (True):
    _, frame = cap.read()
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurredFrame = cv2.GaussianBlur(grayFrame, (5, 5), 0)
    difference = cv2.absdiff(firstFrameBlurrred, blurredFrame)
    _, difference = cv2.threshold(difference, 50, 255, cv2.THRESH_BINARY)

    kernal = np.ones((4, 4), np.uint8)
    mask = cv2.morphologyEx(difference, cv2.MORPH_OPEN, kernal, iterations=2)
    mask = cv2.morphologyEx(difference, cv2.MORPH_CLOSE, kernal, iterations=2)
    final = cv2.bitwise_and(frame, frame, mask=mask)

    final_gray = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(final_gray, scaleFactor=1.1, minNeighbors=5, flags=cv2.CASCADE_SCALE_IMAGE)
    widthes = [w*h for count, (x, y, w, h) in enumerate(faces)]
    try:
        index = np.argmax(widthes)
        (x, y, w, h) = faces[index]
        cv2.rectangle(final, (x, y), (x+w, y+h), (255, 255, 255), 3)
        frame[y:y+h+100, x:x+w+100] = firstFrame[y:y+h+100, x:x+w+100]
        ard.write('Y'.encode())


    except:
        ard.write('N'.encode())
        pass

    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("grayFrame", final_gray)
    count = 0
    contours, hierarchy = cv2.findContours(final_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        maxContour = largestContour(contours)
        cv2.drawContours(final, maxContour, -1, (0,255,0), 3)
        hull = cv2.convexHull(maxContour,returnPoints = False)
        hullPoints = cv2.convexHull(maxContour,returnPoints = True)
        defects = cv2.convexityDefects(maxContour,hull)
        # contours = קווי מתאר
        # convexity defect = area (cavity) between the convex hull and the object itself (its contours)
        # the defect is the furthest point from the vertices of the hull that is still on the contours

        # תמונה אחת שווה אלף מילים
        #https://i.stack.imgur.com/EBlnT.png
        cv2.drawContours(frame, [hullPoints], -1, (0, 255, 0), 3)
        if type(defects) is not type(None):
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(maxContour[s][0])
                end = tuple(maxContour[e][0])
                far = tuple(maxContour[f][0])
                #cv2.line(frame,start,end,(0,255,0),2)
                cv2.circle(frame,far,5,(0,0,255),-1)
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                # we create a triangle from the 2 vertices on the hull and the convexity defect
                # we find the angle of the triangle (the angle between 2 fingers) using
                # משפט הקוסינוסים
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))

                if angle < math.pi/2:
                    count = count + 1
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    bottomLeftCornerOfText = (far[0]+20, far[1]+20)
                    fontScale = 0.7
                    fontColor = (255,255,255)
                    lineType = 2

                    cv2.putText(frame,str(int(angle*180/math.pi)),
                        bottomLeftCornerOfText,
                        font,
                        fontScale,
                        fontColor,
                        lineType)

    ard.write(str(count).encode())


    #flow = cv2.calcOpticalFlowFarneback(firstFrameGray, final_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    #magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])

    # for y in range(len(mask1)):
    #     for x in range(len(mask1[y])):
    #         mask1[y][x][0] = angle * 180 / np.pi / 2 #hue by angle of vector
    #         mask1[y][x][2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX) #value normalize magnitude

    #mask1[..., 0] = angle * 180 / np.pi / 2
    #mask1[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)

    #cv2.cvtColor(mask1, cv2.COLOR_HSV2BGR)


    #final = cv2.flip(final, 1)
    frame = cv2.flip(frame, 1)
    #cv2.imshow("final", final)
    cv2.imshow("frame", frame)
    #cv2.imshow("mask", mask1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
