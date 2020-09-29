import matplotlib.pyplot as plt
import random


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


def find_gantt_array(pr_no, arrival, burst, n):
    wait = [0 for i in range(n)]
    TAT = [0 for i in range(n)]
    total_wt = 0
    total_tat = 0
    comp = [0 for i in range(n)]
    comp[0] = burst[0] + arrival[0]
    TAT[0] = comp[0] - arrival[0]
    wait[0] = TAT[0] - burst[0]
    prevCompTime = 0
    for i in range(1, n):
        prevCompTime = comp[i - 1]  # previous com
        pr_no, arrival, burst = customSort(pr_no, arrival, burst, n, i, prevCompTime)
        if comp[i - 1] < arrival[i]:
            comp[i] = burst[i] + arrival[i]
        else:
            comp[i] = comp[i - 1] + burst[i]
        TAT[i] = comp[i] - arrival[i]
        wait[i] = TAT[i] - burst[i]

    result = {pr: [] for pr in pr_no}
    for i in range(n):
        if i == 0:
            result[pr_no[i]].append((arrival[i], burst[i]))
        else:
            result[pr_no[i]].append((comp[i - 1], burst[i]))

    print("\npr_no\tburst\tarrival\tcomp\t TAT\t wait")
    for i in range(n):
        total_wt += wait[i]
        total_tat += TAT[i]
        # comp = TAT[i] + arrival[i]
        print(
            pr_no[i],
            "\t",
            burst[i],
            "\t",
            arrival[i],
            "\t",
            comp[i],
            "\t",
            TAT[i],
            "\t",
            wait[i],
        )
    print("\nAverage waiting time = ", (total_wt / n))
    print("Average turn around time = ", total_tat / n, "\n")
    return result, comp[n - 1]


def sort_by_arrival(pr_no, arrival, burst, n):

    mix = list(zip(pr_no, arrival, burst))
    mix.sort(key=lambda x: (x[1], x[2]))

    pr_no = [x[0] for x in mix]
    arrival = [x[1] for x in mix]
    burst = [x[2] for x in mix]

    return pr_no, arrival, burst


def get_cmap(n, name="hsv"):

    return plt.cm.get_cmap(name, n)


def find_gantt_array(pr_no, arrival, burst, n):

    return findAllTimes(pr_no, arrival, burst, n)


def plot(pr_no, arrival, burst, n, gantt_array=None, final_comp_time=None):

    fig, gnt = plt.subplots()

    if gantt_array == None and final_comp_time == None:
        gantt_array, final_comp_time = find_gantt_array(pr_no, arrival, burst, n)

    gnt.set_ylim(0, 1)

    gnt.set_xlim(0, final_comp_time + 3)

    gnt.set_xlabel("Seconds since start")
    # gnt.set_ylabel("Process number")

    # gnt.set_yticks([i + 0.5 for i in pr_no])

    # gnt.set_yticklabels(pr_no)

    gnt.grid(True)

    cmap = get_cmap(n + 1)
    for i in pr_no:
        gnt.broken_barh(gantt_array[i], (0, 1), facecolor=cmap(i))
    plt.show()


if __name__ == "__main__":
    n = 5
    pr_no = [1, 2, 3, 4, 5]
    burst = [6, 8, 7, 3, 2]
    arrival = [10, 0, 7, 4, 10]
    pr_no, arrival, burst = sort_by_arrival(pr_no, arrival, burst, n)
    find_gantt_array(pr_no, arrival, burst, n)
    plot(pr_no, arrival, burst, n)
