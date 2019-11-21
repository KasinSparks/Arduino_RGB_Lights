#!/usr/bin/env python

#from serial import Serial
import serial
import time


isLoopingEnabled = False 

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
        
        oldData = [] 


        while True:
            f = open("../config/command", 'r')
            data = f.readlines()


            if len(oldData) == 0:
                for i in range(len(data)):
                    oldData.append("")

            for i in range(len(data)):
                if(data[i] != oldData[i] or isLoopingEnabled):
                    # Check for delay
                    if("DELAY" in data[i].upper()):
                        splitText = data[i].split()
                        try:
                            time.sleep((int)(splitText[1]))
                            continue
                        except:
                            print("Invalid command \'" + data[i] + "\' on line: " + i)
                            f.close()
                            ser.close()
                            exit()

                    ser.write(data[i] + "\r\n")
                    #oldData = data.copy()
                    print("Writing data: " + data[i])

                    line = ""
                    while(True):
                        line = ser.readline()
                        print("I have read: " + str(line))
                        if("DONE" in line):
                            break
                
            oldData = list(data)

            f.close()

            if(not isLoopingEnabled):
                time.sleep(5)
            
        ser.close()

    except Exception, e:
        print "error communicating...: " + str(e)

else:
    print "cannot open serial port "
