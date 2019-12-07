## Author: Kasin Sparks
## Date: 04 DEC 2019
## Objective: Have a dynamic panel in the GUI that shows the user all RGB commands.

from tkinter import *

from Views.ListItem import ListItem

class CommandPanel(Listbox):

    def __init__(self, master=None):
        Listbox.__init__(self, master)

        self.grid()
        self.createWidgets()

    # Insert the existing commands into the panel
    def createWidgets(self):
        ## TODO
        self.insert(END, ListItem(self, "This is a test0", self.removeItem))
        self.insert(END, ListItem(self, "This is a test1"))
        self.insert(END, ListItem(self, "This is a test2"))

    ## TODO: not sure if I will need this
    def updateList(self):
        pass

    # Add an command (item) to the command list
    def addItem(self, listItem, index=END):
        if listItem is None:
            print("ERROR: No list item was given to add...")
            return
        
        self.insert(index, listItem)
        ## TODO: File IO

    def removeItem(self, index=0):
        print(self.size())
        self.delete(0,END)
        self.update_idletasks()

        print("here")
        print(self.size())
        ## TODO: remove an item
        ## TODO: File IO

    def _fileIO(self):
        ## TODO: File IO
        pass
