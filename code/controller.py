#!/usr/bin/env python

#from serial import Serial
import serial
import time
import sys

from SerialHelper import SerialHelper

isLoopingEnabled = False 


def main():

    portFile = open("../config/port", "r")
    currentPort = str(portFile.readline())
    portFile.close()

    # Serial connection
    sc = SerialHelper()

    sc.connect(port=currentPort)

    if sc.isOpen():

        time.sleep(2)

        try:
            sc.flushInputAndOutput()

            oldData = [] 

            while True:
                portFile = open("../config/port", "r")
                tempPort = str(portFile.readline())
                if currentPort != tempPort:
                    currentPort = tempPort
                portFile.close()

                f = open("../config/command", 'r')
                data = f.readlines()


                if not(len(oldData) == len(data)):
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
                                sc.close()
                                exit()

                        print("Data in buffer: " + str(data[i]))
                        sc.write(str.encode(data[i]))
                        #oldData = data.copy()
                        print("Writing data: " + data[i])

                        line = ""
                        while(True):
                            line = sc.readline()
                            
                            print("I have read: " + line.decode("utf-8"))
                            if("DONE" in line.decode("utf-8")):
                                break
                    
                oldData = list(data)

                f.close()

                if(not isLoopingEnabled):
                    time.sleep(2)
                
            sc.close()

        except Exception as e:
            print("error communicating...: " + str(e))
    else:
        print("cannot open serial port ")


if __name__ == "__main__":
    print('Starting Up Serial Monitor')
    main()