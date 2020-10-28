import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


# --------------------START ROUND ROBIN------------------------------

def process_data_s(ns, pr_no_s, burst_s, arrival_s):
    process_data = []
    for i in range(ns):
        process_data.append(
            [pr_no_s[i], arrival_s[i], burst_s[i], 0, burst_s[i]])

    return process_data


def schedulingProcess_rr(process_data, time_slice):
    start_time = []
    exit_time = []
    executed_process = []
    ready_queue = []
    s_time = 0

    process_exec = {}
    for i in range(len(process_data)):
        process_exec[i+1] = []

    process_data.sort(key=lambda x: x[1])
    '''
    Sort processes according to the Arrival Time
    '''
    while 1:
        normal_queue = []
        temp = []
        for i in range(len(process_data)):
            if process_data[i][1] <= s_time and process_data[i][3] == 0:  # if unexecuted
                present = 0
                if len(ready_queue) != 0:  # if ready_queue is not empty
                    for k in range(len(ready_queue)):
                        # if current process is present in ready queue
                        if process_data[i][0] == ready_queue[k][0]:
                            present = 1
                '''
                The above if loop checks if the current process is in the ready queue or not
                '''
                if present == 0:  # if it is not present then add it to the ready queue
                    temp.extend([process_data[i][0], process_data[i]
                                 [1], process_data[i][2], process_data[i][4]])
                    ready_queue.append(temp)
                    temp = []
                '''
                The above if loop adds a process to the ready_queue only if it is not already present in it
                '''
                if len(ready_queue) != 0 and len(executed_process) != 0:
                    for k in range(len(ready_queue)):
                        if ready_queue[k][0] == executed_process[len(executed_process) - 1]:
                            ready_queue.insert(
                                (len(ready_queue) - 1), ready_queue.pop(k))
                '''
                The above if loop makes sure that the recently executed process is appended at the end of ready_queue
                '''
            elif process_data[i][3] == 0:
                temp.extend([process_data[i][0], process_data[i][1],
                             process_data[i][2], process_data[i][4]])
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

                process_exec[ready_queue[0][0]].append(
                    tuple([start_time[-1], time_slice]))

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

                process_exec[ready_queue[0][0]].append(
                    tuple([start_time[-1], ready_queue[0][2]]))

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

                process_exec[ready_queue[0][0]].append(
                    tuple([start_time[-1], time_slice]))

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

                process_exec[ready_queue[0][0]].append(
                    tuple([start_time[-1], normal_queue[0][2]]))

                executed_process.append(normal_queue[0][0])
                for j in range(len(process_data)):
                    if process_data[j][0] == normal_queue[0][0]:
                        break
                process_data[j][2] = 0
                process_data[j][3] = 1
                process_data[j].append(e_time)
    return process_exec, e_time


# --------------------END ROUND ROBIN----------------------------


# --------------------START preSJF------------------------------------------

def processData_i(no_of_processes, pr_no, arrival, burst):
    process_data = []
    for i in range(no_of_processes):
        temporary = []
#         process_id = int(input("Enter Process ID: "))
#         arrival_time = int(input(f"Enter Arrival Time for Process {process_id}: "))
#         burst_time = int(input(f"Enter Burst Time for Process {process_id}: "))
        temporary.extend([pr_no[i], arrival[i], burst[i], 0, burst[i]])
        '''
        '0' is the state of the process. 0 means not executed and 1 means execution complete
        '''
        process_data.append(temporary)
    return schedulingProcess_i(process_data, arrival[0])


