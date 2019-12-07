## Author: Kasin Sparks
## Date: 04 DEC 2019
## Objective: A program to handle communication to the arduino.

import serial
import time
import sys

from SerialHelper import SerialHelper

isLoopingEnabled = False 


def main():

    # Get the port specified in the file
    portFile = open("../config/port", "r")
    currentPort = str(portFile.readline())
    portFile.close()

    # Serial connection
    sc = SerialHelper()

    sc.connect(port=currentPort)

    # Check if the connection was opened
    if sc.isOpen():
        # Try to communicate with the ardiuno
        try:
            sc.flushInputAndOutput()

            oldData = [] 

            # Connect to port specified in file and read data in file
            while True:
                # Check to see if port has changed
                portFile = open("../config/port", "r")
                tempPort = str(portFile.readline())
                if currentPort != tempPort:
                    currentPort = tempPort
                portFile.close()

                # Read the commands in the file
                f = open("../config/command", 'r')
                data = f.readlines()

                # If the data in the file has changed clear out the old data
                ## with empty strings. The list length must be same for old data
                ## and data for comparision later
                if not(len(oldData) == len(data)):
                    for i in range(len(data)):
                        oldData.append("")

                # Iterate through the commands and execute the commands
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