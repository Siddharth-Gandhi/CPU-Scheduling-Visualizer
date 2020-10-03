# print("Siddharth Gandhi 19BCE0005")

# def findWaitingTime(processes, n, bt, wt, quantum): 
#     rem_bt = [0] * n 
#     for i in range(n): 
#         rem_bt[i] = bt[i] 
#     t = 0 
#     while(1): 
#         done = True
#         for i in range(n): 
#             if (rem_bt[i] > 0) : 
#                 done = False 
#                 if (rem_bt[i] > quantum) : 
#                     t += quantum 
#                     rem_bt[i] -= quantum 
#                 else: 
#                     t = t + rem_bt[i] 
#                     wt[i] = t - bt[i] 
#                     rem_bt[i] = 0
#         if (done == True): 
#             break

# def findTurnAroundTime(processes, n, bt, wt, tat): 
#     for i in range(n): 
#         tat[i] = bt[i] + wt[i] 

# def findavgTime(processes, n, bt, quantum): 
#     wt = [0] * n 
#     tat = [0] * n 
#     findWaitingTime(processes, n, bt, wt, quantum) 
#     findTurnAroundTime(processes, n, bt, wt, tat) 
#     print("Processes Burst Time	 Waiting","Time Turn-Around Time") 
#     total_wt = 0
#     total_tat = 0
#     for i in range(n): 
#         total_wt = total_wt + wt[i] 
#         total_tat = total_tat + tat[i] 
#         print(" ", i + 1, "\t\t", bt[i], "\t\t", wt[i], "\t\t", tat[i]) 
#     print("\nAverage waiting time = %.5f "%(total_wt /n) ) 
#     print("Average turn around time = %.5f "% (total_tat / n)) 
    
# if __name__ =="__main__": 
#     n = int(input("Enter number of processes: "))
#     proc = []
#     burst = [] 
#     print("Enter in form of process_number, burst")
#     for i in range(n):
#         x, y = map(int, input().split())
#         proc.append(x)
#         burst.append(y)
#     quantum = int(input("Enter quantum: "))
#     findavgTime(proc, n, burst, quantum) 

import pandas as pd
import matplotlib.pyplot as plt

def processData(no_of_processes):
    process_data = []
    for i in range(no_of_processes):
        temporary = []
        process_id = int(input("Enter Process ID: "))
        arrival_time = int(input(f"Enter Arrival Time for Process {process_id}: "))
        burst_time = int(input(f"Enter Burst Time for Process {process_id}: "))
        temporary.extend([process_id, arrival_time, burst_time, 0, burst_time])
        '''
        '0' is the state of the process. 0 means not executed and 1 means execution complete
        '''
        process_data.append(temporary)
    time_slice = int(input("Enter Time Quantum : "))
    schedulingProcess(process_data, time_slice)
        
