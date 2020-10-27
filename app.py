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


@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":
        n = int(request.form["noOfPr"])
        pr_no = list(map(int, request.form["pr_no"].split()))
        arrival = list(map(int, request.form["arrival"].split()))
        burst = list(map(int, request.form["burst"].split()))
        algoName = request.form.getlist("algo")
        print(algoName)
        if algoName == "FCFS":
            pr_no, arrival, burst = FCFS.sort_by_arrival(
                pr_no, arrival, burst, n)
            wait, TAT, comp, avgWT, avgTAT = FCFS.findAllTimes(
                pr_no, arrival, burst, n)
            FCFS.plot(pr_no, arrival, burst, n)
            return render_template(
                "result.html",
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
        # elif algoName == 'SJFPE':


# @app.route("/result", methods=["POST", "GET"])
# def result():
#     if request.method == "POST":
#         result = request.form
#         return render_template("result.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
