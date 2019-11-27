import os, signal
from ProcessCommandEnum import ProcessCommandEnum

class ProcessManagerAgent():

    def __init__(self):
        self.childPid = -1



    def handler(self, commandVal):
        if commandVal == ProcessCommandEnum.START:
            # Start the process
            self.startProcess() 

        elif commandVal == ProcessCommandEnum.STOP:
            # Stop the process
            self.stopProcess() 
        
        elif commandVal == ProcessCommandEnum.RESTART:
            self.stopProcess()
            self.startProcess()


    def startProcess(self):
        if self.checkIfHasChild():
            print("A child process is already running")
            return
            
        pid = os.fork()
        if pid:
            #parent 
            self.childPid = pid
            print(pid)
            os.waitpid(pid, os.WNOHANG)
        else:
            # child
            print("Starting controller.py")
            os.execlp("python3", "python3", "controller.py")
            print("Code should not of reached here! ERROR!!!")


    def stopProcess(self):
        if not self.checkIfHasChild():
            print("No child process to stop!")
            return

        print("Stoping process with pid: " + str(self.childPid))
        os.kill(self.childPid, signal.SIGTERM)
        os.wait()
        self.childPid = -1
            


    def checkIfHasChild(self):
        if self.childPid > 0:
            return True 
        
        return False 
    
    
    ## Retruns a list of all of the possible commands. Will be useful for later
    def getAllPossibleCommands(self):
        return [c.name for c in ProcessCommandEnum]
        
    # Return the custom process command number or -1 for error
    def vailidateCommand(self, command):
        for c in ProcessCommandEnum:
            if str.upper(command).strip('\n') == str.upper(c.name):
                return c
        
        return -1