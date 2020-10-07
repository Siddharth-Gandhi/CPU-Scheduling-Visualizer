import matplotlib.animation as animation
import matplotlib.pyplot as plt
import random

def get_cmap(n, name="hsv"):
    """Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name."""
    return plt.cm.get_cmap(name, n)

def sort_by_arrival(pr_no, arrival, burst, n):
    # mix them all up in 1 function and then sort by arrival
    mix = list(zip(pr_no, arrival, burst))
    # thanks python for such ez sorting
    mix.sort(key=lambda x: x[1])

    pr_no = [x[0] for x in mix]
    arrival = [x[1] for x in mix]
    burst = [x[2] for x in mix]

    return pr_no, arrival, burst


n = 7
pr_no = [3,4,5,6,7,1,2]
arrival = [3,7,8,15,25,0,2]
burst = [10,1,5,2,7,3,6]
pr_no, arrival, burst = sort_by_arrival(pr_no, arrival, burst, n)
gantt_array = {1: [(0, 3)], 2: [(3, 6)], 3: [(9, 10)], 4: [(19, 1)], 5: [(20, 5)], 6: [(25, 2)], 7: [(27, 7)]}
final_comp_time = 34

fig, gnt = plt.subplots()

# X axis: time
# Y axis: process number

# find the gantt array if we don't have a custom one
# if gantt_array == None and final_comp_time == None:
#     gantt_array, final_comp_time = find_gantt_array(pr_no, arrival, burst, n)

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

cmap = get_cmap(n + 1)

def find(t):
    for i in gantt_array:
        for j in gantt_array[i]:
            if j[0] <= t <= j[0] + j[1]:
                # if t + 1 <= j[0] + j[1]:
                return i, [(t, 1)]
                # else:
                #     return i, [(t, 0)]

def animate(i):
    pr, lot = find(i)
    # print(pr)
    # gnt.cla()
    gnt.broken_barh(lot, (pr, 1), facecolor=cmap(pr))

# Static plotting
# for i in pr_no:
#     # generating a random color
#     # r = random.random()
#     # b = random.random()
#     # g = random.random()
#     # color = (r, g, b)
#     gnt.broken_barh(gantt_array[i], (i, 1), facecolor=cmap(i))

anim = animation.FuncAnimation(fig, animate, frames=final_comp_time, interval= 50)
plt.show()
