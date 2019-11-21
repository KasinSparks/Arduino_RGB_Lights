## A custom silder

from tkinter import Frame, Canvas, Label
from ColorEnum import Color


class Silder(Frame):

    def __init__(self, master=None, text="", barWidth=20, barHeight=256, color=Color.RED, maxValue=255, minValue=0):
        Frame.__init__(self, master)

        self.text = text
        self.barWidth = barWidth
        self.barHeight = barHeight + 5
        self.dialPosition = 0
        self._color = color
        self._maxValue = maxValue
        self._minValue = minValue


        self.bar = Canvas(self, height=self.barHeight, width=self.barWidth, background=self.__generateColor(self._maxValue))
        self.dial = self.bar.create_rectangle(self.dialPosition,self.dialPosition,self.barWidth,5, fill='grey') 

        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.bar.grid()

        self.label = Label(self, text=self.text)
        self.label.grid()

        self.bar.bind("<Button-1>", self.__scrollBar)
        #self.bar.tag_bind(self.dial, "<Button-1>", self.__scrollBar)

    
    # Scrollbar event handler
    def __scrollBar(self, event):
        offset = 2
        ## Check bounds
        if event.y >= self._minValue + offset and event.y <= self._maxValue + offset:

            delta = event.y - self.dialPosition - offset 

            self.bar.move(self.dial, 0, delta)
            self.dialPosition += delta

            self.bar['background'] = self.__generateColor(self._maxValue - self.dialPosition)

        return

    def __generateColor(self, value):
        # Pad the string as needed
        print("Color hex: " + hex(value))
        color = "#"
        for i in range(0,self._color.value):
            color += "0"

        # Convert base ten value to two hex values
        temp = hex(value).split('x')[1]
        # Get rid of the '0x'
        if len(temp) < 2:
            temp = "0" + temp 
        color += temp 

       # Pad the string as needed 
        for i in range(len(color), 7):
            color += '0'
        
        return color
        