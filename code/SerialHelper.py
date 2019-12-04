## Author: Kasin Sparks
## Date: 04 DEC 2019
## Objective: Create a class to interface with the arduino via serial communication.

import serial
import serial.tools.list_ports
import time

class SerialHelper():
    def __init__(self):
        self.bradrate = 9600
        self.ser = serial.Serial(None, self.bradrate)
        self.ser.bytesize = serial.EIGHTBITS #number of bits per bytes
        self.ser.parity = serial.PARITY_NONE #set parity check: no parity
        self.ser.stopbits = serial.STOPBITS_ONE #number of stop bits
        self.ser.timeout = None          #block read
        self.ser.xonxoff = False     #disable software flow control
        self.ser.rtscts = False     #disable hardware (RTS/CTS) flow control
        self.ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
        self.ser.writeTimeout = 0     #timeout for write

    # Connect to a serial port.  1 <= n < 6 will inversly 
    # determine the number of times serial connection will try to connect to port
    def connect(self, port, n=1):
        self.ser.port = port
        # Try to open then connection
        try:
            print("Connecting to " + port)
            self.ser.open()

            if self.ser.isOpen():
                # Give time for Arduino to start up
                time.sleep(2)  
                print("Connection successful")
            else:
                print("Unable to connect...")
        except Exception as e:
            print("An error occured while opening serial port: " + str(e))

            # Try to connect 5 times
            if n > 5:
                return False
            print("Closing then retrying... " + str(n))
            self.ser.close()
            self.connect(port, n + 1) 

        # Was able to connect
        return True

    # Close the connection
    def close(self):
        self.ser.close()

    # Read from the serial port 
    def read(self):
        return self.ser.read()

    # Read the lines from the serial port
    # Returns a list of the lines 
    def readline(self):
        return self.ser.readline()

    # Write the the serial port buffer
    def write(self, s):
        self.ser.write(s)

    # Remove all data in the buffer for the serial port
    def flushInputAndOutput(self):
        self.flushInput()
        self.flushOutput()

    # Only remove the data in the buffer for the input
    def flushInput(self):
        self.ser.flushInput()

    # Only remove the data in the output buffer
    def flushOutput(self):
        self.ser.flushOutput()

    # Test if the serial connect is open
    def isOpen(self):
        return self.ser.isOpen()

# Returns a list of the available serial ports
def getSerialPorts():
    return serial.tools.list_ports.comports()