def schedulingProcess(process_data, time_slice):
    start_time = []
    exit_time = []
    executed_process = []
    ready_queue = []
    s_time = 0

    process_exec={}
    for i in range(len(process_data)):
        process_exec[i+1]=[]

    process_data.sort(key=lambda x: x[1])
    '''
    Sort processes according to the Arrival Time
    '''
    while 1:
        normal_queue = []
        temp = []
        for i in range(len(process_data)):
            if process_data[i][1] <= s_time and process_data[i][3] == 0: #if unexecuted
                present = 0
                if len(ready_queue) != 0: # if ready_queue is not empty
                    for k in range(len(ready_queue)): 
                        if process_data[i][0] == ready_queue[k][0]: # if current process is present in ready queue
                            present = 1
                '''
                The above if loop checks if the current process is in the ready queue or not
                '''
                if present == 0: # if it is not present then add it to the ready queue
                    temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                    ready_queue.append(temp)
                    temp = []
                '''
                The above if loop adds a process to the ready_queue only if it is not already present in it
                '''
                if len(ready_queue) != 0 and len(executed_process) != 0: 
                    for k in range(len(ready_queue)):
                        if ready_queue[k][0] == executed_process[len(executed_process) - 1]:
                            ready_queue.insert((len(ready_queue) - 1), ready_queue.pop(k))
                '''
                The above if loop makes sure that the recently executed process is appended at the end of ready_queue
                '''
            elif process_data[i][3] == 0:
                temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                normal_queue.append(temp)
                temp = []
        if len(ready_queue) == 0 and len(normal_queue) == 0:
            break
        if len(ready_queue) != 0:
            if ready_queue[0][2] > time_slice:
                '''
                If process has remaining burst time greater than the time slice, it will execute for a time period equal to time slice and then switch
                '''
                start_time.append(s_time)
                s_time = s_time + time_slice
                e_time = s_time
                exit_time.append(e_time)

                process_exec[ready_queue[0][0]].append(tuple([start_time[-1],time_slice]))

                executed_process.append(ready_queue[0][0])
                for j in range(len(process_data)):
                    if process_data[j][0] == ready_queue[0][0]:
                        break
                process_data[j][2] = process_data[j][2] - time_slice
                ready_queue.pop(0)
            elif ready_queue[0][2] <= time_slice:
                '''
                If a process has a remaining burst time less than or equal to time slice, it will complete its execution
                '''
                start_time.append(s_time)
                s_time = s_time + ready_queue[0][2]
                e_time = s_time
                exit_time.append(e_time)

                process_exec[ready_queue[0][0]].append(tuple([start_time[-1],ready_queue[0][2]]))

                executed_process.append(ready_queue[0][0])
                for j in range(len(process_data)):
                    if process_data[j][0] == ready_queue[0][0]:
                        break
                process_data[j][2] = 0
                process_data[j][3] = 1
                process_data[j].append(e_time)
                ready_queue.pop(0)
        elif len(ready_queue) == 0:
            if s_time < normal_queue[0][1]:
                s_time = normal_queue[0][1]
            if normal_queue[0][2] > time_slice:
                '''
                If process has remaining burst time greater than the time slice, it will execute for a time period equal to time slice and then switch
                '''
                start_time.append(s_time)
                s_time = s_time + time_slice
                e_time = s_time
                exit_time.append(e_time)

                process_exec[ready_queue[0][0]].append(tuple([start_time[-1],time_slice]))

                executed_process.append(normal_queue[0][0])
                for j in range(len(process_data)):
                    if process_data[j][0] == normal_queue[0][0]:
                        break
                process_data[j][2] = process_data[j][2] - time_slice
            elif normal_queue[0][2] <= time_slice:
                '''
                If a process has a remaining burst time less than or equal to time slice, it will complete its execution
                '''
                start_time.append(s_time)
                s_time = s_time + normal_queue[0][2]
                e_time = s_time
                exit_time.append(e_time)

                process_exec[ready_queue[0][0]].append(tuple([start_time[-1],normal_queue[0][2]]))

                executed_process.append(normal_queue[0][0])
                for j in range(len(process_data)):
                    if process_data[j][0] == normal_queue[0][0]:
                        break
                process_data[j][2] = 0
                process_data[j][3] = 1
                process_data[j].append(e_time)
    printData(process_data,process_exec)

def printData(process_data,process_exec):
    print(process_exec)
    process_data.sort(key=lambda x: x[0])

    result_df=pd.DataFrame()
    process_ID=[]
    process_AT=[]
    process_BT=[]
    process_CT=[]
    for i in range(len(process_data)):
        process_ID.append(process_data[i][0])
        process_AT.append(process_data[i][1])
        process_BT.append(process_data[i][-2])
        process_CT.append(process_data[i][-1])

    result_df['process_id']=process_ID
    result_df['arrival_time']=process_AT
    result_df['burst_time']=process_BT
    result_df['completion_time']=process_CT
    process_TT=result_df['completion_time']-result_df['arrival_time']
    result_df['turnaround_time']=process_TT
    process_WT=result_df['turnaround_time']-result_df['burst_time']
    result_df['waiting_time']=process_WT
    result_df.set_index('process_id',inplace=True)
    print(result_df)
    print("average turnaround time : {}".format(result_df['turnaround_time'].mean()))
    print("average waiting time : {}".format(result_df['waiting_time'].mean()))
    plot(process_ID,process_AT,process_BT,len(process_ID),process_exec,40)
        
def get_cmap(n, name="hsv"):
    """Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name."""
    return plt.cm.get_cmap(name, n)
        
def plot(pr_no, arrival, burst, n, gantt_array, final_comp_time):
# default syntax, remember it
# gnt stands for gantt (just for our convenience)
    fig, gnt = plt.subplots()

    # X axis: time
    # Y axis: process number

    # find the gantt array if we don't have a custom one
#     if gantt_array == None and final_comp_time == None:
#         gantt_array, final_comp_time = find_gantt_array(pr_no, arrival, burst, n)

    # the y limits will be from 0 to number of process + 2 (for better visibility)
    gnt.set_ylim(0, n + 2)

    # x limits from 0 to final_comp_time + 3 (for better visibility)
    gnt.set_xlim(0, final_comp_time + 3)

    # setting x and y labels
    gnt.set_xlabel("Seconds since start")
    gnt.set_ylabel("Process number")

    # yticks mean the values we can see, here we want it to run through the middle
    # of the process block (i + 1.5 came through trial and error)
    gnt.set_yticks([i + 0.5 for i in pr_no])

    # labelling the y ticks
    gnt.set_yticklabels(pr_no)

    # grid on, duh!
    gnt.grid(True)

    # this is an array for different colors
    cmap = get_cmap(n + 1)
    for i in pr_no:
        # generating a random color
        # r = random.random()
        # b = random.random()
        # g = random.random()
        # color = (r, g, b)
        gnt.broken_barh(gantt_array[i], (i, 1), facecolor=cmap(i))
    plt.show()


no_of_processes = int(input("Enter number of processes: "))
processData(no_of_processes)