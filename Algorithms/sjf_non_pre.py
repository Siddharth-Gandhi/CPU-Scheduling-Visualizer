import matplotlib.pyplot as plt
import matplotlib.animation as animation


# This function is used to sort by burst timeand check if the process has arrived
def customSort(pr_no, arrival, burst, n, startFrom, prevCompTime):
    mix = list(zip(pr_no, arrival, burst))
    mix = (
        mix[:startFrom]
        + sorted(
            filter(lambda x: x[1] <= prevCompTime, mix[startFrom:]), key=lambda x: x[2]
        )
        + list(filter(lambda x: x[1] > prevCompTime, mix[startFrom:]))
    )

    pr_no = [x[0] for x in mix]
    arrival = [x[1] for x in mix]
    burst = [x[2] for x in mix]

    return pr_no, arrival, burst


def findAllTimes(pr_no, arrival, burst, comp, n):
    wait = [0 for i in range(n)]
    TAT = [0 for i in range(n)]
    total_wt = 0
    total_tat = 0
    comp[0] = burst[0] + arrival[0]
    TAT[0] = comp[0] - arrival[0]
    wait[0] = TAT[0] - burst[0]
    prevCompTime = 0
    for i in range(1, n):
        prevCompTime = comp[i - 1]  # completion time of previous process
        pr_no, arrival, burst = customSort(
            pr_no, arrival, burst, n, i, prevCompTime)
        if comp[i - 1] < arrival[i]:
            comp[i] = burst[i] + arrival[i]
        else:
            comp[i] = comp[i - 1] + burst[i]
        TAT[i] = comp[i] - arrival[i]
        wait[i] = TAT[i] - burst[i]

    # print("\npr_no\tburst\tarrival\tcomp\t TAT\t wait")
    for i in range(n):
        total_wt += wait[i]
        total_tat += TAT[i]
        # print(
        #     pr_no[i],
        #     "\t",
        #     burst[i],
        #     "\t",
        #     arrival[i],
        #     "\t",
        #     comp[i],
        #     "\t",
        #     TAT[i],
        #     "\t",
        #     wait[i],
        # )
    avgWT = total_wt / n
    avgTAT = total_tat / n
    # print("\nAverage waiting time = ", (total_wt / n))
    # print("Average turn around time = ", total_tat / n, "\n")
    return pr_no, arrival, burst, comp, wait, TAT, avgWT, avgTAT
    # Returns the order in which the processes execute and corresponding values of arrival,
    # burst and completion time


def sort_by_arrival(pr_no, arrival, burst, n):

    mix = list(zip(pr_no, arrival, burst))
    mix.sort(key=lambda x: (x[1], x[2]))

    pr_no = [x[0] for x in mix]
    arrival = [x[1] for x in mix]
    burst = [x[2] for x in mix]

    return pr_no, arrival, burst


def get_cmap(n, name="hsv"):

    return plt.cm.get_cmap(name, n)


def find_gantt_array(pr_no, arrival, burst, comp, n):

    result = {pr: [] for pr in pr_no}
    for i in range(n):
        if i == 0:
            # For the first process to execute, add its arrival and burst time to
            # the corresponding process no. in the result dictionary
            result[pr_no[i]].append((arrival[i], burst[i]))
        else:
            # For subsequent processes,
            if comp[i - 1] < arrival[i]:
                # Add arrival time if current arrival time is greater than the previous
                # completion time
                result[pr_no[i]].append((arrival[i], burst[i]))
            else:
                # Add completion time of previous process and burst time in all other cases
                result[pr_no[i]].append((comp[i - 1], burst[i]))
    return result, comp[n - 1]


def plot(pr_no, arrival, burst, n, comp, gantt_array=None, final_comp_time=None):

    fig, gnt = plt.subplots()

    if gantt_array == None and final_comp_time == None:
        gantt_array, final_comp_time = find_gantt_array(
            pr_no, arrival, burst, comp, n)

    # print(gantt_array)
    gnt.set_ylim(0, n + 2)

    gnt.set_xlim(0, final_comp_time + 3)

    gnt.set_xlabel("Seconds since start")
    gnt.set_ylabel("Process number")

    gnt.set_yticks([i + 0.5 for i in pr_no])

    gnt.set_yticklabels(pr_no)

    gnt.grid(True)

    cmap = get_cmap(n + 1)
    # Static plotting
    # for i in pr_no:
    #     gnt.broken_barh(gantt_array[i], (i, 1), facecolor=cmap(i))
    # plt.show()
    plt.title('SJF Non Preemptive')

    def find(t):
        for i in gantt_array:
            for j in gantt_array[i]:
                if j[0] <= t <= j[0] + j[1]:
                    return i, [(t, 1)]
        return -1

    def animate(i):
        if find(i) != -1:
            pr, time = find(i)
            gnt.broken_barh(time, (pr, 1), facecolor=cmap(pr))

    anim = animation.FuncAnimation(
        fig, animate, frames=final_comp_time, interval=200)
    anim.save(
        "static\\gifs\\SJF Non Preemptive.gif",
        writer="pillow",
        fps=60,
    )
    # plt.show()


if __name__ == "__main__":
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
    n = 5
    pr_no = [1, 2, 3, 4, 5]
    burst = [6, 2, 7, 3, 2]
    arrival = [10, 1, 7, 4, 10]
    comp = [0 for i in range(n)]  # The completion time of all processes
    pr_no, arrival, burst = sort_by_arrival(pr_no, arrival, burst, n)
    pr_no, arrival, burst, comp, wait, TAT, avgWT, avgTAT = findAllTimes(
        pr_no, arrival, burst, comp, n
    )
    plot(pr_no, arrival, burst, n, comp)
