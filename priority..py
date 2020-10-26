import matplotlib.pyplot as plt
import matplotlib.animation as animation
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
    service = [0] * n
  
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
    # # Static plotting
    # for i in pr_no:
    #     # generating a random color
    #     # r = random.random()
    #     # b = random.random()
    #     # g = random.random()
    #     # color = (r, g, b)
    #     gnt.broken_barh(gantt_array[i], (i, 1), facecolor=cmap(i))

# ------------------------- ANIMATION -----------------------------
# JUST ADD THIS PART IN PLOT FUNCTION FOR ANIMATING
    # Animation function

    # you all don't need to bother about this most probably, but still if you want to know how it works

    # here our frame is 1 second. so we will be plotting every second, but we can adjust the speed to make it faster

    def find(t):
        # THE ENTIRE POINT OF THIS FUNCTION IS TO JUST FIND THE PROCESS NUMBER EXECUTING AT TIME t
        # this is an absolutely inefficient function to find the pr_no that is going on at the time t
        # just iterate through everything and check
        # i'm sure that there's a more efficient way of doing this but i can't be bothered to think about it rn
        # y'all can suggest a better algorithm if you want
        for i in gantt_array:
            # i will be all the keys in gantt_array = pr_no
            for j in gantt_array[i]:
                # iterate through the list of tuples (j) until we find a process such that t lies b/w start time, start time +
                # amount of time the process is executing
                if j[0] <= t <= j[0] + j[1]:
                    # return in this form to make life easier for plotting (broken_barh)
                    return i, [(t, 1)]

    def animate(i):
        # find pr (process number), time is just i (current frame = current second), but to plot it we need to have it in list of tuple form
        pr, time = find(i)
        gnt.broken_barh(time, (pr, 1), facecolor=cmap(pr))

    # idk what the hell this is, just know that animate will plot the function for every frame
    # frames is total frames, ie total time completed we'll take
    # frames = final_comp_time will just work as range(final_comp_time)
    # intervals controls speed, idk how
    anim = animation.FuncAnimation(
        fig, animate, frames=final_comp_time, interval=50)

    plt.show()
# ------------------------------ TILL HERE ------------------------------------------


if __name__ == "__main__":

    #n = int(input('Enter number of processes: '))
    #pr_no = list(map(int,input('Enter the order of process number: ').split()))
    #burst = list(map(int,input("Enter burst time of each process : ").split()))
    #arrival = list(map(int,input("Enter arrival time of each process : ").split()))
    #priority = list(map(int,input("Enter priority of each process: ").split()))

    n = 7
    pr_no = [3, 4, 5, 6, 7, 1, 2]
    arrival = [3, 7, 8, 15, 25, 0, 2]
    burst = [10, 1, 5, 2, 7, 3, 6]
    priority = [4, 2, 3, 5, 7, 1, 6]
    pr_no, arrival, burst, priority = sort_by_arrival(pr_no, arrival, burst, n, priority)
    
    
    # 
    #print(find_gantt_array(pr_no, arrival, burst, n))
    findAllTimes(pr_no, arrival, burst, n, priority)
    plot(pr_no, arrival, burst, n, priority)
    
