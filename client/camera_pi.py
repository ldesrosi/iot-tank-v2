import time
import io
import threading
import picamera
import picamera.array
import cv2
import numpy
import pantiltmanager

class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera

    # side face pattern detection
    profileface = cv2.CascadeClassifier("./haarcascade_profileface.xml")		

    # frontal face pattern detection
    frontalface = cv2.CascadeClassifier("./lbpcascade_frontalface.xml")		
    
    face = [0,0,0,0]
    Cface = [0,0]
    lastface = 0

    width = 320
    height = 240
    
    panTiltManager = pantiltmanager.PanTiltManager()

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _searchForFaces(cls, image):
        faceFound = False

        if not faceFound:
            if cls.lastface == 0 or cls.lastface ==1:
               fface = cls.frontalface.detectMultiScale(image, 1.1, 2, 0, (60,60))
               if fface != ():		# if we found a frontal face...
                    cls.lastface = 1	# set lastface 1 (so next loop we will only look for a frontface)
                    for f in fface:	# f in fface is an array with a rectangle representing a face
                        faceFound = True
                        cls.face = f

        if not faceFound:				
            if cls.lastface == 0 or cls.lastface == 2:	
                pfacer = cls.profileface.detectMultiScale(image, 1.3, 4,          
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
            if cls.lastface == 0 or cls.lastface == 3:	
                flipImage = True         
                cv2.flip(image,1,image)	# flip the image
                pfacel = cls.profileface.detectMultiScale(image, 1.3, 4, 
                                   (cv2.cv.CV_HAAR_DO_CANNY_PRUNING + 
                                    cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT + 
                                    cv2.cv.CV_HAAR_DO_ROUGH_SEARCH), (80,80))
                if pfacel != ():
                    cls.lastface = 3
                    for f in pfacel:
                        faceFound = True
                        cls.face = f

        if not faceFound:		# if no face was found...-
            cls.lastface = 0		# 	the next loop needs to know
            cls.face = [0,0,0,0]	# so that it doesn't think the face is still where it was last loop

        x,y,w,h = cls.face
        
        if cls.lastface == 3:
            # we are given an x,y corner point and a width and height, we need the center
            cls.Cface = [(w/2+(cls.width-x-w)),(h/2+y)]	
        else:
            # we are given an x,y corner point and a width and height, we need the center
            cls.Cface = [(w/2+x),(h/2+y)]
        
        cv2.cv.Rectangle(cv2.cv.fromarray(image), (x,y), (x+w, y+h), cv2.cv.RGB(255, 0, 0), 3, 8, 0)
        if (flipImage):
           cv2.flip(image,1,image) # flip back the image to preserve original orientation
        return image

    @classmethod
    def _panTilt(cls):
       x,y,w,h = cls.face
       tolerance = 20 
 
       if (x == 0 and y == 0 and w == 0 and h == 0):
           return

       # Coordinate of the center of the face
       x = x + (w/2)
       delta = int(cls.width/2) - x
       if (abs(delta) > tolerance):
          panX = cls.panTiltManager.panPosition
          if (delta < 0):
             panX -= 5
          else:
             panX += 5
          cls.panTiltManager.panTo(panX)
      
       y = y + (h/2)
       delta = int(cls.height/2) - y
       if (abs(delta) > tolerance):
          tiltY = cls.panTiltManager.tiltPosition
          if (delta < 0):
             tiltY += 5
          else:
             tiltY -= 5
          cls.panTiltManager.tiltTo(tiltY)

 
       #cls.panTiltManager.tiltTo(turn_y)

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (320, 240)
            camera.hflip = True
            camera.vflip = True
            
            rawCapture = picamera.array.PiRGBArray(camera, size=(320, 240))
            # let camera warm up
            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for frame in camera.capture_continuous(rawCapture, 'bgr',
                                                 use_video_port=True):
                image = numpy.copy(frame.array)
                image = cls._searchForFaces(image)
                
                #Recenter the face 
                cls._panTilt()
           
                stream.write(cv2.imencode('.jpg', image)[1]) 
                
                # store frame
                stream.seek(0)
                cls.frame = stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

                rawCapture.truncate(0)

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None
