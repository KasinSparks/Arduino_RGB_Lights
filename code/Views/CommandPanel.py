## Author: Kasin Sparks
## Date: 04 DEC 2019
## Objective: Have a dynamic panel in the GUI that shows the user a given 
### amount of RGB commands.

## TODO: Test class

from tkinter import *

from Views.ListItem import ListItem

class CommandPanel(Frame):

    def __init__(self, master=None, numOfViewableItems = 10):
        Frame.__init__(self, master)
        
        # Staticly type _items to a list of ListItems
        self._items: List[ListItem] = []

        self._currentPosition = 0
        self._numOfViewableItems = numOfViewableItems

        self.grid()
        self.createWidgets()

    # Insert the existing commands into the panel
    def createWidgets(self):
        ## TODO

        #self._items.insert(0, ListItem(self, "TEst0", self.removeItem))
        self._items.append(ListItem(self, "TEST0"))
        self._items.append(ListItem(self, "TEST1"))
        #self._items.insert(0, ListItem(self, "TEst1"))

        self.updateList()
        #for i in self._items:
        #    i.grid()

        #self.insert(END, ListItem(self, "This is a test0", self.removeItem))
        #self.insert(END, ListItem(self, "This is a test1"))
        #self.insert(END, ListItem(self, "This is a test2"))

    # Update the list. If the index is in range of current showing, update. 
    ## If no index is specified, update current showing.
    def updateList(self, index=None):
        if index is None or self._isInShowingRange(index):
            # Update list
            showingRange = self._getShowingRange()

            ## Remove the items
            for i in self._items:
                i.indexOffset = -1
                i.grid_remove()

            ## Add the items back
            for i in range(showingRange[0], showingRange[1]):
                self._items[i].grid()
                self._items[i].indexOffset = i
        
        return


    # Check to see if the index is in the list's current showing
    def _isInShowingRange(self, index):
        # See if the viewable items in the list need to be updated
        _range = self._getShowingRange()
        if index in range(_range[0], _range[1]):
            return True

        return False

    # Calculate the list's showing range. Returns tuple with (start, end)
    def _getShowingRange(self):
        # Determine range
        if len(self._items) < self._currentPosition + self._numOfViewableItems:
            endRange = len(self._items)
        else:
            endRange = self._currentPosition + self._numOfViewableItems

        # Return a tuple with (start, end) range        
        return (self._currentPosition, endRange)

    # Add an command (item) to the command list. If 0 > index < len(list) then item will
    ## get appended to the list.
    def addItem(self, text="", index=-1):
        if text is None or text == "":
            print("ERROR: No list item was given to add...")
            return

        # Check for integer index
        try: 
            if index < 0 or index >= len(self._items):
                # Append to end
                self._items.append(ListItem(self, text=text))
            else:
                # Insert at given position
                self._items.insert(index, ListItem(self, text=text))
        except ValueError:
            print("ERROR: index value was not an integer. Item was not added.")
            return 

        self.updateList(index)


    def removeItem(self, index=0):
        #print(self.size())
        #self.delete(0,END)
        #self.update_idletasks()
        # Remove the item from the view
        #self._items[index].grid_remove()
        # Remove the item from the list
        self._items.pop(index=index)
        self.updateList(index)
        #print(self.size())
        ## TODO: remove an item
        ## TODO: File IO

    def save(self):
        # TODO:
        pass

    def _fileIO(self):
        ## TODO: File IO
        pass
