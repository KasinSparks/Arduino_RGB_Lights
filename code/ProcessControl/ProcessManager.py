## Author: Kasin Sparks
## Date: 04 DEC 2019
## Manages the controller process by reading commands
# such as {STOP, RESTART, START} from file processctl

from ProcessControl.ProcessCommandEnum import ProcessCommandEnum
from ProcessControl.ProcessManagerAgent import ProcessManagerAgent
import time, sys, signal, os, traceback

mainDirectory = os.path.join(os.getcwd(), "..")
processctlFile = os.path.join(mainDirectory, "config", "processctl") 

def main():
    # Create as many agents as need for unique processes
    agents = {} 
    # Create an agent
    agents['controller.py'] = ProcessManagerAgent(os.path.join(mainDirectory, "code", "controller.py"))

    try:
        while(True):
            # Check for existance
            try:
                # Open the file for reading
                file = open(processctlFile, "r")
            except FileNotFoundError:
                print("Could not find file required at path: " + str(processctlFile))

            # Read the command(s) and check it for vaild command
            commands = file.readlines()
            file.close()

            # Try to process the commands and distribute command to respective agent
            for c in commands:
                if c == "" or c is None:
                    time.sleep(1)
                    continue
                
                try:
                    # Commands should have the form processName,value
                    commandSplit = c.split(",")

                    # Ignore the processes in the 'handled' state
                    if str.upper(commandSplit[1]).split('\n')[0] == 'HANDLED':
                        time.sleep(1)
                        continue

                    # Check for key in dict
                    if not commandSplit[0] in agents:
                        print("Command key: " + str(commandSplit[0]) + " not found in agents...")
                        continue
                    
                    # Try handle the request
                    commandVal = agents[commandSplit[0]].vailidateCommand(commandSplit[1])

                    if commandVal.value < 0:
                        print("Error processing processctl command: " + str(c))
                        continue

                    # Handle the request
                    agents[commandSplit[0]].handler(commandVal)

                    file = open(processctlFile, "w")
                    for line in commands:
                        if line.split(',')[0] == commandSplit[0]:
                            file.write(commandSplit[0] + ",HANDLED\n")
                        else:
                            file.write(line)
                    
                    file.close()

                except Exception as ex:
                    print(ex)
                    print(str(ex.with_traceback()))


            time.sleep(1) 
    finally:
        # Close any spwaned processes then this process
        print("Closing processes")
        for a in agents.values():
            a.handler(ProcessCommandEnum.STOP)
        #traceback.print_tb()
        exit()

def sigterm_handler(_signo, _stackframe):
    print("SIGTERM Recived... Trying to exit gracefully")
    sys.exit()

    


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)
    print("ProcessManager started")
    main() 


# Used to send start, stop, and restart commands
def sendCommand(processName, command):
    # Check for file existance
    try:
        file = open(processctlFile, 'r')
        lines = file.readlines()
        file.close()
    except FileNotFoundError:
        print("File: " + str(processctlFile) + " does not exist. Could not send command.")
        return -1

    # Check to see if process exist in file. If exist, replace, else create
    file = open(processctlFile, 'w')

    # Handle edge case where the file is empty
    if len(lines) == 0:
        file.write(processName + "," + str(command.name) + '\n')
    else:
        for line in lines:
            if line.split(',')[0] == processName:
                # Match
                file.write(processName + "," + str(command.name) + '\n')
            else:
                # Write data back to file
                file.write(line)

    file.close()

    return 1

