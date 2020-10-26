from flask import Flask, render_template, request

import Algorithms.fcfs
import Algorithms.sjf_non_pre
import Algorithms.sjfpre
import Algorithms.priority
import Algorithms.rr

app = Flask(__name__)


@app.route("/")
def form():
    return render_template("form.html")


@app.route("/fcfs/", methods=["POST", "GET"])
def fcfs():
    if request.method == "POST":
        pr_no = request.form["pr_no"]
        arrival = request.form["arrival"]
        burst = request.form["burst"]
        algoName = request.form["algo"]
        return render_template(
            "temp.html", pr_no=pr_no, arrival=arrival, burst=burst, algoName=algoName
        )


# @app.route("/result", methods=["POST", "GET"])
# def result():
#     if request.method == "POST":
#         result = request.form
#         return render_template("result.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)