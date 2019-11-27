## Manages the controller process by reading commands
## such as {STOP, RESTART, START} from file

from ProcessCommandEnum import ProcessCommandEnum
from ProcessManagerAgent import ProcessManagerAgent
import time, sys, signal, traceback

def main():
    oldCommand = ""
    # Create an agent
    agent = ProcessManagerAgent()
    try:
        while(True):
            # Open the file for reading
            file = open("../config/processctl", "r")

            # Read the command and check it for vaild command
            command = file.readline()
            file.close()

            if command == oldCommand:
                time.sleep(1)
                continue
            else:
                oldCommand = command

            commandVal = agent.vailidateCommand(command)
            if commandVal.value < 0:
                if not(command is None or command == ""):
                    print("Error processing processctl command: " + str(command))
                    continue

            # Handle the request
            agent.handler(commandVal)

            time.sleep(2) 
    finally:
        # Close any spwaned processes then this process
        print("Closing processes")
        agent.handler(ProcessCommandEnum.STOP)
        exit()

def sigterm_handler(_signo, _stackframe):
    print("SIGTERM Recived... Trying to exit gracefully")
    sys.exit()

    


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)
    print("ProcessManager started")
    main() 