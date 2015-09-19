#!env/bin/python
# coding=utf-8

import logging
import os.path
import mysql.connector as db_connector

from datetime import datetime
from mysql.connector import errorcode
from flask import Flask, jsonify, request, redirect, g


# Default configuration
LOG_DIR = "log"
APP_NAME = "Actor"

# Create the application
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar("MIRRORS_SETTINGS")


# Create log file
def error_log_file_handler():
    # Create error log file
    log_name = '.'.join([APP_NAME.lower(), "error", "log"])
    if "ERROR_LOG" in app.config:
        log_name = app.config["ERROR_LOG"]
    error_log = os.path.join(LOG_DIR, log_name)

    fh = logging.FileHandler(error_log)
    fh.setLevel(logging.ERROR)
    formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s: %(message)s"
                                      "[in %(pathname)s:%(lineno)d]",
                                  datefmt="%Y-%m-%d %H:%M:%S")
    fh.setFormatter(formatter)
    return fh


app.logger.addHandler(error_log_file_handler())


def connect_db():
    """Connect to the specific database."""
    db_config = dict(user=app.config["DB_USER"],
                     passwd=app.config["DB_PASSWORD"],
                     host=app.config["DB_HOST"],
                     port=app.config["DB_PORT"],
                     db=app.config["DB_DATABASE"])
    conn = db_connector.connect(**db_config)
    return conn


def get_db():
    """Open a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, "mysql_db"):
        g.mysql_db = connect_db()
    return g.mysql_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, "mysql_db"):
        g.mysql_db.close()


@app.route("/api/mirrors/list")
def get_mirrors_list():
    """Return a list of all the mirrors"""
    cursor = get_db().cursor()
    cursor.execute("SELECT name, fullname, protocol, host, path, help, comment FROM mirrors_info")
    res = dict(count=0, targets=[])
    for (name, fullname, protocol, host, path, raw_help, comment) in cursor.fetchall():
        mirror_help = raw_help if raw_help is not None else ''
        mirror_comment = comment if comment is not None else ''
        target = dict(
            name=name,
            fullname=fullname,
            url=''.join([protocol, "://", host, path]),
            help=mirror_help,
            comment=mirror_comment,
            last_update="0000-00-00 00:00:00",
            size="unknown",
            status=500,
            message=''
        )
        # Update last_update, size, status, message from sync log
        prepare_mirrors_status(target)
        res["targets"].append(target)
    res["count"] = len(res["targets"])
    return jsonify(res)


def get_error_message(code):
    rsync_error_refer_table = {
        "0": "Success",
        "1": "Syntax or usage error",
        "2": "Protocol incompatibility",
        "3": "Errors selecting input/output files, dirs",
        "4": "Requested action not supported: an attempt was made to "
             "manipulate 64-bit files on a platform that cannot",
        "5": "Error starting client-server protocol",
        "6": "Daemon unable to append to log-file",
        "10": "Error in socket I/O",
        "11": "Error in file I/O",
        "12": "Error in rsync protocol data stream",
        "13": "Errors with program diagnostics",
        "14": "Error in IPC code",
        "20": "Received SIGUSR1 or SIGINT",
        "21": "Some error returned by waitpid()",
        "22": "Error allocating core memory buffers",
        "23": "Partial transfer due to error",
        "24": "Partial transfer due to vanished source files",
        "25": "The --max-delete limit stopped deletions",
        "30": "Timeout in data send/receive"
    }
    message = ''
    if code in rsync_error_refer_table:
        message = rsync_error_refer_table[code]
    return message


def format_size(size):
    return round(float(size) / (1024 * 1024), 2)


def prepare_mirrors_status(target):
    """Update mirrors' last_update, size, status, message property"""
    mirror_log = '.'.join([target["name"], "log"])
    mirror_log_path = os.path.join(app.config["SYNC_LOG_DIR"], mirror_log)
    try:
        with open(mirror_log_path, 'r') as f:
            lines = f.readlines()
            length = len(lines)
            if length <= 1:
                return

            # 0: yyyyMMdd 1: HH:mm:ss
            # 2: SyncStart | SyncSuccd | SyncError | SyncCompt
            # 3: Size or Return code
            last_line_values = lines[-1].rstrip().split(" - ")
            second_last_values = lines[-2].rstrip().split(" - ")
            stage = last_line_values[2]

            time_old_format = "%Y%m%d %H:%M:%S"
            time_new_format = "%Y-%m-%d %H:%M:%S"

            if stage == "SyncCompt":
                time = ' '.join([last_line_values[0], last_line_values[1]])
                target["last_update"] = datetime.strptime(time, time_old_format).strftime(time_new_format)
                target["size"] = ''.join([str(format_size(int(last_line_values[3]))), 'G'])   # KB to GB
                if second_last_values[-2] == "SyncError":
                    error_code = second_last_values[3]
                    error_message = get_error_message(error_code)
                    target["message"] = \
                        "Error code: {} - {}".format(error_code, error_message)
                    target["status"] = 400
                else:
                    target["message"] = ''
                    target["status"] = 200

            if stage == "SyncStart":
                time = ' '.join([second_last_values[0], second_last_values[1]])
                target["last_update"] = datetime.strptime(time, time_old_format).strftime(time_new_format)
                target["size"] = ''.join([str(format_size(int(last_line_values[3]))), 'G'])   # KB to GB
                target["message"] = ''
                target["status"] = 100
    except IOError:
        target["message"] = "Fail to read sync log file."
        target["status"] = 500


