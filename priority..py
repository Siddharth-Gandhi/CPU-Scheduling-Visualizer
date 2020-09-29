print("Siddharth Gandhi 19BCE0005")

if __name__ == "__main__":
    print("Enter the number of processess: ")
    n=int(input())
    processes=[]
    for i in range(0,n):
        processes.insert(i,i+1)
    print("Enter the burst time of the processes: ")
    bt=list(map(int, input().split()))
    print("Enter the priority of the processes: ")
    priority=list(map(int, input().split()))
    tat,wt=[], []
    for i in range(0,len(priority)-1):
        for j in range(0,len(priority)-i-1):
            if(priority[j]>priority[j+1]):
                swap=priority[j]
                priority[j]=priority[j+1]
                priority[j+1]=swap

                swap=bt[j]
                bt[j]=bt[j+1]
                bt[j+1]=swap

                swap=processes[j]
                processes[j]=processes[j+1]
                processes[j+1]=swap
    wt.insert(0,0)
    tat.insert(0,bt[0])
    for i in range(1,len(processes)):
        wt.insert(i,wt[i-1]+bt[i-1])
        tat.insert(i,wt[i]+bt[i])
    avgtat=0
    avgwt=0
    for i in range(0,len(processes)):
        avgwt=avgwt+wt[i]
        avgtat=avgtat+tat[i]
    avgwt=float(avgwt)/n
    avgtat=float(avgtat)/n
    print("Process\t  Burst Time\t  Waiting Time\t  Turn Around Time")
    for i in range(0,n):
        print(str(processes[i])+"\t\t"+str(bt[i])+"\t\t"+str(wt[i])+"\t\t"+str(tat[i]))
    print("Average Waiting time is: "+str(avgwt))
    print("Average Turn Around Time is: "+str(avgtat))
