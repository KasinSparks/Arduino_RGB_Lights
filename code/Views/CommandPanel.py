## Author: Kasin Sparks
## Date: 04 DEC 2019
## Objective: Have a dynamic panel in the GUI that shows the user a given 
### amount of RGB commands.

## TODO: Test class

from tkinter import *

from Views.ListItem import ListItem

from functools import partial

import random, math

import os

class CommandPanel(Frame):

    def __init__(self, master=None, numOfViewableItems = 10):
        Frame.__init__(self, master)
        
        # Command file location
        self._commandFile = os.path.join('config', 'command')

        # Staticly type _items to a list of ListItems
        self._items: List[ListItem] = []

        self._currentPosition = 0
        self._numOfViewableItems = numOfViewableItems

        # Trash buttons
        self._trashButtons = []

        self._selectedItem = None

        self.grid()
        self.createWidgets()

    # Insert the existing commands into the panel
    def createWidgets(self):
        ## TODO
        
        # Create trash buttons
        for i in range(self._numOfViewableItems):
            functionCall = partial(self.removeItem, i)
            self._trashButtons.append(Button(self, bitmap="error", command=functionCall))


        # Load data from file
        self.load()

        # Save button
        self._saveButton = Button(self, text="SAVE", command=self.save)
        self._saveButton.grid(column=0, row=(self._numOfViewableItems))

        # Page up/down buttons
        self._pageButtons = {"Page Down": Button(self, text="Page Down", command=partial(self._pageButtonsCommand, 1)), 
                        "Page Up": Button(self, text="Page Up", command=partial(self._pageButtonsCommand, -1))}
        self._pageButtons["Page Up"].grid(column=2, row=0)
        self._pageButtons["Page Down"].grid(column=2, row=self._numOfViewableItems-1)

        # Single inc. buttons
        self._incButtons = {"Down": Button(self, text="Scroll Down", command=partial(self._scrollButtonsCommand, 1)),
                            "Up": Button(self, text="Scroll Up", command=partial(self._scrollButtonsCommand, -1))}
        self._incButtons["Up"].grid(column=2, row=1)
        self._incButtons["Down"].grid(column=2, row=self._numOfViewableItems-2)


    # Move the list a page down
    def _pageButtonsCommand(self, direction=1):
        # Page the list in the direction given
        gotoPos = self._currentPosition + (self._numOfViewableItems * direction) 

        scrollResult = self._scroll(gotoPos)

        if scrollResult > 0:        
            # Over shot the target
            gotoPos = len(self._items) - self._numOfViewableItems
        elif scrollResult < 0:
            # Under shot the target
            gotoPos = 0
        
        self._currentPosition = gotoPos
        self.updateList()


    # Move the list up/down an item
    def _scrollButtonsCommand(self, direction=1):
        # Move the list by one in direction given
        gotoPos = self._currentPosition + direction

        # Already at end of list or already at beginning of list
        if self._scroll(gotoPos) != 0:
            return 

        self._currentPosition = gotoPos
        self.updateList()

    # Returns -1 for under, 0 for within range, 1 for over shot target
    def _scroll(self, gotoPos):
        # Check bounds
        if gotoPos > len(self._items) - self._numOfViewableItems:
            # Over shot the target
            return 1
        elif gotoPos < 0:
            # Under shot the target
            return -1
        
        return 0


    # Update the list. If the index is in range of current showing, update. 
    ## If no index is specified, update current showing.
    def updateList(self, index=None):
        if index is None or self._isInShowingRange(index):
            # Update list
            showingRange = self._getShowingRange()

            ## Remove the items
            for i in range(len(self._items)):
                self._items[i].grid_remove()


            # Remove the trash buttons
            for i in range(self._numOfViewableItems):
                self._trashButtons[i].grid_remove()


            ## Add the items back
            for i in range(showingRange[0], showingRange[1]):
                self._items[i].grid(column=1, row=(i - showingRange[0]))

                # Add the trash buttons
                functionCall = partial(self.removeItem, i)
                self._trashButtons[i - showingRange[0]]['command'] = functionCall
                self._trashButtons[i - showingRange[0]].grid(column=0, row=(i - showingRange[0]))

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

        # Update list after change
        self.updateList()


    def removeItem(self, index):
        # Remove the item from the list
        if len(self._items) > 0 and index > -1 and index < len(self._items):
            print("Index: " + str(index))

            # Remove the trash button
            if len(self._items) < self._numOfViewableItems:
                ## Make sure this is before the item get poped out of the list,
                ## unless the index will be one too negative
                self._trashButtons[len(self._items) - 1].grid_remove()
            
            # Remove the listItem
            self._items.pop(index).grid_remove()
            
            # Update list after change
            self.updateList()
        else:
            print("Invaild index... No item was removed.")

    

    # Save what is in the _items list to the file
    def save(self):
        # Save to the command file
        try:
            f = open(self._commandFile, 'w')
        except FileNotFoundError:
            print("File was not found. Could not save Commnads.")
            return

        try:
            print("Saving commands...")
            for i in self._items:
                f.write(str(i.text))
                # If it is the last item in the list, don't write the newline after command
                if i != (self._items[len(self._items) - 1]):
                    f.write('\n')

            print("Done.")
        finally:
            f.close()


    # Load all the command in the command file to the _items list
    def load(self):
        # Load the commands from the file
        try:
            f = open(self._commandFile, 'r')
        except:
            print("File not found. Commands were not loaded.")
            return

        try:
            print("Loading commands...")
            for i in f:
                # Add the command line without the new line
                self.addItem(i.split('\n')[0])
            
            print("Done.")
        finally:
            f.close()


    # Return the index of a ListItem
    def getListItemIndex(self, listItem):
        if listItem is None:
            print("Could not find index... No ListItem object provided.")
            return

        # Find item in the list O(n)
        for i in range(len(self._items)):
            if listItem is self._items[i]:
                return i

    
    # Return a random index
    def getRandomIndex(self):
        return random.randint(0, len(self._items))