@app.route("/api/mirrors/status")
def get_mirrors_status():
    cursor = get_db().cursor()
    cursor.execute("SELECT name FROM mirrors_info")
    res = dict(count=0, targets=[])
    for (name,) in cursor.fetchall():
        # Only name in row
        target = dict(
            name=name,
            last_update="0000-00-00 00:00:00",
            size="unknown",
            status=500,
            message=''
        )
        prepare_mirrors_status(target)
        res["targets"].append(target)
    res["count"] = len(res["targets"])
    return jsonify(res)


@app.route("/api/mirrors/notices")
def get_mirrors_notices():
    res = {
        "count": 2,
        "targets": [{"created_at": "2015-08-21 01:02:00", "notice": "这是第一条公告: 你好,地球"},
                    {"created_at": "2015-08-21 11:02:00", "notice": "这是第二条公告: Beta 测试"}]
    }
    return jsonify(res)


def format_version(version):
    if '-' not in version:
        return version

    # Target format: 7.1 (x86_64, Minimal, ...)
    values = version.split('-')
    version_f = "{} ({})".format(values[0], ", ".join(values[1:]))
    return version_f


@app.route("/api/mirrors/oses")
def get_mirrors_oses():
    cursor = get_db().cursor()
    cursor.execute("SELECT DISTINCT name FROM mirrors_downloads WHERE type = %s", ("os",))
    names = [name for (name,) in cursor]
    res = dict(count=0, targets=[])
    for name in names:
        os = dict(
            name=name,
            fullname="",
            url="",
            type="os",
            count=0,
            versions=[]
        )
        # Find all links for kinds of versions of the os
        cursor.execute("SELECT fullname, protocol, host, dir, path, version "
                       "FROM mirrors_downloads WHERE name = %s", (name,))
        for (fullname, protocol, host, directory, path, raw_version) in cursor.fetchall():
            base_dir = ''.join([protocol, "://", host, directory])
            url = ''.join([protocol, "://", host, path])
            version_f = format_version(raw_version)
            version = dict(version=version_f, url=url)
            os["versions"].append(version)
            # TODO(@Zhiqiang He): Find a better method to update fullname and url
            os["fullname"] = fullname
            os["url"] = base_dir
        os["count"] = len(os["versions"])
        # Append the os to list
        res["targets"].append(os)
    res["count"] = len(res["targets"])
    return jsonify(res)


@app.route("/api/mirrors/osses")
def get_mirrors_osses():
    return jsonify(dict(count=0, targets=[]))


@app.after_request
def custom_headers(res):
    res.headers["Server"] = APP_NAME
    return res


# Start DEBUG
# Handle static files for debug
@app.before_request
def add_static():
    if not app.debug:
        return
    path = request.path
    if path == "/":
        return redirect("/static/index.html")


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
