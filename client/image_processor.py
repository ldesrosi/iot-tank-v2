import cv2
import io
import numpy
import time

from PIL import Image

class FaceProcessor(object):

    # side face pattern detection
    profileface = cv2.CascadeClassifier("./haarcascade_profileface.xml")

    # frontal face pattern detection
    frontalface = cv2.CascadeClassifier("./lbpcascade_frontalface.xml")

    face = [0,0,0,0]
    Cface = [0,0]
    lastface = 0

    def process(self, image, x=0, y=0, w=0, h=0):
        #Convert PIL Image to numpy array
        open_cv_image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)

        faceFound = False

        if not faceFound:
            if self.lastface == 0 or self.lastface ==1:
               fface = self.frontalface.detectMultiScale(open_cv_image, 1.1, 2, 0, (60,60))
               if fface != ():		# if we found a frontal face...
                    self.lastface = 1	# set lastface 1 (so next loop we will only look for a frontface)
                    for f in fface:	# f in fface is an array with a rectangle representing a face
                        faceFound = True
                        self.face = f

        if not faceFound:
            if self.lastface == 0 or self.lastface == 2:
                pfacer = self.profileface.detectMultiScale(open_cv_image, 1.3, 4,
                                   (cv2.cv.CV_HAAR_DO_CANNY_PRUNING +
                                    cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT +
                                    cv2.cv.CV_HAAR_DO_ROUGH_SEARCH), (80,80))
                if pfacer != ():		# if we found a profile face...
                    lastface = 2
                    for f in pfacer:
                        faceFound = True
                        face = f

        flipImage = False
        if not faceFound:			# a final attempt
            if self.lastface == 0 or self.lastface == 3:
                flipImage = True
                cv2.flip(open_cv_image,1,open_cv_image)	# flip the image
                pfacel = self.profileface.detectMultiScale(open_cv_image, 1.3, 4,
                                   (cv2.cv.CV_HAAR_DO_CANNY_PRUNING +
                                    cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT +
                                    cv2.cv.CV_HAAR_DO_ROUGH_SEARCH), (80,80))
                if pfacel != ():
                    self.lastface = 3
                    for f in pfacel:
                        faceFound = True
                        self.face = f

        if not faceFound:		# if no face was found...-
            self.lastface = 0		# 	the next loop needs to know
            self.face = [0,0,0,0]	# so that it doesn't think the face is still where it was last loop


        x,y,w,h = self.face

        if self.lastface == 3:
            # we are given an x,y corner point and a width and height, we need the center
            self.Cface = [(w/2+(self.width-x-w)),(h/2+y)]
        else:
            # we are given an x,y corner point and a width and height, we need the center
            self.Cface = [(w/2+x),(h/2+y)]

        cv2.cv.Rectangle(cv2.cv.fromarray(open_cv_image), (x,y), (x+w, y+h), cv2.cv.RGB(255, 0, 0), 3, 8, 0)
        if (flipImage):
           cv2.flip(open_cv_image,1,open_cv_image) # flip back the image to preserve original orientation

        image = Image.fromarray(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))

        return (image, x, y, w, h)
