import matplotlib.pyplot as plt
import random

# TAT: turn around time

# ----------- FOR FINDING THE TABLE -----------------
# EDIT THIS

def findWaitingTime(processes, n, wt):  
    rt = [0] * n 
  
    # Copy the burst time into rt[]  
    for i in range(n):  
        rt[i] = processes[i][1] 
     # declaring service array that stores 
    # cumulative burst time  
    service = [0] * 5
  
    # Initilising initial elements  
    # of the arrays  
    service[0] = 0
    wt[0] = 0
  
    for i in range(1,n):  
        service[i] = processes[i - 1][1] + service[i - 1]  
        wt[i] = service[i] - processes[i][0] + 1
  
        # If waiting time is negative, 
        # change it o zero  
        if(wt[i] < 0) :      
            wt[i] = 0
  
# Function to calculate turn around time  
def findTurnAroundTime(processes, n, wt, tat):  
      
    # Calculating turnaround time  
    for i in range(n): 
        tat[i] = processes[i][1] + wt[i]  
  
# Function to calculate average waiting  
# and turn-around times.  
def findAllTimes(pr_no, arrival, burst, n, priority):  
    processes=[list(a) for a in zip(pr_no, burst, arrival, priority)]
    wt = [0] * n 
    tat = [0] * n  
  
    # Function to find waiting time  
    # of all processes  
    findWaitingTime(processes, n, wt)  
  
    # Function to find turn around time 
    # for all processes  
    findTurnAroundTime(processes, n, wt, tat)  
  
    # Display processes along with all details  
    print("Processes \t    Burst Time \t    Waiting",  
                    "Time \t    Turn-Around Time") 
    total_wt = 0
    total_tat = 0
    for i in range(n): 
  
        total_wt = total_wt + wt[i]  
        total_tat = total_tat + tat[i]  
        print(" ", processes[i][0], "\t\t\t",  
                   processes[i][1], "\t\t\t",  
                   wt[i], "\t\t", tat[i]) 
  
    print("\nAverage waiting time = %.5f "%(total_wt /n) ) 
    print("Average turn around time = ", total_tat / n)  
# --------------------- TILL HERE --------------------------------


def sort_by_arrival(pr_no, arrival, burst, n, priority):
    # mix them all up in 1 function and then sort by arrival
    mix = list(zip(pr_no, arrival, burst,priority))
    # thanks python for such ez sorting
    mix.sort(key=lambda x: x[3])

    pr_no = [x[0] for x in mix]
    arrival = [x[1] for x in mix]
    burst = [x[2] for x in mix]
    priority = [x[3] for x in mix]

    return pr_no, arrival, burst, priority


def get_cmap(n, name="hsv"):
    """Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name."""
    return plt.cm.get_cmap(name, n)


# ------------------------- FOR FINDING THE DICTIONARY -----------------------------
# EDIT THIS
def find_gantt_array(pr_no, arrival, burst, n, priority):
    mix = [list(a) for a in zip(pr_no, burst, arrival, priority)]

    # Note: mix is already sorted by arrival before function call

    result = {pr: [] for pr in pr_no}

    """for i in range(n):
        # each element of mix is a tuple of form (pr_no, arrival, burst)
        cur_pr = mix[i][0]
        cur_arr = mix[i][1]
        cur_burst = mix[i][2]

        if i == 0:
            # first item
            result[cur_pr].append((cur_arr, cur_burst))
            prev_end_time = cur_arr + cur_burst
        else:
            # check if prev is still executing ie current arrival < prev_end_time
            if cur_arr >= prev_end_time:
                # no conflicts
                result[cur_pr].append((cur_arr, cur_burst))
                prev_end_time = cur_arr + cur_burst
            else:
                # the current process arrives before the last one end
                # so the start for current will be prev_end_time
                result[cur_pr].append((prev_end_time, cur_burst))
                prev_end_time = prev_end_time + cur_burst"""

    t = 0
    prev=0
    while(True):
        l = []
        #print("mix" , mix)
        for i in range(n):
            if(mix[i][2] <= t and mix[i][1] > 0):
                l.append(mix[i])
        #print("l",l)
        l.sort(key=lambda x: x[3])
        #if(l[0][1] != 0):
        if(len(l)>0):
            if(l[0][0]==prev):
                #print(result[l[0][0]])
                result[l[0][0]][-1][1]+=1
            else:
                result[l[0][0]].append([t,1])
            l[0][1] -= 1
        else:
            break
        prev=l[0][0]
        t = t+1
        #else:
        #    break
    #print(result)
    """for i in result.keys():
        if(len(result[i])==1):
            store=result[i][0]
            result[i]=store"""

    # at the end, all processes executed, so the previous end time is the final completion time
    # this final completion time is used in the plot function for setting the x limit
    print( result)
    return result,  result[n][-1][0]+ result[n][-1][1]


# ------------------------------ TILL HERE ------------------------------------------


def plot(pr_no, arrival, burst, n, priority, gantt_array=None, final_comp_time=None):
    # default syntax, remember it
    # gnt stands for gantt (just for our convenience)
    fig, gnt = plt.subplots()

    # X axis: time
    # Y axis: process number

    # find the gantt array if we don't have a custom one
    if gantt_array == None and final_comp_time == None:
        gantt_array, final_comp_time = find_gantt_array(pr_no, arrival, burst, n, priority)

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


if __name__ == "__main__":

    # User input
    # n = int(input("Enter number of processes: "))

    # pr_no = []
    # burst = []
    # arrival = []
    # print("Enter in form of process_number, arrival, burst")
    # for i in range(n):
    #     x, y, z = map(int, input().split())
    #     pr_no.append(x)
    #     arrival.append(y)
    #     burst.append(z)
    # # sorting everything by arrival time
    
    # findAllTimes(pr_no, arrival, burst, n)
    # plot(pr_no, arrival, burst, n)
    n = 4
    pr_no = [4, 2, 3, 1]
    burst = [7, 3, 4, 5]
    arrival = [3, 1, 2, 0]
    priority = [2,4,1,3]
    pr_no, arrival, burst, priority = sort_by_arrival(pr_no, arrival, burst, n, priority)
    
    
    # 
    #print(find_gantt_array(pr_no, arrival, burst, n))
    findAllTimes(pr_no, arrival, burst, n, priority)
    plot(pr_no, arrival, burst, n, priority)
    """
    plot(
        [1, 2, 3, 4, 5],
        [0, 1, 2, 3, 5],
        [21, 3, 6, 2, 7],
        5,
        {1: [(0, 1), (19, 20)], 2: [(1, 3)], 3: [(6, 6)], 4: [(4, 2)], 5: [(12, 7)]},
        40,
    )"""
