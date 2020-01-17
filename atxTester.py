# Yann Allandit
## Last update: January the 16th, 2020

import subprocess
import re
import multiprocessing
import random
import time

listeProc = []
nbSocket = []
nbThread = []
hyperThreading = False


def nombreOcc(valeur):
    occurence = listeProc.count (str(valeur))
    return occurence


def reporting():
    socketStatus = 0
    # Number of processor in the system
    nbProc = multiprocessing.cpu_count()

    ## Detect Hyper-Threading
    h = subprocess.Popen('lscpu |grep Thread| awk \'{print $4}\'', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in h.stdout.readlines():
        nbThread.append ((re.sub("[^0-9]", "", str(line))))
    nbThread[0] = int (nbThread[0])    
    if nbThread[0] > 1:
        hyperThreading = True
    else:
        hyperThreading = False

    ## Number of socket in the system
    q = subprocess.Popen('lscpu |grep Socket| awk \'{print $2}\'', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in q.stdout.readlines():
        nbSocket.append ((re.sub("[^0-9]", "", str(line))))
    nbSocket[0] = int (nbSocket[0])

    ## Processor where the loader is running
    p = subprocess.Popen('ps -aeF |grep atxTester.py|grep -v grep|awk \'{print $7}\'', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        listeProc.append ((re.sub("[^0-9]", "", str(line))))

    ## Sort the processor used list     
    listeProc.sort (key=lambda x:x[0])

    ## Print system information
    print ("========================================")
    print (" The system has ",nbSocket[0]," sockets")
    print (" The system has ",nbProc," core")
    if hyperThreading:
        print (" Hyper-threading is enabled")
    else:
        print (" Hyper-threading is disabled")
    print ("    ")

    ## Print the processes distribution map
    for j in range (nbProc):
        if j % (nbProc / nbSocket[0]) == 0:
            print ("===== Socket ",socketStatus, " ======")
            socketStatus += 1
        print ("CPU ", j, " has ", nombreOcc (j), " processes")

    retval = p.wait()

    
def pieceEquilibree():
    if random.uniform(0,1) <= 0.5:
        return 1
    else:
        return -1
    

def pieceJeuA():
    if random.uniform(0,1) <= 0.49:
        return 1
    else:
        return -1
    

def pieceJeuB1():
    if random.uniform(0,1) <= 0.09:
        return 1
    else:
        return -1
    

def pieceJeuB2():
    if random.random() <= 0.74:
        return 1
    else:
        return -1
    

def child():
    moy = 0
    for i in range(10):
        n = 1000000
        gain = 0
        for i in range(n):
            jeu = pieceEquilibree()
            if jeu == 1:
                gain += pieceJeuA()
            else:
                if gain % 3 == 0:
                    gain += pieceJeuB1()
                else:
                    gain += pieceJeuB2()
        moy += gain

#    print("le gain net est de :", moy /10, "euros")    


# function starting the childs process
def parent(nbChild):
    jobsChild = []
    for c in range(0, nbChild):
        processChild = multiprocessing.Process(target=child, args=())
        jobsChild.append(processChild)

    for c in jobsChild:
        c.start()

    for c in jobsChild:
        c.join()

# core program
if __name__ == "__main__":
    process = multiprocessing.set_start_method('fork')
    jobsParent = []
    procsP = input ("How many Parent jobs? ")
    procsP = int (procsP)
    procsC = input ("How many Child jobs? ")
    procsC = int (procsC)
    for p in range (0, procsP):
        process = multiprocessing.Process (target=parent, args=(procsC,))
        jobsParent.append (process)
    
    for p in jobsParent:
        p.start()

    time.sleep (2) 
    reporting()
    
    for p in jobsParent:
        p.join()
    
    print ("    ")
    print ("processing complete")
   
