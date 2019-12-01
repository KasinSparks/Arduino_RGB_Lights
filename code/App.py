from tkinter import *
from ModeEnum import Mode
#from SerialHelper import SerialHelper
#from SerialHelper import SerialHelper
import SerialHelper
import Views.StaticView

import Views.CustomWidgets.Silder
from ColorEnum import Color

from functools import partial

from Views.CommandPanel import CommandPanel

import os, signal

menuBackgroundColor = "#262e30"
menuForegroundColor = "#e5e4c5"
menuActiveForegroundColor = menuForegroundColor 
menuActiveBackgroundColor = "#464743"

mainBackgroundColor = "#1b2122"

class App(Frame):

    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.mode = Mode.Static
        self.ser = SerialHelper.SerialHelper()

        self.test = Views.StaticView.StaticView(self)
        self.sliderRed = Views.CustomWidgets.Silder.Silder(self, "Red", color=Color.RED)
        self.sliderGreen = Views.CustomWidgets.Silder.Silder(self, "Green", color=Color.GREEN)
        self.sliderBlue = Views.CustomWidgets.Silder.Silder(self, "Blue", color=Color.BLUE)


        self.grid()
        self.createWidgets()
        # Restart the RGB controller
        f = open("../config/processctl", "w")
        f.write("start")
        f.close()
    
    def createWidgets(self):
        self.quitButton= Button(self, text="Quit", command=self.quit)
        self.quitButton.grid()

        self.my_label = Label(self, text="My Label!")
        self.my_label.grid()

        self.connectedLabel = Label(self, text="Not Connected", foreground='red')
        self.connectedLabel.grid()

        self.test.grid()
        
        self.tempText = Label(self, text="NONE")
        self.tempText.grid()

        self.addButton = Button(self, text="Add", command=self.addValues)
        self.addButton.grid()

        # test
        self.sliderRed.grid(column=0, row=0)
        self.sliderGreen.grid(column=1, row=0)
        self.sliderBlue.grid(column=2, row=0)

        self.delayAreaFrame = Frame(self)
        self.delayAreaFrame.grid(column=3, row=0)

        self.delayValLabel = Label(self.delayAreaFrame, text="Fade Value:")
        self.delayValLabel.grid(column=0, row=0)
        self.delayVal = Entry(self.delayAreaFrame)
        self.delayVal.grid(column=0, row=1)

        self.cPanel = CommandPanel()
        self.cPanel.grid(column=4,row = 0)
        

        self.my_menu = Menu(self,
                            tearoff=0,
                            activebackground=menuActiveBackgroundColor,
                            background=menuBackgroundColor,
                            activeforeground=menuActiveForegroundColor, 
                            foreground=menuForegroundColor
                            )


        #self.fileMenu = Menu(self.my_menu)
        #self.fileMenu.add_command(label="Exit", command=self.quit)


        self.my_menu.add_cascade(label="File", menu=self.fileMenu(self.my_menu))
        self.my_menu.add_cascade(label="Ports", menu=self.portsMenu(self.my_menu))
        self.my_menu.add_cascade(label="Mode", menu=self.modeMenu(self.my_menu))

    def fileMenu(self, mainMenu):
        fileMenu = Menu(mainMenu,
                        tearoff=0,
                        activebackground=menuActiveBackgroundColor,
                        background=menuBackgroundColor,
                        activeforeground=menuActiveForegroundColor, 
                        foreground=menuForegroundColor
                        )
        fileMenu.add_command(label="Exit", command=self.quit)
        return fileMenu

    def portsMenu(self, mainMenu):
        portsMenu = Menu(mainMenu,
                        tearoff=0,
                        activebackground=menuActiveBackgroundColor,
                        background=menuBackgroundColor,
                        activeforeground=menuActiveForegroundColor, 
                        foreground=menuForegroundColor
                        )
        
        for sp in SerialHelper.getSerialPorts():
            # Have this be a call to the function and supply the serial port as the arg
            functionCall = partial(self.selectPort, sp[0], self.connectedLabel) 
            portsMenu.add_command(label=sp, command=functionCall)
        return portsMenu 


    def selectPort(self, port, uiElement):
        color = 'red'
        text = 'Failed'

        if self.ser.connect(port):
            text = 'Connected on ' + port
            color = 'green'
            f = open("../config/port", "w")
            f.write(port)
            f.close()

            # Restart the RGB controller
            f = open("../config/processctl", "w")
            f.write("restart")
            f.close()


        uiElement['foreground'] = color 
        uiElement['text'] = text 

    def modeMenu(self, mainMenu):
        menu = Menu(mainMenu,
                    tearoff=0,
                    activebackground=menuActiveBackgroundColor,
                    background=menuBackgroundColor,
                    activeforeground=menuActiveForegroundColor,
                    foreground=menuForegroundColor
                    )

        for m in Mode:
            funcCall = partial(self.changeMode, m)
            menu.add_command(label=m, command=funcCall)

        return menu

    def changeMode(self, mode):
        print("Mode changed from: "+ (str) (self.mode) + " to: " + (str) (mode))
        self.mode = mode

    def parseDelayValue(self):
        delayValStr = self.delayVal.get()

        try:
            value = int(delayValStr)
            if value < 1 or value > 255:
                print("Delay value out of byte range")
                return 1
        except ValueError as err:
            print(err)
            return 1

        return value        


    def addValues(self):
        tempString = self.paddNum(self.sliderRed.getValue()) + ',' + self.paddNum(self.sliderGreen.getValue()) + ',' + self.paddNum(self.sliderBlue.getValue()) + ',' + self.paddNum(self.parseDelayValue()) + ';'
        self.tempText['text'] = tempString
        self.writeToFile(file="../config/command", text=tempString + '\n')

    def paddNum(self, num=0):
        if num > 255:
            print("Fade number > 255. Defaulting to 000")
            return "000"
        
        paddedZeros = ""

        # Generate the correct number of padding zeros
        if num < 100:
            paddedZeros += '0'
        if num < 10:
            paddedZeros += '0'

        # Pad the number
        paddedZeros += str(num)

        return paddedZeros


    def writeToFile(self, file=None, fileArgs='a', text=None):
        if file is None:
            print("No file to write to...")
            return
        
        f = open(file, fileArgs)
        f.write(text)

        



#from SerialHelper import getSerialPorts 
#for sp in getSerialPorts():
#    print(sp)

# Start the app up!
app = App()
app.master.title("RGB Lights 3000")
app.master.config(menu=app.my_menu, background=mainBackgroundColor)

#subprocess.call(["./controller.py", "/dev/ttyUSB0"])

# Start up the app and the process manager
pid = os.fork()

if pid:
    # parent
    app.mainloop()
    os.kill(pid, signal.SIGTERM)
else:
    # child
    exec(open("./ProcessManager.py").read())

#os.system("controller.py")

#app.mainloop()
#print("here")