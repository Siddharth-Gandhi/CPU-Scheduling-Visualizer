import pandas as pd
import matplotlib.pyplot as plt
import os
import random
import matplotlib.animation as animation


def processData(no_of_processes, pr_no, arrival, burst, speed):
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
    return schedulingProcess(process_data, speed)


def schedulingProcess(process_data, speed):
    start_time = []
    exit_time = []
    s_time = 0
    sequence_of_process = []

    process_exec = {}
    for i in range(len(process_data)):
        process_exec[process_data[i][0]] = []

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

            process_exec[normal_queue[0][0]].append(tuple([start_time[-1], 1]))

            sequence_of_process.append(normal_queue[0][0])
            for k in range(len(process_data)):
                if process_data[k][0] == normal_queue[0][0]:
                    break
            process_data[k][2] = process_data[k][2] - 1
            # If Burst Time of a process is 0, it means the process is completed
            if process_data[k][2] == 0:
                process_data[k][3] = 1
                process_data[k].append(e_time)
    return printData(process_data, process_exec, speed)


def printData(process_data, process_exec, speed):
    process_data.sort(key=lambda x: x[0])

    result_df = pd.DataFrame()
    process_ID = []
    process_AT = []
    process_BT = []
    process_CT = []
    for i in range(len(process_data)):
        process_ID.append(process_data[i][0])
        process_AT.append(process_data[i][1])
        process_BT.append(process_data[i][-2])
        process_CT.append(process_data[i][-1])

    result_df['process_id'] = process_ID
    result_df['arrival_time'] = process_AT
    result_df['burst_time'] = process_BT
    result_df['completion_time'] = process_CT
    process_TT = result_df['completion_time']-result_df['arrival_time']
    result_df['turnaround_time'] = process_TT
    process_WT = result_df['turnaround_time']-result_df['burst_time']
    result_df['waiting_time'] = process_WT
    result_df.set_index('process_id', inplace=True)
#     print(result_df)
#     print("average turnaround time : {}".format(result_df['turnaround_time'].mean()))
#     print("average waiting time : {}".format(result_df['waiting_time'].mean()))
    avg_tat = result_df['turnaround_time'].mean()
    avg_wt = result_df['waiting_time'].mean()
    plot(process_ID, process_AT, process_BT, len(
        process_ID), process_exec, max(list(result_df["completion_time"])), speed)
    return result_df, avg_tat, avg_wt


def get_cmap(n, name="hsv"):
    """Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name."""
    return plt.cm.get_cmap(name, n)


def plot(pr_no, arrival, burst, n, gantt_array, final_comp_time, speed):
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
    # for i in pr_no:
    #     # generating a random color
    #     # r = random.random()
    #     # b = random.random()
    #     # g = random.random()
    #     # color = (r, g, b)
    #     gnt.broken_barh(gantt_array[i], (i, 1), facecolor=cmap(i))
    # plt.show()
    plt.title('SJF Preemptive')

    def find(t):
        for i in gantt_array:
            for j in gantt_array[i]:
                if j[0] <= t < j[0] + j[1]:
                    return i, [(t, 1)]
        return -1

    def animate(i):
        if find(i) != -1:
            pr, time = find(i)
            gnt.broken_barh(time, (pr, 1), facecolor=cmap(pr))

    anim = animation.FuncAnimation(
        fig, animate, frames=final_comp_time, interval=speed
    )

    # plt.show()

    # mpld3.show(fig, "127.0.0.1", 5000)
    # if os.path.exists("static\\fcfs.gif"):
    #     try:
    #         os.remove("static\\fcfs.gif")
    #     except OSError as err:
    #         print("Failed with:", err.strerror)  # look what it says
    #         print("Error code:", err.code)
    # os.remove("static\\fcfs.gif")
    anim.save(
        "static\\gifs\\SJF Preemptive.gif",
        writer="pillow"
    )


if __name__ == "__main__":
    #     no_of_processes = int(input("Enter number of processes: "))
    #     sjf = SJF()
    #     sjf.processData(no_of_processes)
    # no_of_processes = 7  # int(input("Enter number of processes: "))
    # pr_no = [3, 4, 5, 6, 7, 1, 2]
    # arrival = [3, 7, 8, 15, 25, 0, 2]
    # burst = [10, 1, 5, 2, 7, 3, 6]
    no_of_processes = 3
    pr_no = [3, 6, 7]
    arrival = [3, 15, 25]
    burst = [10, 2, 7]
    temp = processData(no_of_processes, pr_no, arrival, burst, 150)
    print(temp)
