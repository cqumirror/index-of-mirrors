#!env/bin/python
# coding=utf-8

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/api/mirrors/list")
def get_mirrors_list():
    res = {
        "count": 0,
        "targets": []
    }
    return jsonify(res)


@app.route("/api/mirrors/status")
def get_mirrors_status():
    res = {
        "count": 0,
        "targets": []
    }
    return jsonify(res)


@app.route("/api/mirrors/notice")
def get_mirrors_notice():
    res = {
        "count": 0,
        "targets": []
    }
    return jsonify(res)


@app.after_request
def custom_headers(res):
    res.headers["Server"] = "Bang+"
    return res


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
