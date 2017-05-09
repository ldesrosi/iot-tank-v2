import pantiltmanager

class ImageTracker(object):
    def __init__(self, panTiltManager, width=320, height=240):
        self.panTiltManager = panTiltManager
        self.width = width
        self.height = height

    def process(self, image, x=0, y=0, w=0, h=0):
       tolerance = 20

       if (w == 0 and h == 0):
           return (image, 0, 0, 0, 0)

       # Coordinate of the center of the face
       x = x + (w/2)
       delta = int(self.width/2) - x
       if (abs(delta) > tolerance):
          panX = self.panTiltManager.panPosition
          if (delta < 0):
             panX -= 5
          else:
             panX += 5
          self.panTiltManager.panTo(panX)

       y = y + (h/2)
       delta = int(self.height/2) - y
       if (abs(delta) > tolerance):
          tiltY = self.panTiltManager.tiltPosition
          if (delta < 0):
             tiltY += 5
          else:
             tiltY -= 5
          self.panTiltManager.tiltTo(tiltY)

       return (image, x, y, w, h)
