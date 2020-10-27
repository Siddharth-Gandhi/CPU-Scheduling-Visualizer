from flask import Flask, render_template, request

import Algorithms.fcfs as FCFS
import Algorithms.sjf_non_pre as SJFNPE
import Algorithms.sjfpre as SJFPE
import Algorithms.priority as PRIORITY
import Algorithms.rr as RR
import pandas as pd
import math

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def form():
    return render_template("form.html")


@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":
        which_fastest = dict()
        finalRes = []
        speed = int(request.form["speed"])
        n = int(request.form["noOfPr"])
        algoName = request.form.getlist("algo")
        pr_no = list(map(int, request.form["pr_no"].replace(',', ' ').split()))
        arrival = list(
            map(int, request.form["arrival"].replace(',', ' ').split()))
        burst = list(map(int, request.form["burst"].replace(',', ' ').split()))
        if "FCFS" in algoName:
            Tpr_no, Tarrival, Tburst = FCFS.sort_by_arrival(
                pr_no, arrival, burst, n)
            wait, TAT, comp, avgWT, avgTAT = FCFS.findAllTimes(
                Tpr_no, Tarrival, Tburst, n
            )
            FCFS.plot(Tpr_no, Tarrival, Tburst, n, speed)
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
            which_fastest["First Come First Serve"] = [sum(comp)/n, avgWT]
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
            SJFNPE.plot(Tpr_no, Tarrival, Tburst, n, comp, speed)
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
            which_fastest["SJF Non Preemptive"] = [sum(comp)/n, avgWT]
            finalRes.append(temp)

        if "SJFPE" in algoName:
            result = pd.DataFrame()
            result, avgTAT, avgWT = SJFPE.processData(
                n, pr_no, arrival, burst, speed)

            temp = ["SJF Preemptive", sorted(pr_no), list(result["arrival_time"]), list(result["burst_time"]),
                    list(result["waiting_time"]), list(result["turnaround_time"]), list(result["completion_time"]), avgWT, avgTAT]
            which_fastest["SJF Preemptive"] = [sum(comp)/n, avgWT]
            finalRes.append(temp)

        if "Priority" in algoName:
            priority = list(
                map(int, request.form["priority"].replace(',', ' ').split()))
            result = pd.DataFrame()
            result, avgTAT, avgWT = PRIORITY.processData(
                n, pr_no, arrival, burst, priority, speed)

            temp = ["Priority", sorted(pr_no), list(result["arrival_time"]), list(result["burst_time"]),
                    list(result["waiting_time"]), list(result["turnaround_time"]), list(result["completion_time"]), avgWT, avgTAT, priority]
            which_fastest["Priority"] = [sum(comp)/n, avgWT]
            finalRes.append(temp)

        if "RR" in algoName:
            result = pd.DataFrame()
            quantum = int(request.form["timeSlice"])
            result, avgTAT, avgWT = RR.processData(
                n, quantum, pr_no, arrival, burst, speed)

            temp = ["Round Robin", sorted(pr_no), list(result["arrival_time"]), list(result["burst_time"]),
                    list(result["waiting_time"]), list(result["turnaround_time"]), list(result["completion_time"]), avgWT, avgTAT, quantum]
            which_fastest["Round Robin"] = [sum(comp)/n, avgWT]
            finalRes.append(temp)
        print(which_fastest)
        fastest_ct, fastest_ct_name = math.inf, None
        fastest_wt, fastest_wt_name = math.inf, None
        for key, val in which_fastest.items():
            if val[0] < fastest_ct:
                fastest_ct = val[0]
                fastest_ct_name = key
            if val[1] < fastest_wt:
                fastest_wt = val[1]
                fastest_wt_name = key
        return render_template(
            "result.html",
            finalRes=finalRes,
            fastest_ct=fastest_ct,
            fastest_ct_name=fastest_ct_name,
            fastest_wt=fastest_wt,
            fastest_wt_name=fastest_wt_name
        )


if __name__ == "__main__":
    app.run(debug=True)
