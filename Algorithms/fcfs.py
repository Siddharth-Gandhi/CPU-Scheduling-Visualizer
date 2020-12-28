import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import matplotlib.animation as animation
import mpld3
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")

# TAT: turn around time


def findWT(pr_no, arrival, burst, n, wait):
    service = [0 for i in range(n)]
    service[0] = 0
    wait[0] = 0
    for i in range(1, n):
        service[i] = service[i - 1] + burst[i - 1]
        wait[i] = service[i] - arrival[i]
        if wait[i] < 0:
            wait[i] = 0


def findTAT(pr_no, burst, wait, TAT):
    for i in range(len(pr_no)):
        TAT[i] = wait[i] + burst[i]


def findAllTimes(pr_no, arrival, burst, n):
    wait = [0 for i in range(n)]
    TAT = [0 for i in range(n)]
    comp = [0 for i in range(n)]
    total_wt = 0
    total_tat = 0
    findWT(pr_no, arrival, burst, n, wait)
    findTAT(pr_no, burst, wait, TAT)
    # print("\npr_no\tburst\tarrival\tcomp\t TAT\t wait")
    for i in range(n):
        total_wt += wait[i]
        total_tat += TAT[i]
        comp[i] = TAT[i] + arrival[i]
        # print(
        #     i + 1,
        #     "\t",
        #     burst[i],
        #     "\t",
        #     arrival[i],
        #     "\t",
        #     comp[i],
        #     "\t ",
        #     TAT[i],
        #     "\t ",
        #     wait[i],
        # )
    avgWT = total_wt / n
    avgTAT = total_tat / n
    # print("\nAverage waiting time = ", (total_wt / n))
    # print("Average turn around time = ", total_tat / n, "\n")
    return wait, TAT, comp, avgWT, avgTAT


def sort_by_arrival(pr_no, arrival, burst, n):
    # mix them all up in 1 function and then sort by arrival
    mix = list(zip(pr_no, arrival, burst))
    # thanks python for such ez sorting
    mix.sort(key=lambda x: x[1])

    pr_no = [x[0] for x in mix]
    arrival = [x[1] for x in mix]
    burst = [x[2] for x in mix]

    return pr_no, arrival, burst


def get_cmap(n, name="hsv"):
    """Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name."""
    return plt.cm.get_cmap(name, n)


def find_gantt_array(pr_no, arrival, burst, n):
    mix = list(zip(pr_no, arrival, burst))
    # Note: mix is already sorted by arrival before function call

    result = {pr: [] for pr in pr_no}

    for i in range(n):
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
                prev_end_time = prev_end_time + cur_burst

    # at the end, all processes executed, so the previous end time is the final completion time
    # this final completion time is used in the plot function for setting the x limit
    return result, prev_end_time


def plot(pr_no, arrival, burst, n, gantt_array=None, final_comp_time=None):
    # default syntax, remember it
    # gnt stands for gantt (just for our convenience)
    fig, gnt = plt.subplots()

    # X axis: time
    # Y axis: process number

    # find the gantt array if we don't have a custom one
    if gantt_array == None and final_comp_time == None:
        gantt_array, final_comp_time = find_gantt_array(
            pr_no, arrival, burst, n)
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
        return -1

    def animate(i):
        # find pr (process number), time is just i (current frame = current second), but to plot it we need to have it in list of tuple form
        if find(i) != -1:
            pr, time = find(i)
            gnt.broken_barh(time, (pr, 1), facecolor=cmap(pr))

    # idk what the hell this is, just know that animate will plot the function for every frame
    # frames is total frames, ie total time completed we'll take
    # frames = final_comp_time will just work as range(final_comp_time)
    # intervals controls speed, idk how
    anim = animation.FuncAnimation(
        fig, animate, frames=final_comp_time, interval=150)

    plt.show()
# ------------------------------ TILL HERE ------------------------------------------


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

    # sorting everything by arrival time
    # pr_no, arrival, burst = sort_by_arrival(pr_no, arrival, burst, n)

    # findAllTimes(pr_no, arrival, burst, n)
    # plot(pr_no, arrival, burst, n)

    # Sample input
    n = 7
    pr_no = [3, 4, 5, 6, 7, 1, 2]
    arrival = [3, 7, 8, 15, 25, 0, 2]
    burst = [10, 1, 5, 2, 7, 3, 6]
    pr_no, arrival, burst = sort_by_arrival(pr_no, arrival, burst, n)
    findAllTimes(pr_no, arrival, burst, n)
    plot(pr_no, arrival, burst, n)
