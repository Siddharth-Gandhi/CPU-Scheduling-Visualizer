import os
import random
import matplotlib.animation as animation
import mpld3
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")

# TAT: turn around time

# ----------- FOR FINDING THE TABLE -----------------
# EDIT THIS


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


# --------------------- TILL HERE --------------------------------


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


# ------------------------- FOR FINDING THE DICTIONARY -----------------------------
# EDIT THIS
def find_gantt_array(pr_no, arrival, burst, n):
    mix = list(zip(pr_no, arrival, burst))
    # print(mix)
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


# ------------------------------ TILL HERE ------------------------------------------


def plot(pr_no, arrival, burst, n, speed, gantt_array=None, final_comp_time=None):
    # default syntax, remember it
    # gnt stands for gantt (just for our convenience)
    fig, gnt = plt.subplots()

    # X axis: time
    # Y axis: process number

    # find the gantt array if we don't have a custom one
    if gantt_array == None and final_comp_time == None:
        gantt_array, final_comp_time = find_gantt_array(
            pr_no, arrival, burst, n)
    # print(gantt_array)
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
    plt.title('FCFS')

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
        "static\\gifs\\First Come First Serve.gif",
        writer="pillow"
    )


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
    # pr_no, arrival, burst = sort_by_arrival(pr_no, arrival, burst, n)
    # findAllTimes(pr_no, arrival, burst, n)
    # plot(pr_no, arrival, burst, n)
    n = 7
    pr_no = [3, 4, 5, 6, 7, 1, 2]
    arrival = [3, 7, 8, 15, 25, 0, 2]
    burst = [10, 1, 5, 2, 7, 3, 6]
    pr_no, arrival, burst = sort_by_arrival(pr_no, arrival, burst, n)
    findAllTimes(pr_no, arrival, burst, n)
    plot(pr_no, arrival, burst, n, 50)
