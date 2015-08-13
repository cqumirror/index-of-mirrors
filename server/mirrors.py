#!env/bin/python
# coding=utf-8

from flask import Flask, jsonify, request, redirect

app = Flask(__name__)
LOG_DIR = "/www/mirrors/log"


@app.route("/api/mirrors/list")
def get_mirrors_list():
    res = {
        "count": 0,
        "targets": []
    }
    return jsonify(res)


@app.route("/api/mirrors/status")
def get_mirrors_status():

    return jsonify(res)


@app.route("/api/mirrors/notice")
def get_mirrors_notice():
    res = {
        "count": 0,
        "targets": []
    }
    return jsonify(res)


@app.route("/api/mirrors/downloads")
def get_mirrors_downloads():
    res = {
        "count": 0,
        "targets": []
    }
    return jsonify(res)


"""Handle static files for debug"""
@app.before_request
def add_static():
    if not app.debug:
        return
    path = request.path
    if path == "/":
        return redirect("/static/index.html")


@app.after_request
def custom_headers(res):
    res.headers["Server"] = "Bang+"
    return res


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
