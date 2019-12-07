## Author: Kasin Sparks
## Date: 04 DEC 2019
## Objective: A list item to display data with a delete button.

from tkinter import *

class ListItem(Frame):

    def __init__(self, master=None, text="", callback=None, indexOffset=-1):
        Frame.__init__(self, master)

        self.text = text
        self._callback = callback
        self.indexOffset = indexOffset #The offset in the list, if -1 not currently in the list... hopefully

        self.grid()
        self.createWidgets()

    def createWidgets(self):
        # Data text
        self._label = Label(self, text=self.text)
        self._label.grid(column=1, row=0)

        # Trash button
        if self._callback is None:
            self._deleteButton = Button(self, bitmap="error")
        else:
            self._deleteButton = Button(self, bitmap="error", command=self._callback)
        
        self._deleteButton.grid(column=0, row = 0)
