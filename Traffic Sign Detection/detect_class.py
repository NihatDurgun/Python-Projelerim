import cv2
import numpy as np
from skimage.measure import compare_ssim
from threading import Thread

bestmatch=0
bestx=0
besty=0
bestr=0
finded_signname=""
signnames= ["20","30","40","50","60","nostop","noentry","norightturn","noleftturn","nouturn"]


class sign_control(Thread):
    def __init__(self,bestx,besty,bestr,signname,bestmatch,sign,levhatemp,x, y, r):
        Thread.__init__(self)
        self.sign = sign
        self.levhatemp = levhatemp
        self.x = x
        self.y = y
        self.r = r
        self.bestx = bestx
        self.besty = besty
        self.bestr = bestr
        self.signname = signname
        self.bestmatch = bestmatch


    def run(self):
        self.sign_width, self.sign_height, self.sign_channel = self.sign.shape
        self.score = 0
        if (self.sign_width > 32 and self.sign_height > 32):
            self.levhatemp_resized = cv2.resize(self.levhatemp, (self.sign_width, self.sign_height))
            self.levhatemp_canny = cv2.Canny(self.levhatemp_resized, 20, 150)
            if (self.levhatemp_resized.shape == self.sign.shape):
                self.result = cv2.matchTemplate(self.sign, self.levhatemp_resized, cv2.TM_CCOEFF_NORMED)
                (self.score2, self.diff2) = compare_ssim(self.sign, self.levhatemp_resized, full=True, multichannel=True)
                (_, self.score1, _, self.maxLoc) = cv2.minMaxLoc(self.result)
                self.score = self.score1 + self.score2
            if (self.bestmatch < self.score):
                self.bestmatch = self.score
                self.bestx = self.x
                self.besty = self.y
                self.bestr = self.r
                self.finded_signname = self.signname
                return (self.bestx, self.besty, self.bestr, self.finded_signname, self.bestmatch, 1)
        return (self.bestx, self.besty, self.bestr, "ssss", self.bestmatch, 0)



class sign_detection(Thread):
    def __init__(self, image,signnames):
        Thread.__init__(self)
        self.image = image
        self.bestx =0
        self.besty = 0
        self.bestr = 0
        self.finded_signname=""
        self.bestmatch = 0
        self.kontrol = 0

        self.signnames = signnames


    def run(self):
        self.__init__(self.image, self.signnames)
        self.blured_image = cv2.bilateralFilter(self.image, 9, 75, 75)
        self.hsvimage = cv2.cvtColor(self.blured_image, cv2.COLOR_BGR2HSV)

        self.mask1 = cv2.inRange(self.hsvimage, (0, 70, 50), (10, 255, 255))
        self.mask2 = cv2.inRange(self.hsvimage, (170, 70, 50), (180, 255, 255))
        self.mask = cv2.bitwise_or(self.mask1, self.mask2)

        self.masked = cv2.bitwise_and(self.hsvimage, self.hsvimage, mask=self.mask)

        self.masked_gry = cv2.cvtColor(self.masked, cv2.COLOR_BGR2GRAY)
        self.masked_gry = cv2.medianBlur(self.masked_gry, 5)
        self.blured_masked_gry = cv2.bilateralFilter(self.masked_gry, 9, 75, 75)
        self.canny_edge = cv2.Canny(self.blured_masked_gry, 400, 400)

        self.circles = cv2.HoughCircles(self.canny_edge, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=10, maxRadius=0)

        if self.circles is not None:
            self.circles = np.uint16(np.around(self.circles))

            for self.signname in self.signnames:
                self.levhatemp = cv2.imread(r"C:\Users\emre\PycharmProjects\findsign\sign\\" + self.signname + ".png")
                self.levhatemp_gry = cv2.cvtColor(self.levhatemp, cv2.COLOR_BGR2GRAY)
                self.wt, self.ht = self.levhatemp_gry.shape[::-1]

                for (self.x, self.y, self.r) in self.circles[0, :]:
                    self.sign = self.image[self.y - self.r:self.y + self.r, self.x - self.r:self.x + self.r]
                    self.sign_blured = cv2.bilateralFilter(self.sign, 9, 75, 75)
                    self.sign_canny = cv2.Canny(self.sign_blured, 20, 150)

                    if ((self.x + self.r) - (self.x - self.r) > 32 and (self.y + self.r) - (self.y - self.r) > 32 and self.sign is not None):
                        control_thread = sign_control(self.bestx, self.besty, self.bestr, self.signname, self.bestmatch,self.sign,self.levhatemp,self.x, self.y, self.r)
                        control_thread.start()
                        self.bestx, self.besty, self.bestr, self.finded_signname, self.bestmatch,self.kontrol = control_thread.run()
                        if(self.bestmatch > 0.6 and self.kontrol ==1 and self.finded_signname != "ssss"):
                            print(self.finded_signname+":"+str(self.bestmatch))
                            cv2.circle(self.image, (self.bestx, self.besty), self.bestr, (0, 255, 0), 2)
                            self.sign = self.image[self.besty - self.bestr:self.besty + self.bestr, self.bestx - self.bestr:self.bestx + self.bestr]

                            cv2.putText(self.image, self.finded_signname, (self.bestx - self.bestr, self.besty + self.bestr + 20), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 2, cv2.LINE_AA)
                            return self.image, self.sign, self.sign_canny, self.canny_edge, self.masked,self.finded_signname,0,1,self.bestmatch

        return self.image, None, None, None, None,self.finded_signname,1,0,self.bestmatch





image = cv2.imread(r"C:\Users\emre\PycharmProjects\findsign\sign\20.png")
detection_thread = sign_detection(image,signnames)
detection_thread.start()
kontrol = 0
while(kontrol == 0):
    image, sign, sign_canny, canny_edge, masked,finded_signname,kontrol,levhavar,bestmatch = detection_thread.run()

    if(levhavar ==  1):
        print("Levha" + finded_signname + ":" + str(bestmatch))
        cv2.imshow("result", image)
        f = open(r"C:\Users\emre\PycharmProjects\findsign\dataset\\" + finded_signname + "\count.txt", "r")
        count = f.read()
        f.close()
        cv2.imwrite(r"C:\Users\emre\PycharmProjects\findsign\dataset\\"+finded_signname+"\\"+count+".jpg",sign)
        f = open(r"C:\Users\emre\PycharmProjects\findsign\dataset\\" + finded_signname + "\count.txt","w")
        f.write(str(int(count)+1))
        cv2.imshow("sign",sign)
        f.close()