def schedulingProcess_i(process_data, arr_time):
    start_time = []
    exit_time = []
    s_time = 0
    sequence_of_process = []

    process_exec = {}
    for i in range(len(process_data)):
        process_exec[i + 1] = []

    process_data.sort(key=lambda x: x[1])
    '''
    Sort processes according to the Arrival Time
    '''
    while 1:
        ready_queue = []
        normal_queue = []
        temp = []
        for i in range(len(process_data)):
            if process_data[i][1] <= s_time and process_data[i][3] == 0:
                temp.extend([process_data[i][0], process_data[i][1],
                             process_data[i][2], process_data[i][4]])
                ready_queue.append(temp)
                temp = []
            elif process_data[i][3] == 0:
                temp.extend([process_data[i][0], process_data[i][1],
                             process_data[i][2], process_data[i][4]])
                normal_queue.append(temp)
                temp = []
        if len(ready_queue) == 0 and len(normal_queue) == 0:
            break
        if len(ready_queue) != 0:
            ready_queue.sort(key=lambda x: x[2])
            '''
            Sort processes according to Burst Time
            '''
            start_time.append(s_time)
            s_time = s_time + 1
            e_time = s_time
            exit_time.append(e_time)
            sequence_of_process.append(ready_queue[0][0])
            for k in range(len(process_data)):
                if process_data[k][0] == ready_queue[0][0]:
                    break

            process_exec[ready_queue[0][0]].append(tuple([start_time[-1], 1]))

            process_data[k][2] = process_data[k][2] - 1
            # If Burst Time of a process is 0, it means the process is completed
            if process_data[k][2] == 0:
                process_data[k][3] = 1
                process_data[k].append(e_time)
        if len(ready_queue) == 0:
            if s_time < normal_queue[0][1]:
                s_time = normal_queue[0][1]
            start_time.append(s_time)
            s_time = s_time + 1
            e_time = s_time
            exit_time.append(e_time)

            process_exec[ready_queue[0][0]].append(tuple([start_time[-1], 1]))

            sequence_of_process.append(normal_queue[0][0])
            for k in range(len(process_data)):
                if process_data[k][0] == normal_queue[0][0]:
                    break
            process_data[k][2] = process_data[k][2] - 1
            # If Burst Time of a process is 0, it means the process is completed
            if process_data[k][2] == 0:
                process_data[k][3] = 1
                process_data[k].append(e_time)
    return process_exec

# -------------------END SJF----------------------------------------------


# ------------------START PRIORITY-----------------------------------------------

def processData_b(no_of_processes, pr_no, arrival, burst, priority):
    process_data = []
    for i in range(no_of_processes):
        temporary = []
#         process_id = int(input("Enter Process ID: "))
#         arrival_time = int(input(f"Enter Arrival Time for Process {process_id}: "))
#         burst_time = int(input(f"Enter Burst Time for Process {process_id}: "))
#         priority = int(input(f"Enter Priority for Process {process_id}: "))
        temporary.extend(
            [pr_no[i], arrival[i], burst[i], priority[i], 0, burst[i]])
        '''
        '0' is the state of the process. 0 means not executed and 1 means execution complete
        '''
        process_data.append(temporary)
    return schedulingProcess_b(process_data, process_data[0][1])


def schedulingProcess_b(process_data, comp_time):
    start_time = []
    exit_time = []
    s_time = comp_time
    sequence_of_process = []

    process_exec = {}
    for i in range(len(process_data)):
        process_exec[i + 1] = []

    process_data.sort(key=lambda x: x[1])
    '''
    Sort processes according to the Arrival Time
    '''
    while 1:
        ready_queue = []
        normal_queue = []
        temp = []
        for i in range(len(process_data)):
            # if the process has arrived and it is still unexecuted
            if process_data[i][1] <= s_time and process_data[i][4] == 0:
                temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][3],
                             process_data[i][5]])
                # then append the process in ready queue
                ready_queue.append(temp)
                # reset temp
                temp = []
            # if the process has not yet arrived but and is unexecuted
            elif process_data[i][4] == 0:
                temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4],
                             process_data[i][5]])
                # put the process in the normal queue
                normal_queue.append(temp)
                # reset temp
                temp = []
        # if all processes have executed break the loop
        if len(ready_queue) == 0 and len(normal_queue) == 0:
            break
        # if there is a process in the ready queue
        if len(ready_queue) != 0:
            # sort the processes in the ready queue by priority
            ready_queue.sort(key=lambda x: x[3], reverse=True)
            start_time.append(s_time)
            # execute the current process by 1 sec
            s_time = s_time + 1
            e_time = s_time
            exit_time.append(e_time)
            sequence_of_process.append(ready_queue[0][0])
            # find the index of the currently running process
            for k in range(len(process_data)):
                if process_data[k][0] == ready_queue[0][0]:
                    break

            process_exec[ready_queue[0][0]].append(tuple([start_time[-1], 1]))

            # reduce its burst time by 1
            process_data[k][2] = process_data[k][2] - 1
            # if the process completes its execution
            if process_data[k][2] == 0:
                # mark its completion
                process_data[k][4] = 1
                process_data[k].append(e_time)
        if len(ready_queue) == 0:
            normal_queue.sort(key=lambda x: x[1])
            if s_time < normal_queue[0][1]:
                s_time = normal_queue[0][1]
            start_time.append(s_time)
            s_time = s_time + 1
            e_time = s_time
            exit_time.append(e_time)

            process_exec[ready_queue[0][0]].append(tuple([start_time[-1], 1]))

            sequence_of_process.append(normal_queue[0][0])
            for k in range(len(process_data)):
                if process_data[k][0] == normal_queue[0][0]:
                    break
            process_data[k][2] = process_data[k][2] - 1
            # if burst time is zero, it means process is completed
            if process_data[k][2] == 0:
                process_data[k][4] = 1
                process_data[k].append(e_time)
    return process_exec

