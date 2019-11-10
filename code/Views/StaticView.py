## Static View
## Simple display of 4 dials to control RGB and Fade speed

from tkinter import *

class StaticView(Frame):

    def __init__(self,master=None):
        Frame.__init__(self, master)

        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.test_label = Label(self, text="tEST")
        self.test_label.grid()