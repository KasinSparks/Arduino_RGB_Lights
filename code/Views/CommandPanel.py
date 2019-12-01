from tkinter import *

from Views.ListItem import ListItem

class CommandPanel(Listbox):

    def __init__(self, master=None):
        Listbox.__init__(self, master)

        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.insert(END, ListItem(self, "This is a test0"))
        self.insert(END, ListItem(self, "This is a test1"))
        self.insert(END, ListItem(self, "This is a test2"))

    def updateList(self):
        pass

    def _addItem(self, index=END):
        pass

    def _removeItem(self):
        pass

    def _fileIO(self):
        pass
