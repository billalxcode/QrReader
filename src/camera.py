import numpy as np
from cv2 import VideoCapture
from cv2 import imread
from cv2 import imwrite
from cv2 import polylines
from cv2 import resize
from cv2 import putText
from cv2 import cvtColor

from PIL.ImageTk import PhotoImage
from PIL.Image import fromarray

# Other
from cv2 import COLOR_BGR2RGBA
from cv2 import COLOR_BGR2GRAY
from cv2 import COLOR_BGR2RGB
from cv2 import CAP_PROP_POS_FRAMES
from cv2 import FONT_HERSHEY_SIMPLEX

from src.gui import GUI

class Camera:
    def __init__(self):
        self.camera = None
        self.frame = None
        
    @property
    def getFrame(self):
        return self.frame

    #---------- Cv2tk ----------#
    def convert2tk(self, frame):
        return PhotoImage(fromarray(frame))

    #---------- Resize image ----------#
    def resize(self, frame, newsize):
        return resize(frame, newsize)

    #---------- Get size ----------#
    def getSize(self):
        width, height, layers = self.frame.shape
        return width, height

    def BGR2Gray(self, frame):
        return cvtColor(frame, COLOR_BGR2GRAY)

    def BGR2RGBA(self, frame):
        return cvtColor(frame, COLOR_BGR2RGBA)

    def BGR2RGB(self, frame):
        return cvtColor(frame, COLOR_BGR2RGB)

    #---------- Array numpy ----------#
    def cv2array(self, img, dtype=np.int32):
        return np.array(img, dtype=dtype)

    #---------- Set polygon ----------#
    def createpolygon(self, frame, pts, color=(0, 255, 0)):
        return polylines(frame, [pts], True, color, 2)

    #---------- Set text ----------#
    def setText(self, frame, text="", position=(0, 0), font=FONT_HERSHEY_SIMPLEX, color=(0, 255, 0)):
        return putText(frame, text, position, font, 1, color, 2)

    def readImage(self, path, flag=None):
        self.frame = imread(path, flag)

    def startVideo(self, src=0):
        self.camera = VideoCapture(src)

    def readCapture(self, islopp=False, gui=None):
        if self.camera is None:
            GUI().message("Failed to capture video, please start a capture", 1)
            return False
        else:
            ret, frame = self.camera.read()
            if ret:
                self.frame = frame
                return frame
            else:
                if islopp:
                    self.camera.set(CAP_PROP_POS_FRAMES, 0)
                    return True
                else:
                    if gui is None:
                        GUI().message("Camera has been stopped", 3)
                    else:
                        gui.message("Camera has been stopped", 3)
                        gui.panel.destroy()
                    return None