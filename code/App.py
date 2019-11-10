from tkinter import *
from ModeEnum import Mode
#from SerialHelper import SerialHelper
#from SerialHelper import SerialHelper
import SerialHelper
import Views.StaticView

import Views.CustomWidgets.Silder

from functools import partial

menuBackgroundColor = "#262e30"
menuForegroundColor = "#e5e4c5"
menuActiveForegroundColor = menuForegroundColor 
menuActiveBackgroundColor = "#464743"

class App(Frame):

    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.mode = Mode.Static
        self.ser = SerialHelper.SerialHelper()

        self.test = Views.StaticView.StaticView(self)
        self.test2 = Views.CustomWidgets.Silder.Silder(self, "TEST Slider")

        self.grid()
        self.createWidgets()
    
    def createWidgets(self):
        self.quitButton= Button(self, text="Quit", command=self.quit)
        self.quitButton.grid()

        self.my_label = Label(self, text="My Label!")
        self.my_label.grid()

        self.connectedLabel = Label(self, text="Not Connected", foreground='red')
        self.connectedLabel.grid()

        self.test.grid()

        # test
        self.test2.grid()


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



#from SerialHelper import getSerialPorts 
#for sp in getSerialPorts():
#    print(sp)

# Start the app up!
app = App()
app.master.title("RGB Lights 3000")
app.master.config(menu=app.my_menu)
app.mainloop()