# coding=utf-8

import logging
import os.path

from actor import app
from datetime import datetime
from flask import jsonify
from domains import db, MirrorsInfo, MirrorsResources


# create log file
def error_log_file_handler():
    # create error log file
    log_name = '.'.join([app.config["APP_NAME"].lower(), "error", "log"])
    if "ERROR_LOG" in app.config:
        log_name = app.config["ERROR_LOG"]
    error_log = os.path.join(app.config["LOG_DIR"], log_name)

    fh = logging.FileHandler(error_log)
    fh.setLevel(logging.ERROR)
    formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s: %(message)s"
                                      "[in %(pathname)s:%(lineno)d]",
                                  datefmt="%Y-%m-%d %H:%M:%S")
    fh.setFormatter(formatter)
    return fh


app.logger.addHandler(error_log_file_handler())


@app.route("/api/mirrors/list")
def get_mirrors_list():
    """Return a list of all the mirrors."""
    mirrors = MirrorsInfo.query.order_by(MirrorsInfo.name)
    res = dict(count=0, targets=[])
    for mirror in mirrors:
        mirror_help = mirror.help if mirror.help is not None else ''
        mirror_comment = mirror.comment if mirror.comment is not None else ''
        target = dict(
            name=mirror.name,
            fullname=mirror.fullname,
            url=''.join([mirror.protocol, "://", mirror.host, mirror.path]),
            help=mirror_help,
            comment=mirror_comment,
            last_update="????-??-?? ??:??:??",
            size="unknown",
            status=500,
            message=''
        )
        # update last_update, size, status, message from sync log
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
    """Update mirrors' last_update, size, status, message property."""
    mirror_log = '.'.join([target["name"], "log"])
    mirror_log_path = os.path.join(app.config["SYNC_LOG_DIR"], mirror_log)
    try:
        with open(mirror_log_path, 'r') as f:
            lines = f.readlines()

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
    except IndexError:
        target["message"] = "Invalid sync log format."
        target["status"] = 500


@app.route("/api/mirrors/status")
def get_mirrors_status():
    mirrors = MirrorsInfo.query.all()
    res = dict(count=0, targets=[])
    for mirror in mirrors:
        # Only name in row
        target = dict(
            name=mirror.name,
            last_update="????-??-?? ??:??:??",
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
        "count": 3,
        "targets": [{"created_at": "2015-08-21 01:02:00", "notice": "这是第一条公告: 你好,地球"},
                    {"created_at": "2015-08-21 11:02:00", "notice": "这是第二条公告: doing..."},
                    {"created_at": "2015-10-27 11:02:00", "notice": "这是第三条公告: deploy successfully"}]
    }
    return jsonify(res)


def format_version(version):
    if '-' not in version:
        return version

    # target format: 7.1 (x86_64, Minimal, ...)
    values = version.split('-')
    version_f = "{} ({})".format(values[0], ", ".join(values[1:]))
    return version_f


@app.route("/api/mirrors/oses")
def get_mirrors_oses():
    res = dict(count=0, targets=[])
    # query all the oses
    query = db.session.query(MirrorsResources.name).distinct().filter(MirrorsResources.type == "os")
    os_names = [row.name for row in query.all()]

    for os_name in os_names:
        # fetch all versions of the os
        os_versions = MirrorsResources.query.filter_by(type="os", name=os_name).all()

        # prepare the os object
        o_s_f = dict(name=os_name, fullname='', type="os", url='', versions=[], count=0)

        for (idx, o_s) in enumerate(os_versions):
            # init the os object
            if idx == 0:
                o_s_f["fullname"] = o_s.fullname
                o_s_f["url"] = ''.join([o_s.protocol, "://", o_s.host, o_s.dir])

            # add new version of the os
            os_version_f = format_version(o_s.version)
            os_version_url = ''.join([o_s.protocol, "://", o_s.host, o_s.path])
            version = dict(version=os_version_f, url=os_version_url)
            o_s_f["versions"].append(version)
        # update count of the os's version object
        o_s_f["count"] = len(o_s_f["versions"])
        res["targets"].append(o_s_f)
    res["count"] = len(res["targets"])
    return jsonify(res)


@app.route("/api/mirrors/osses")
def get_mirrors_osses():
    return jsonify(dict(count=0, targets=[]))


@app.after_request
def custom_headers(res):
    res.headers["Server"] = app.config["APP_NAME"]
    return res
