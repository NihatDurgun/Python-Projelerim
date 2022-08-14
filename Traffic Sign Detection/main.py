
import cv2
import numpy as np
from skimage.measure import compare_ssim



def scanner(bestx,besty,bestr,finded_signname,bestmatch):
    sign_width, sign_height, sign_channel = sign.shape
    score =0
    if(sign_width >32 and sign_height > 32):
        levhatemp_resized = cv2.resize(levhatemp, (sign_width, sign_height))
        levhatemp_canny = cv2.Canny(levhatemp_resized, 20, 150)
        if (levhatemp_resized.shape == sign.shape):
            result = cv2.matchTemplate(sign, levhatemp_resized, cv2.TM_CCOEFF_NORMED)
            (score2, diff2) = compare_ssim(sign, levhatemp_resized, full=True, multichannel=True)
            (_, score1, _, maxLoc) = cv2.minMaxLoc(result)
            score = score1 + score2
        if (bestmatch < score):
            bestmatch = score
            bestx = x
            besty = y
            bestr = r
            finded_signname = signname
            return (bestx, besty, bestr, finded_signname, bestmatch, 1)
        print("Match: " + signname + ":" + str(score))
    return (bestx, besty, bestr, finded_signname, bestmatch, 0)


bestmatch=0
bestx=0
besty=0
bestr=0
finded_signname=""
signnames= ["10","20","30","40","50","60","nostop","noentry","norightturn","noleftturn","nouturn"]

image = cv2.imread(r"C:\Users\emre\PycharmProjects\findsign\sources\deneme.jpg")

blured_image = cv2.bilateralFilter(image, 9, 75, 75)
hsvimage = cv2.cvtColor(blured_image,cv2.COLOR_BGR2HSV)





mask1 = cv2.inRange(hsvimage, (0, 70, 50), (10, 255, 255))
mask2 = cv2.inRange(hsvimage, (170, 70, 50), (180, 255, 255))
mask = cv2.bitwise_or(mask1, mask2)

masked = cv2.bitwise_and(hsvimage, hsvimage, mask=mask)

masked_gry = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
masked_gry = cv2.medianBlur(masked_gry,5)
blured_masked_gry = cv2.bilateralFilter(masked_gry, 9, 75, 75)
canny_edge = cv2.Canny(blured_masked_gry, 400, 400)

circles = cv2.HoughCircles(canny_edge,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=10,maxRadius=0)

if circles is not None:
    circles = np.uint16(np.around(circles))

    for signname in signnames:
        levhatemp = cv2.imread(r"C:\Users\emre\PycharmProjects\findsign\sign\\"+signname+".png")
        levhatemp_gry = cv2.cvtColor(levhatemp, cv2.COLOR_BGR2GRAY)
        wt, ht = levhatemp_gry.shape[::-1]

        for (x,y,r) in circles[0,:]:
            sign = image[y - r:y + r, x - r:x + r]
            sign_blured= cv2.bilateralFilter(sign, 9, 75, 75)
            sign_canny = cv2.Canny(sign_blured, 20, 150)


            if ((x + r) - (x - r) > 32 and (y + r) - (y - r) > 32 and sign is not None):
                bestx, besty, bestr, finded_signname, bestmatch , kontrol= scanner(bestx,besty,bestr,finded_signname,bestmatch)
                if (kontrol == 1 ):
                    print("Yeni bestmatch"+signname+":" +str(bestmatch))
    if(bestmatch > 0.3):
            cv2.circle(image, (bestx, besty), bestr, (0, 255, 0), 2)
            sign = image[besty - bestr:besty + bestr, bestx - bestr:bestx + bestr]

            cv2.putText(image, finded_signname, (bestx-bestr, besty+bestr+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)




cv2.imshow("result",image)
if(bestmatch > 0.3):
    cv2.imshow("sign",sign)
    print( "Bestmatch "+ finded_signname + ": " + str(bestmatch))
    cv2.imshow("sign canny", sign_canny)

cv2.imshow("canny",canny_edge)
cv2.imshow("image",masked)
cv2.waitKey(0)