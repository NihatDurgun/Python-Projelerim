import cv2
import numpy as np


dogruluk = 0.7
image = cv2.imread(r"C:\Users\emre\PycharmProjects\findsign\sources\speed.png")

levhatemp = cv2.imread(r"C:\Users\emre\PycharmProjects\findsign\sources\50temp.jpg")
levhatemp = cv2.cvtColor(levhatemp, cv2.COLOR_BGR2GRAY)


hsvimage = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

lower_red = np.array([0,70,50])
upper_red = np.array([170,70,50])


mask1 = cv2.inRange(hsvimage, (0, 70, 50), (10, 255, 255))
mask2 = cv2.inRange(hsvimage, (170, 70, 50), (180, 255, 255))
mask = cv2.bitwise_or(mask1, mask2)

maskedhsv = cv2.bitwise_and(hsvimage, hsvimage, mask=mask)
maskedimg = cv2.bitwise_and(image, image, mask=mask)
masked_gry = cv2.cvtColor(maskedhsv, cv2.COLOR_BGR2GRAY)
gry_blur = cv2.medianBlur(masked_gry,5)

circles = cv2.HoughCircles(gry_blur,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)


circles = np.uint16(np.around(circles))

wt, ht = levhatemp.shape[::-1]

for (x,y,r) in circles[0,:]:
    # draw the outer circle

    cv2.circle(image, (x, y), r, (0, 255, 0), 2)



    # Draw a rectangle around the matched region.

cv2.imshow("result",image)

cv2.imshow("image",maskedimg)
cv2.imshow("hsv image",maskedhsv)
cv2.waitKey(0)