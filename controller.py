#!/usr/bin/env python

# based on tutorials:
#   http://www.roman10.net/serial-port-communication-in-python/
#   http://www.brettdangerfield.com/post/raspberrypi_tempature_monitor_project/

#from serial import Serial
import serial
import time




SERIALPORT = "/dev/ttyUSB0"
BAUDRATE = 9600 

ser = serial.Serial(SERIALPORT, BAUDRATE)

ser.bytesize = serial.EIGHTBITS #number of bits per bytes

ser.parity = serial.PARITY_NONE #set parity check: no parity

ser.stopbits = serial.STOPBITS_ONE #number of stop bits

ser.timeout = None          #block read

#ser.timeout = 0             #non-block read

#ser.timeout = 3              #timeout block read

ser.xonxoff = False     #disable software flow control

ser.rtscts = False     #disable hardware (RTS/CTS) flow control

ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control

ser.writeTimeout = 0     #timeout for write

print('Starting Up Serial Monitor')

try:
    ser.open()

except Exception as e:
    print "error open serial port: " + str(e)
    ser.close()
    ser.open()

if ser.isOpen():

    time.sleep(5)

    try:
        ser.flushInput() #flush input buffer, discarding all its contents
        ser.flushOutput()#flush output buffer, aborting current output
        
        oldData = ""


        while True:
            f = open("command", 'r')
            data = f.readline()

            if(data != oldData):
                ser.write(data + "\r\n")
                oldData = data
            
            f.close()

            time.sleep(5)
            
        ser.close()

    except Exception, e:
        print "error communicating...: " + str(e)

else:
    print "cannot open serial port "
