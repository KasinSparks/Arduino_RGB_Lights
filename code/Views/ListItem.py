## Author: Kasin Sparks
## Date: 04 DEC 2019
## Objective: A list item to display data with a delete button.

from tkinter import *

class ListItem(Frame):

    def __init__(self, master=None, text=""):
        Frame.__init__(self, master)

        self._master = master

        self.text = text
        
        #self.bind("<Button-1>", self._test)

        self.grid()
        self.createWidgets()

    def createWidgets(self):
        # Data text
        self._label = Label(self, text=self.text)
        self._label.grid(column=1, row=0)


        self._label.bind("<Button-1>", self._test)

    def _test(self, event):
        # Change the previous selected item to being unselected
        if self._master._selectedItem is not None:
            self._master._selectedItem._label['bg'] = '#FFFFFF'

        if self._master._selectedItem is not self:
            self._label['bg'] = '#0000FF'
            self._master._selectedItem = self
        else:
            self._master._selectedItem = None