# ------------------END PRIORITY-----------------------------


if __name__ == '__main__':
    #     ns = int(input('Enter number of system processes: '))
    #     pr_no_s = list(map(int,input('Enter processes numbers: ').split()))
    #     burst_s = list(map(int,input('Enter burst time of processses: ').split()))
    #     arrival_s = [0 for i in range(ns)]
    #     time_slice = int(input('Enter time quantam: '))
    #     process_info_s=process_data_s(ns,pr_no_s,burst_s,arrival_s)
    #     gant_array_s,e_time_s=schedulingProcess_rr(process_info_s,time_slice)
    #     print(gant_array_s)
    # ns = 3
    # pr_no_s = [1, 2, 3]
    # burst_s = [5, 2, 10]
    # arrival_s = [0, 0, 2]
    # time_slice = 2
    # process_info_s = process_data_s(ns, pr_no_s, burst_s, arrival_s)
    # gant_array_s, e_time_s = schedulingProcess_rr(process_info_s, time_slice)
    # print(gant_array_s)

    #     ni = int(input('Enter number of interactive processes: '))
    #     pr_no_i = list(map(int,input('Enter processes numbers: ').split()))
    # #     comp_i = [0 for i in range(ni)]
    #     burst_i = list(map(int,input('Enter burst time of processses: ').split()))
    #     arrival_i = [0 for i in range(ni)]
    #     gant_array_i=processData_i(ni, pr_no_i, arrival_i, burst_i)
    #     print(gant_array_i)
    # ni = 3
    # pr_no_i = [1, 2, 3]
    # burst_i = [5, 2, 10]
    # arrival_i = [0, 0, 2]
    # gant_array_i = processData_i(ni, pr_no_i, arrival_i, burst_i)
    # print(gant_array_i)

    #     nb = int(input('Enter number of batch processes: '))
    #     pr_no_b = list(map(int,input('Enter processes numbers: ').split()))
    #     burst_b = list(map(int,input('Enter burst time of processses: ').split()))
    #     arrival_b = [comp_time_i for i in range(nb)]
    #     priority_b = list(map(int,input('Enter priority: ').split()))
    #     gant_array_b=processData_b(nb, pr_no_b, arrival_b, burst_b, priority_b)
    #     print(gant_array_b)
    # 1 2 3 4 5 6 7 : pr_no
    # 3 4 6 1 1 5 7 : burst
    # .. arival
    # S U I S S U I :
    n = 7
    pr_no = [3, 4, 5, 6, 7, 1, 2]
    arrival = [3, 7, 8, 15, 25, 0, 2]
    burst = [10, 1, 5, 2, 7, 3, 6]
    pr_type = ['s', 'i', 'u', 's', 's', 'i', 'u']
    quantum = 2
    pr_no_s, pr_no_u, pr_no_i, arrival_s, arrival_i, arrival_u, burst_s, burst_i, burst_u = [
    ], [], [], [], [], [], [], [], []
    for i in range(n):
        if pr_type[i] == 's':
            pr_no_s.append(pr_no[i])
            arrival_s.append(arrival[i])
            burst_s.append(burst[i])
        elif pr_type[i] == 'i':
            pr_no_i.append(pr_no[i])
            arrival_i.append(arrival[i])
            burst_i.append(burst[i])
        else:
            pr_no_u.append(pr_no[i])
            arrival_u.append(arrival[i])
            burst_u.append(burst[i])
    n_s, n_i, n_u = len(pr_no_s), len(pr_no_i), len(pr_no_u)

    # first rr
    print(n_s, pr_no_s, arrival_s, burst_s)
    print(RR.processData(
        n_s, quantum, pr_no_s, arrival_s, burst_s, 50))

# s, u, i
