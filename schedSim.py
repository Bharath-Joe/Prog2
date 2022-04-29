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
    try:
        f = open(inputFile, "r")
    except FileNotFoundError:
        print("Wrong file or file path")
        exit()
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
    jobdict = readFileContents(inputFile)
    num_left = len(jobdict)
    gantChart = []
    current_time = 0
    for i in range(current_time, jobdict[0][1]):
        gantChart.append("IDLE")
        current_time += 1
    gantChart.append(0)
    minVal = 0

    while num_left > 0:
        temp = []
        if minVal != "IDLE":
            temp.append(jobdict[minVal][0] - 1)
            temp.append(jobdict[minVal][1])
            jobdict.update({minVal: temp})
            if (jobdict[minVal][0]) == 0:
                num_left -= 1
        current_time += 1
        minVal = getShortestJob(jobdict, current_time, num_left)
        if minVal == -1:
            break
        gantChart.append(minVal)

    end_times = {}
    turnaround_times = {}
    wait_time = {}
    for i in range(0, len(jobdict)):
        turnaround_times.update({i : 0})
        end_times.update({i : 0})
        wait_time.update({i : 0})
    i = 0
    while(i < len(jobdict)):
        for x in range(len(gantChart) - 1, -1, -1):
            if gantChart[x] == i:
                end_times.update({i : x + 1})
                break
        i += 1
    for i in range(0, len(end_times)):
        turn_time = end_times[i] - jobdict[i][1]
        turnaround_times.update({i : turn_time})
    
    mydict = readFileContents(inputFile) # reset vals of mydict
    for i in range(0, len(mydict)):
        wait = turnaround_times[i] - mydict[i][0]
        wait_time.update({i : wait})

    avg_turnaround = 0
    avg_wait = 0
    for i in range(0, len(mydict)):
        avg_wait += wait_time[i]
        avg_turnaround += turnaround_times[i]
        print("Job %3d -- Turnaround %3.2f  Wait %3.2f"%(i, turnaround_times[i], wait_time[i]))
    avg_turnaround /= len(mydict)
    avg_wait /= len(mydict)
    print("Average - - Turnaround %3.2f Wait %3.2f" % (avg_turnaround, avg_wait))
    

def getShortestJob(jobDict, current_time, num_left):
    arrivedJobs = {}
    for job in jobDict:
        if jobDict[job][1] <= current_time and jobDict[job][0] != 0:
            arrivedJobs[job] = jobDict[job]
    if len(arrivedJobs) > 0:
        minValue = min(arrivedJobs.items(), key=lambda x: x[1][0]) 
        return minValue[0]
    else:
        if num_left > 0:
            return "IDLE"
        else:
            return -1


def FIFO(inputFile):
    print("You are in FIFO function.")
    print("File name: " + inputFile)
    gantChart = []
    waitTime = {}
    completionTime = {}
    turnAroundTime = {}
    startTime = {}
    sumTAT = 0
    sumWT = 0
    jobDict = readFileContents(inputFile)

    for job in jobDict:
        for i in range(jobDict[job][0]):
            if jobDict[job][1] > len(gantChart):
                for j in range(jobDict[job][1] - len(gantChart)):
                    gantChart.append("IDLE")
            gantChart.append(job)
        completionTime[job] = len(gantChart)

    for job in jobDict:
        startTime[job] = gantChart.index(job)
        turnAroundTime[job] = completionTime[job] - jobDict[job][1]
        waitTime[job] = startTime[job] - jobDict[job][1]
        sumWT += waitTime[job]
        sumTAT += turnAroundTime[job]
        print("Job %3d -- Turnaround %3.2f  Wait %3.2f"%(job, turnAroundTime[job], waitTime[job]))
    avgWT = sumWT / len(jobDict)
    avgTAT = sumTAT / len(jobDict)
    print("Average -- Turnaround %3.2f  Wait %3.2f" % (avgTAT, avgWT))

def RR(inputFile, quantum):
    print("You are in RR function w/ quantum =", quantum)
    print("File name: " + inputFile)
    mydict = readFileContents(inputFile)
    num_left = len(mydict)
    process_executions = []
    cur_time = 0
    before_cur_time = 0
    queue = []
    if mydict[0][1] == 0:
        queue.append(0) # process 0
    print(mydict)
    while len(queue) > 0 or num_left > 0: 
        if num_left != 0:
            while mydict[len(mydict) - num_left][1] > cur_time:
                process_executions.append("IDLE")
                cur_time += 1
            if len(process_executions) > 0:
                if process_executions[len(process_executions) - 1] == "IDLE":
                    queue.append(len(mydict) - num_left)

        before_cur_time = cur_time

        for i in range(0, quantum):
            if mydict[queue[0]][0] > 0 and mydict[queue[0]][1] <= cur_time:
                process_executions.append(queue[0])
                temp = []
                temp.append(mydict[queue[0]][0] - 1)
                temp.append(mydict[queue[0]][1])
                mydict.update({queue[0] : temp})
                if (mydict[queue[0]][0]) == 0:
                    num_left -= 1
                cur_time += 1
            else:
                break

        for key in mydict:
            if mydict[key][1] <= cur_time and mydict[key][1] >= before_cur_time and key != queue[0]:
                queue.append(key)

        if mydict[queue[0]][0] > 0:
            queue.append(queue[0])
        queue.pop(0)
        
    end_times = {}
    turnaround_times = {}
    wait_time = {}
    for i in range(0, len(mydict)):
        turnaround_times.update({i : 0})
        end_times.update({i : 0})
        wait_time.update({i : 0})
    i = 0
    while(i < len(mydict)):
        for x in range(len(process_executions) - 1, -1, -1):
            if process_executions[x] == i:
                end_times.update({i : x + 1})
                break
        i += 1

    for i in range(0, len(end_times)):
        turn_time = end_times[i] - mydict[i][1]
        turnaround_times.update({i : turn_time})

    mydict = readFileContents(inputFile) # reset vals of mydict
    for i in range(0, len(mydict)):
        wait = turnaround_times[i] - mydict[i][0]
        wait_time.update({i : wait})

    avg_turnaround = 0
    avg_wait = 0
    for i in range(0, len(mydict)):
        avg_wait += wait_time[i]
        avg_turnaround += turnaround_times[i]
        print("Job %3d -- Turnaround %3.2f  Wait %3.2f"%(i, turnaround_times[i], wait_time[i]))
    avg_turnaround /= len(mydict)
    avg_wait /= len(mydict)
    print("Average - - Turnaround %3.2f Wait %3.2f" % (avg_turnaround, avg_wait))

if __name__ == '__main__':
    main()