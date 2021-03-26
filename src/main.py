from tkinter import Tk
from tkinter import Button
from tkinter import Frame
from tkinter import Label
from tkinter import Menu
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

from tkinter import END
from tkinter import INSERT
from cv2 import error

from pyzbar import pyzbar

# Local lib
from src.gui import GUI
from src.callback import Callback
from src.camera import Camera
from src.util import convert2geometry
from src.parser import Parser

class Main:
    def __init__(self, path=""):
        self.configpath = path
        self.root = Tk()
        self.cameras = Camera()
        self.parser = Parser()
        self.gui = GUI(root=self.root)
        self.callback = Callback(self.root)

        self.isImage_active = False
        self.isVideo_active = False
        self.isCamera_active = False
        self.isObject_active = False
        
    #---------- Local callback ----------#
    def openwithimage_callback(self, event=None):
        if self.gui.panel != None:
            self.gui.destroyPanel()
        path = self.callback.openwithimage_callback()
        if path != None:
            self.cameras.readImage(path, flag=None)
            self.cameras.frame = self.cameras.resize(self.cameras.getFrame, (400, 400))
            width, height = self.cameras.getSize()
            image = self.cameras.convert2tk(self.cameras.getFrame)
            self.gui.createPanel(image, width=width, height=height)
            self.isImage_active = True
            self.isVideo_active = False
            self.isCamera_active = False
        
    def openwithvideo_callback(self, event=None):
        if self.gui.panel != None:
            self.gui.destroyPanel()
        path = self.callback.openwithvideo_callback(event=event)
        if path != None:
            self.cameras.startVideo(path)
            startCapture = self.cameras.readCapture()
            startCapture = self.cameras.BGR2RGBA(startCapture)
            startCapture = self.cameras.convert2tk(startCapture)
            width, height = self.cameras.getSize()
            self.gui.createPanel(startCapture, width=width, height=height)
            self.captureVideo(loop=True)
            self.isImage_active = False
            self.isVideo_active = True
            self.isCamera_active = False

    def openwithcamera_callback(self, event=None):
        if self.gui.panel != None:
            self.gui.destroyPanel()
        settings = self.parser.parseCameraSettings()
        src = settings["src"]
        try:
            self.cameras.startVideo(src=src)
            startCapture = self.cameras.readCapture()
            startCapture = self.cameras.BGR2RGB(startCapture)
            startCapture = self.cameras.convert2tk(startCapture)
            width, height = self.cameras.getSize()
            self.gui.createPanel(startCapture, width=width, height=height)
            self.captureVideo(loop=False)
            self.isImage_active = False
            self.isVideo_active = False
            self.isCamera_active = True
        except error:
            self.gui.message("Failed to open camera with device " + str(src), 2)
            # self.gui.destroyPanel()

    def detectBarcode_callback(self, event=None):
        self.isObject_active = True
        if self.isObject_active:
            if self.cameras.getFrame is None:
                self.gui.message("No object")
            else:
                if self.isCamera_active is None:
                    newframe = self.detectBarcode()
                    newframe = self.cameras.convert2tk(newframe)
                    self.gui.update(newframe)
                
    #---------- Edit menu ----------#
    def clearframe_callback(self, event=None):
        self.callback.clearframe_callback(self.gui)

    #---------- Capture Video ----------#
    def captureVideo(self, loop=False):
        
        try:
            captured = self.cameras.readCapture(islopp=loop, gui=self.gui)
        
            captured = self.cameras.BGR2RGB(captured)
            self.cameras.frame = captured
            if captured is None:
                pass
            else:
                if self.isObject_active:
                    frame = self.detectBarcode(customFrame=self.cameras.getFrame)
                    if frame is None:
                        frame = self.cameras.getFrame
                else:
                    frame = self.cameras.getFrame
                newframe = self.cameras.convert2tk(frame)
                self.gui.update(newframe)
            self.gui.delay(15, self.captureVideo)
        except error:
            self.gui.message("Asserting failed, please check your camera!")
            self.gui.destroyPanel()

    #---------- Detect barcode ----------#
    def detectBarcode(self, customFrame=None):
        if customFrame is None:
            customFrame = self.cameras.getFrame

        image = self.cameras.BGR2Gray(self.cameras.getFrame)
        barcode = pyzbar.decode(image)
        if len(barcode) == 0: return None
        for data in barcode:
            points = data.polygon
            x, y, w, h = data.rect
            pts = self.cameras.cv2array(points)
            pts = pts.reshape((-1, 1, 2))
            newframe = self.cameras.createpolygon(self.cameras.frame, pts)
            code = data.data.decode("utf-8")
            newframe = self.cameras.setText(newframe, text=code, position=(x,y))
            return newframe

    #---------- Setup menbubars function ----------#
    def setupMenubars(self):
        menubars = Menu(self.root)

        #---------- File bars ----------#
        fileBars = Menu(menubars, tearoff=0)
        menubars.add_cascade(label="File", menu=fileBars)
        fileBars.add_command(label="Open with image file", command=self.openwithimage_callback)
        fileBars.add_command(label="Open with video file", command=self.openwithvideo_callback)
        fileBars.add_command(label="Open with camera", command=self.openwithcamera_callback)
        fileBars.add_separator()
        fileBars.add_command(label="Save barcode", command=print)
        fileBars.add_separator()
        fileBars.add_command(label="Quit", command=self.callback.quit_callback)
        #---------- CTRL + O (Open with image file) ----------#
        self.root.bind("<Control-o>", self.openwithimage_callback)
        self.root.bind("<Control-O>", self.openwithimage_callback)
        #---------- CTRL + Shift + O (Open with video file) ----------#
        self.root.bind("<Control-Shift-o>", self.openwithvideo_callback)
        self.root.bind("<Control-Shift-O>", self.openwithvideo_callback)
        #---------- CTRL + Q (Quit) ----------#
        self.root.bind("<Control-Q>", self.callback.quit_callback)
        self.root.bind("<Control-q>", self.callback.quit_callback)

        #---------- Edit bars ----------#
        editbars = Menu(menubars, tearoff=0)
        menubars.add_cascade(label="Edit", menu=editbars)
        editbars.add_command(label="Clear frame", command=self.clearframe_callback)
        editbars.add_command(label="Detect barcode", command=self.detectBarcode_callback)
        #---------- CTRL + Shift + C (Clear Frame) ----------#
        self.root.bind("<Control-Shift-c>", self.clearframe_callback)
        self.root.bind("<Control-Shift-C>", self.clearframe_callback)

        #---------- Settings bar ----------
        settingbars = Menu(menubars, tearoff=0)
        menubars.add_cascade(label="Settings", menu=settingbars)
        settingbars.add_command(label="Settings camera", command=self.callback.setCameraDevice_callback)
        

        self.root.config(menu=menubars)

    #---------- Setup function ----------#
    def setup(self):
        callback = [self.openwithimage_callback, self.openwithvideo_callback, self.openwithcamera_callback, self.clearframe_callback, self.detectBarcode_callback]
        w, h = self.gui.getWindowSize() # get window size
        self.gui.setTitle("QrScanner")
        self.gui.setScreensize(size=convert2geometry(w=w, h=h))
        self.setupMenubars()
        self.gui.createButton(command=callback)

    def run(self):
        self.root.mainloop()