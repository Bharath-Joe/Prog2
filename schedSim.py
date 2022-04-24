import sys

def main():
    info = extractCommandLineArgs(sys.argv)
    algorithmList = ["SRTN", "FIFO", "RR"]
    fileName = info[0]
    algorithm = info[1]
    if algorithm not in algorithmList:
        algorithm = "FIFO"
    quantum = info[2]
    if len(quantum) == 0 or not quantum.isdigit():
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
    gantChart = []
    waitTime = {}
    completionTime = {}
    turnAroundTime = {}
    startTime = {}
    sumTAT = 0
    sumWT = 0
    print("File name: " + inputFile)
    jobDict = readFileContents(inputFile)
    # print("Job: (Burst Time, Arrival Time)")
    # print(jobDict)
    for job in jobDict:
        for i in range(jobDict[job][0]):
            if jobDict[job][1] > len(gantChart):
                for j in range(jobDict[job][1] - len(gantChart)):
                    gantChart.append("IDLE")
            gantChart.append(job)
        completionTime[job] = len(gantChart)
    print("gantChart:", end=" ")
    print(gantChart)
    for job in jobDict:
        startTime[job] = gantChart.index(job)
        turnAroundTime[job] = completionTime[job] - jobDict[job][1]
        waitTime[job] = startTime[job] - jobDict[job][1]
        sumWT += waitTime[job]
        sumTAT += turnAroundTime[job]
        print("Job %3d -- Turnaround %3.2f  Wait %3.2f"%(job, turnAroundTime[job], waitTime[job]))
    # print("Start Time:", end=" ")
    # print(startTime)
    # print("Completion Time:", end=" ")
    # print(completionTime)
    # print("Turn-Around Time:", end=" ")
    # print(turnAroundTime)
    # print("Wait Time:", end=" ")
    # print(waitTime)
    avgWT = sumWT / len(jobDict)
    avgTAT = sumTAT / len(jobDict)
    print("Average -- Turnaround %3.2f  Wait %3.2f" % (avgTAT, avgWT))

def RR(inputFile, quantum):
    print("You are in RR function.")
    print("File name: " + inputFile)
    print("Quantum Value: ", quantum)
    print(readFileContents(inputFile))

if __name__ == '__main__':
    main()
    