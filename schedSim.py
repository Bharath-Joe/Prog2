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
    # print(process_list)
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
    mydict = readFileContents(inputFile)
    # for key in mydict:
    #     print(mydict[key])
    # print(len(mydict))
    # print(mydict[0])
    # temp = []
    # temp.append(mydict[0][0] - 1)
    # temp.append(mydict[0][1])

    # mydict.update({0 : temp})
    print(mydict)

    num_left = len(mydict)
    running_process = 0
    process_executions = []
    while(num_left > 0):
        quant_copy = quantum
        while(quant_copy > 0):
            if mydict[running_process][0] <= 0:
                break
            print("[P" + str(running_process) + "]", end = "")
            process_executions.append(running_process)
            temp = []
            temp.append(mydict[running_process][0] - 1)
            temp.append(mydict[running_process][1])
            mydict.update({running_process : temp})
            if mydict[running_process][0] == 0:
                num_left -= 1
            quant_copy -= 1
        if(running_process == len(mydict) - 1):
            running_process = 0
        else:
            running_process += 1
    print()
    end_time = {}
    turnaround_times = {}
    wait_time = {}
    for i in range(0, len(mydict)):
        turnaround_times.update({i : 0})
        end_time.update({i : 0})
        wait_time.update({i : 0})
    i = 0
    while(i < len(mydict)):
        for x in range(len(process_executions) - 1, -1, -1):
            if process_executions[x] == i:
                end_time.update({i : x + 1})
                break
        i += 1

    for i in range(0, len(end_time)):
        turn_time = end_time[i] - mydict[i][1]
        turnaround_times.update({i : turn_time})

    
    mydict = readFileContents(inputFile) # reset vals of mydict
    for i in range(0, len(mydict)):
        wait = turnaround_times[i] - mydict[i][0]
        wait_time.update({i : wait})
    

    print("Process \t wait \t turn-around")
    avg_turnaround = 0
    avg_wait = 0
    for i in range(0, len(mydict)):
        print(str(i) + "  \t\t" + str(wait_time[i]) + "  \t\t" +  str(turnaround_times[i]))
        avg_wait += wait_time[i]
        avg_turnaround += turnaround_times[i]
    avg_turnaround /= len(mydict)
    avg_wait /= len(mydict)
    print("Average - - Turnaround %3.2f Wait %3.2f" % (avg_turnaround, avg_wait))

if __name__ == '__main__':
    main()
    