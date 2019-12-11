## Author: Kasin Sparks
## Date: 04 DEC 2019
## Objective: A list item to display data with a delete button.

from tkinter import *

class ListItem(Frame):

    def __init__(self, master=None, text=""):
        Frame.__init__(self, master)

        self.text = text

        self.grid()
        self.createWidgets()

    def createWidgets(self):
        # Data text
        self._label = Label(self, text=self.text)
        self._label.grid(column=1, row=0)
