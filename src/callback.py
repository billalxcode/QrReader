from tkinter.filedialog import askopenfilename

# Local lib
from src.parser import Parser
from src.util import getBasename
from src.gui import GUI, SettingsCameraWindow

class Callback:
    def __init__(self, root):
        self.root = root
        self.gui = GUI(self.root)
        self.parser = Parser()
        self.extensions = self.parser.parseExtensions()
        self.path = ""
        
        
    def getPath(self):
        return self.path

    #---------- File callback ----------
    def openwithimage_callback(self, event=None):
        filetypes = self.extensions["image"]
        openfile = askopenfilename(filetypes=filetypes)
        if openfile != "" and len(openfile) >= 1:
            basename = getBasename(openfile)
            for extension in self.extensions["image"]:
                if extension[1] == "*": continue
                else:
                    ext = extension[1].replace("*", "")
                    if basename[1] == ext:
                        return openfile
            if self.path == "":
                GUI().message("Unable extension", type=0)
                return None
            else:
                return openfile
        else:
            GUI().message("Failed to open file", type=2)
            return None
            

    def openwithvideo_callback(self, event=None):
        filetypes = self.extensions["video"]
        openfile = askopenfilename(filetypes=filetypes)
        if openfile != "" and len(openfile) >= 1:
            basename = getBasename(openfile)
            for extension in self.extensions["video"]:
                if extension[1] == "*": continue
                else:
                    ext = extension[1].replace("*", "")
                    if basename[1] == ext:
                        return openfile
            if self.path == "":
                GUI().message("Unable extension", type=0)
                return None
            else:
                return openfile
        else:
            GUI().message("Failed to open file", type=2)
            return None

    def quit_callback(self, event=None):
        self.root.destroy()

    #---------- Edit callback ----------#
    def clearframe_callback(self, gui):
        gui.destroyPanel()

    def setCameraDevice_callback(self, event=None):
        settingsWindow = SettingsCameraWindow()
        settingsWindow.setup()
        settingsWindow.setBind()
        settingsWindow.createButton()
        settingsWindow.createCheckButton()
        settingsWindow.main()