import sys

def main():
    info = extractCommandLineArgs(sys.argv)
    algorithmList = ["SRTN", "FIFO", "RR"]
    fileName = info[0]
    algorithm = info[1]
    if algorithm not in algorithmList:
        algorithm = "FIFO"
    quantum = info[2]
    if len(quantum) == 0:
        quantum = 1
    else:
        quantum = int(quantum)    
    if algorithm == "SRTN":
        SRTN(fileName)
    elif algorithm == "FIFO":
        FIFO(fileName)
    elif algorithm == "RR":
        RR(fileName, quantum)

def extractCommandLineArgs(arguments):
    inputFile = arguments[1]
    algorithm = ""
    quantum = ""
    for i in range(len(arguments)):
        if '-p' == arguments[len(arguments)-1]:
            algorithm = algorithm
        elif arguments[i] == '-p':
            if arguments[i+1] == "-q":
                algorithm = algorithm
            else:
                algorithm += arguments[i+1]
        if '-q' == arguments[len(arguments)-1]:
            quantum = quantum
        elif arguments[i] == '-q':
            if arguments[i+1] == "-p":
                quantum = quantum
            else:
                quantum += arguments[i+1]
    return inputFile, algorithm, quantum

def readFileContents(inputFile):
    mydict = {}
    listOfJobs = []
    f = open(inputFile, "r")
    content = f.read()
    process_list = content.split("\n")
    print(process_list)
    for process in process_list:
        if process == "":
            continue
        values = process.split()
        listOfJobs.append((int(values[0]), int(values[1])))
    listOfJobs.sort(key = lambda x: x[1]) 
    i = 0
    for job in listOfJobs:
        mydict[i] = job
        i+=1
    return mydict

def SRTN(inputFile):
    print("You are in SRTN function.")
    print("File name: " + inputFile)
    print(readFileContents(inputFile))

def FIFO(inputFile):
    print("You are in FIFO function.")
    print("File name: " + inputFile)
    print(readFileContents(inputFile))

def RR(inputFile, quantum):
    print("You are in RR function.")
    print("File name: " + inputFile)
    print("Quantum Value: ", quantum)
    print(readFileContents(inputFile))

if __name__ == '__main__':
    main()
    