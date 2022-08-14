import cv2
import numpy as np


dogruluk = 0.7
image = cv2.imread(r"C:\Users\emre\PycharmProjects\findsign\sources\speed.png")

levhatemp = cv2.imread(r"C:\Users\emre\PycharmProjects\findsign\sources\70temp.jpg")
levhatemp = cv2.cvtColor(levhatemp, cv2.COLOR_BGR2GRAY)


hsvimage = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

lower_red = np.array([0,70,50])
upper_red = np.array([170,70,50])


mask1 = cv2.inRange(hsvimage, (0, 70, 50), (10, 255, 255))
mask2 = cv2.inRange(hsvimage, (170, 70, 50), (180, 255, 255))
mask = cv2.bitwise_or(mask1, mask2)

masked = cv2.bitwise_and(hsvimage, hsvimage, mask=mask)

masked_gry = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
masked_gry = cv2.medianBlur(masked_gry,5)
canny_edge = cv2.Canny(masked_gry, 50, 240)

circles = cv2.HoughCircles(canny_edge,cv2.HOUGH_GRADIENT,0.5,50,param1=50,param2=30,minRadius=0,maxRadius=0)

if circles is not None:
    circles = np.uint16(np.around(circles))

    wt, ht = levhatemp.shape[::-1]

    for (x,y,r) in circles[0,:]:
        cv2.circle(image, (x, y), r, (0, 255, 0), 2)


cv2.imshow("result",image)
cv2.imshow("canny",canny_edge)
cv2.imshow("image",masked)

cv2.waitKey(0)