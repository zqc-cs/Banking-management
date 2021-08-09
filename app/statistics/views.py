from . import statistics
from flask import render_template, request
from ..models.statistics import statistics_saving, statistics_loan
import json


@statistics.route("/statistics")
def index():
    return render_template("statistics/statistics.html")


@statistics.route("/statistics/do_statistics")
def do_statistics():
    statistics_type = request.args.get("statistics_type")
    begin_time = request.args.get("begin_time")
    end_time = request.args.get("end_time")
    if statistics_type == "saving":
        result_statistics, show_windows, err_msg = statistics_saving(begin_time, end_time)
        result = {}
        result["statistics"] = list(result_statistics)
        result["show_windows"] = show_windows
        result["err_msg"] = err_msg
        result["statistics_type"] = "saving"
        result = json.dumps(result)
        return result
    else:
        result_statistics, show_windows, err_msg = statistics_loan(begin_time, end_time)
        result = {}
        result["statistics"] = list(result_statistics)
        result["show_windows"] = show_windows
        result["err_msg"] = err_msg
        result["statistics_type"] = "loan"
        result = json.dumps(result)
        return result