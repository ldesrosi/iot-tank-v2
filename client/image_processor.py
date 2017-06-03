import cv2
import io
import numpy
import time

from PIL import Image, ImageDraw

class FaceProcessor(object):

    def __init__(self):
        # side face pattern detection
        self.profileface = cv2.CascadeClassifier("./opencv/haarcascade_profileface.xml")

        # frontal face pattern detection
        #self.frontalface = cv2.CascadeClassifier("./opencv/lbpcascade_frontalface.xml")
        self.frontalface = cv2.CascadeClassifier("./opencv/haarcascade_frontalface_alt2.xml")

        self.face = [0,0,0,0]
        self.lastface = 0

    def process(self, image, x=0, y=0, w=0, h=0):
        #Convert PIL Image to numpy array
        open_cv_image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2GRAY)

        #open_cv_image = cv2.equalizeHist(open_cv_image)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        open_cv_image = clahe.apply(open_cv_image)

        faceFound = False

        if self.lastface == 0 or self.lastface == 1:
           fface = self.frontalface.detectMultiScale(
               open_cv_image, 
               scaleFactor=1.5, 
               minNeighbors=1,
               minSize=(10,10),
               flags = cv2.cv.CV_HAAR_SCALE_IMAGE)

           if fface != ():		# if we found a frontal face...
               faceFound = True
               self.lastface = 1	# set lastface 1 (so next loop we will only look for a frontface)
               self.face = fface[0]

        if not faceFound:
            if self.lastface == 0 or self.lastface == 2:
                pfacer = self.profileface.detectMultiScale(
                             open_cv_image,
                             scaleFactor=1.3,
                             minNeighbors=4,
                             minSize=(80,80),
                             flags=(cv2.cv.CV_HAAR_DO_CANNY_PRUNING +
                                    cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT +
                                    cv2.cv.CV_HAAR_DO_ROUGH_SEARCH))
                if pfacer != ():		# if we found a profile face...
                    faceFound = True
                    self.lastface = 2
                    self.face = pface[0]

        flipImage = False
        if not faceFound:			# a final attempt
            if self.lastface == 0 or self.lastface == 3:
                flipImage = True
                cv2.flip(open_cv_image,1,open_cv_image)	# flip the image
                pfacel = self.profileface.detectMultiScale(
                             open_cv_image,
                             scaleFactor=1.3,
                             minNeighbors=4,
                             minSize=(80,80),
                             flags=(cv2.cv.CV_HAAR_DO_CANNY_PRUNING +
                                    cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT +
                                    cv2.cv.CV_HAAR_DO_ROUGH_SEARCH))

                if pfacel != ():
                    faceFound = True
                    self.lastface = 3
                    self.face = pfacel[0]

        if not faceFound:		# if no face was found...-
            self.lastface = 0		# 	the next loop needs to know
            self.face = [0,0,0,0]	# so that it doesn't think the face is still where it was last loop

        x,y,w,h = self.face

        drawContext = ImageDraw.Draw(image)
        drawContext.rectangle([x, y, x+w, y+h], fill=None, outline=(255,0,0,0))

        return (image, x, y, w, h)
