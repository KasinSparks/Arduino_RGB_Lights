from tkinter import *

class ListItem(Frame):

    def __init__(self, master=None, text=""):
        Frame.__init__(self, master)

        self._text = text

        self.grid()
        self.createWidgets()

    def createWidgets(self):
        # Data text
        self._label = Label(self, text=self._text)
        self._label.grid(column=1, row=0)

        # Trash button
        self._deleteButton = Button(self, bitmap="error")
        self._deleteButton.grid(column=0, row = 0)

    def setText(self, text):
        self._text = text