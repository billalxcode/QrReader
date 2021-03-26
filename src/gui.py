# QrCode Reader
# Develop by Billal Fauzan (billal.xcode@gmail.com)

from tkinter import Button
from tkinter import Label
from tkinter import Frame
from tkinter import Canvas
from tkinter import Toplevel
from tkinter import Checkbutton

from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from tkinter.messagebox import showwarning

from tkinter import NW
from tkinter import CENTER
from tkinter import IntVar

# Local lib
from src.util import convert2geometry

class GUI:
    def __init__(self, root=None):
        self.root = root
        self.framebox = Frame(self.root)
        self.framebox.grid(row=0, column=0)
        self.frame = None
        self.panel = None

    #---------- Update frame ----------#
    def update(self, newframe):
        if self.panel is None:
            GUI().message("Failed to update frame, check your panel", 3)
        else:
            self.frame = newframe
            self.panel.create_image(30.0, 0, image=self.frame, anchor=NW)

    #---------- Delay ----------#
    def delay(self, time, function):
        if self.panel is None:
            GUI().message("Failed to update frame, check your panel", 3)
        else:
            self.root.after(time, function)

    #---------- Get resolution size ----------#
    def getWindowSize(self):
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        return w, h

    #---------- Set window title ----------#
    def setTitle(self, title):
        self.root.title(title)

    #---------- Set window size ----------#
    def setScreensize(self, size=""):
        self.root.geometry(size)

    #---------- Messagebox function ----------#
    def message(self, msg, type=0):
        if type == 0:
            showwarning("WARNING!", message=msg)
        elif type == 1:
            showinfo("INFO!", msg)
        elif type == 2:
            showerror("ERROR!", msg)
        else:
            pass

    #---------- Create button ----------#
    def createButton(self, command=[]):
        Button(self.framebox, text="Image", command=command[0]).grid(row=1, column=0, pady=10, padx=10)
        Button(self.framebox, text="Video", command=command[1]).grid(row=1, column=1, pady=10, padx=10)
        Button(self.framebox, text="Camera", command=command[2]).grid(row=1, column=2, pady=10, padx=10)
        Button(self.framebox, text="Clear frame", command=command[3]).grid(row=1, column=3, pady=10, padx=10)
        Button(self.framebox, text="Detect barcode", command=command[4]).grid(row=1, column=4, pady=10, padx=10)

    #---------- Create panel ----------#
    def createPanel(self, frame=None, width=0, height=0):
        self.frame = frame
        if self.frame is None:
            GUI().message("Frame is None, please insert a frame")
        else:
            if width == 0:
                width = 200
            elif height == 0:
                height = 200
            self.panel = Canvas(self.root, width=width, height=height)
            self.panel.create_image(30.0, 0, image=self.frame, anchor=NW)
            self.panel.grid(row=2, column=0)

    #---------- Destroy panel ----------#
    def destroyPanel(self):
        if self.panel is None:
            self.message("Panel not found", 2)
        else:
            self.panel.grid_forget()

class SettingsCameraWindow:
    def __init__(self):
        self.root = Toplevel()
        self.checkbutton1 = IntVar()

    def getScreenSize(self):
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        return w, h

    def getWindowSize(self):
        w = self.root.winfo_screenmmwidth()
        h = self.root.winfo_screenmmheight()
        return w, h

    def setTitle(self):
        self.root.title("Settings Camera")

    def setBind(self):
        #---------- CTRL + Q (Quit) ----------#
        self.root.bind("<Control-q>", self.quit_callback)
        self.root.bind("<Control-Q>", self.quit_callback)

    def setup(self):
        width, height = self.getScreenSize()
        width = int(width/2-100)
        height = int(height/2-100)

        screensize = convert2geometry(width, height)

        self.root.geometry(screensize)
        self.setTitle()

    #---------- Destroy ----------#
    def quit_callback(self, event=None):
        self.root.destroy()

    def isChecked_callback(self):
        print (self.checkbutton1.get())

    def createButton(self):
        Label(self.root, text="Is URL: ", width=6).grid(row=1, column=0)

    def createCheckButton(self):
        Checkbutton(self.root, text="Is URL", variable=self.checkbutton1, command=self.isChecked_callback, onvalue=1, offvalue=0).pack()

    def main(self):
        self.root.mainloop()