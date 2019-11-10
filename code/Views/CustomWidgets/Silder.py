## A custom silder

from tkinter import Frame, Canvas, Label
from ColorEnum import Color


class Silder(Frame):

    def __init__(self, master=None, text="", barWidth=20, barHeight=256, color=Color.RED):
        Frame.__init__(self, master)

        self.text = text
        self.barWidth = barWidth
        self.barHeight = barHeight
        self.dialPosition = 0
        self._color = color


        self.bar = Canvas(self, height=self.barHeight, width=self.barWidth, background='#00ff00')
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
        delta = event.y - self.dialPosition

        self.bar.move(self.dial, 0, delta)
        self.dialPosition += delta
        print(event.y)
        return

    def __generateColor(self, value):
        if value ==  
