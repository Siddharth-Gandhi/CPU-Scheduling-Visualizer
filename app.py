from flask import Flask, render_template, request

import Algorithms.fcfs as FCFS
import Algorithms.sjf_non_pre as SJFNPE
import Algorithms.sjfpre as SJFPE
import Algorithms.priority as PRIORITY
import Algorithms.rr as RR
import pandas as pd

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def form():
    return render_template("form.html")


@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":
        finalRes = []
        n = int(request.form["noOfPr"])
        algoName = request.form.getlist("algo")
        pr_no = list(map(int, request.form["pr_no"].split()))
        arrival = list(map(int, request.form["arrival"].split()))
        burst = list(map(int, request.form["burst"].split()))
        if "FCFS" in algoName:
            Tpr_no, Tarrival, Tburst = FCFS.sort_by_arrival(
                pr_no, arrival, burst, n)
            wait, TAT, comp, avgWT, avgTAT = FCFS.findAllTimes(
                Tpr_no, Tarrival, Tburst, n
            )
            FCFS.plot(Tpr_no, Tarrival, Tburst, n)
            temp = [
                "First Come First Serve",
                Tpr_no,
                Tarrival,
                Tburst,
                wait,
                TAT,
                comp,
                avgWT,
                avgTAT,
            ]
            finalRes.append(temp)

        if "SJFNPE" in algoName:
            # The completion time of all processes
            comp = [0 for i in range(n)]
            Tpr_no, Tarrival, Tburst = SJFNPE.sort_by_arrival(
                pr_no, arrival, burst, n)
            (
                Tpr_no,
                Tarrival,
                Tburst,
                comp,
                wait,
                TAT,
                avgWT,
                avgTAT,
            ) = SJFNPE.findAllTimes(Tpr_no, Tarrival, Tburst, comp, n)
            SJFNPE.plot(Tpr_no, Tarrival, Tburst, n, comp)
            temp = [
                "SJF Non Preemptive",
                Tpr_no,
                Tarrival,
                Tburst,
                wait,
                TAT,
                comp,
                avgWT,
                avgTAT,
            ]
            finalRes.append(temp)

        # if "SJFPE" in algoName:
        #     pr_no, arrival, burst = SJFPE.sort_by_arrival(pr_no, arrival, burst, n)
        #     wait, TAT, avgWT, avgTAT = SJFPE.findAllTimes(pr_no, arrival, burst, n)
        #     SJFPE.plot(pr_no, arrival, burst, n)
        #     comp = ["-" for x in range(n)]
        #     temp = ["SJFPE", pr_no, arrival, burst, wait, TAT, comp, avgWT, avgTAT]
        #     finalRes.append(temp)

        if "Priority" in algoName:
            priority = list(map(int, request.form["priority"].split()))
            Tpr_no, Tarrival, Tburst, Tpriority = PRIORITY.sort_by_arrival(
                pr_no, arrival, burst, n, priority
            )
            wait, TAT, avgWT, avgTAT = PRIORITY.findAllTimes(
                Tpr_no, Tarrival, Tburst, n, Tpriority
            )
            PRIORITY.plot(Tpr_no, Tarrival, Tburst, n, Tpriority)
            comp = ["-" for x in range(n)]
            temp = [
                "Priority",
                Tpr_no,
                Tarrival,
                Tburst,
                wait,
                TAT,
                comp,
                avgWT,
                avgTAT,
                Tpriority,
            ]
            finalRes.append(temp)

        if "RR" in algoName:
            result = pd.DataFrame()
            quantum = int(request.form["timeSlice"])
            result, avgTAT, avgWT = RR.processData(
                n, quantum, pr_no, arrival, burst)
            temp = ["Round Robin", sorted(pr_no), list(result["arrival_time"]), list(result["burst_time"]),
                    list(result["waiting_time"]), list(result["turnaround_time"]), list(result["completion_time"]), avgWT, avgTAT]
            finalRes.append(temp)

        return render_template(
            "result.html",
            finalRes=finalRes
        )


if __name__ == "__main__":
    app.run(debug=True)
