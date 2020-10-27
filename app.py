from flask import Flask, render_template, request

import Algorithms.fcfs as FCFS
import Algorithms.sjf_non_pre
import Algorithms.sjfpre
import Algorithms.priority
import Algorithms.rr

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def form():
    return render_template("form.html")


@app.route("/fcfs/", methods=["POST", "GET"])
def fcfs():
    if request.method == "POST":
        n = int(request.form["noOfPr"])
        print(n)
        pr_no = list(map(int, request.form["pr_no"].split()))
        print(pr_no)
        arrival = list(map(int, request.form["arrival"].split()))
        print(arrival)
        burst = list(map(int, request.form["burst"].split()))
        print(burst)
        algoName = request.form["algo"]
        if algoName == "FCFS":
<<<<<<< HEAD
            pr_no, arrival, burst = FCFS.sort_by_arrival(
                pr_no, arrival, burst, n)
            FCFS.findAllTimes(pr_no, arrival, burst, n)
            FCFS.plot(pr_no, arrival, burst, n)
        # return render_template(
        #     "temp.html", pr_no=pr_no, arrival=arrival, burst=burst, algoName=algoName
        # )
=======
            pr_no, arrival, burst = FCFS.sort_by_arrival(pr_no, arrival, burst, n)
            wait, TAT, comp, avgWT, avgTAT = FCFS.findAllTimes(pr_no, arrival, burst, n)
            FCFS.plot(pr_no, arrival, burst, n)
        return render_template(
            "fcfs.html",
            pr_no=pr_no,
            arrival=arrival,
            burst=burst,
            algoName=algoName,
            wait=wait,
            tat=TAT,
            comp=comp,
            avgWT=avgWT,
            avgTAT=avgTAT,
        )
>>>>>>> 1318ebfbdd7e3d27640ee6a1f15006c39c643605


# @app.route("/result", methods=["POST", "GET"])
# def result():
#     if request.method == "POST":
#         result = request.form
#         return render_template("result.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
