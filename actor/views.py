# coding=utf-8

import hmac
import logging
import os.path

from actor import app
from hashlib import sha1
from datetime import datetime
from flask import jsonify, request, abort
from domains import db, MirrorsInfo, MirrorsResources, MirrorsNotices

time_old_format = "%Y%m%d %H:%M:%S"
time_new_format = "%Y-%m-%d %H:%M:%S"
time_unknown = "????-??-?? ??:??:??"


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
    mirrors = MirrorsInfo.query.filter_by(status=0).order_by(MirrorsInfo.name)
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
            last_sync=time_unknown,
            size="unknown",
            status=500,
            message=''
        )
        # update last_sync, size, status, message from sync log
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
    """Update mirrors' last_sync, size, status, message property."""
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

            if stage == "SyncCompt":
                time = ' '.join([last_line_values[0], last_line_values[1]])
                target["last_sync"] = datetime.strptime(time, time_old_format).strftime(time_new_format)
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
                target["last_sync"] = datetime.strptime(time, time_old_format).strftime(time_new_format)
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
    mirrors = MirrorsInfo.query.filter_by(status=0).all()
    res = dict(count=0, targets=[])
    for mirror in mirrors:
        # Only name in row
        target = dict(
            name=mirror.name,
            last_sync=time_unknown,
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
    """Show the last notices."""
    res = dict(count=0, targets=[])

    # query all the actived notices
    notices = MirrorsNotices.query.filter_by(status=0)\
        .order_by(MirrorsNotices.created.desc())
    for notice in notices:
        time_created_f = notice.created.strftime(time_new_format)
        notice_f = dict(
            created_at=time_created_f,
            notice=notice.content,
            level=notice.level
        )
        res["targets"].append(notice_f)
    res["count"] = len(res["targets"])
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
    query = db.session.query(MirrorsResources.name)\
        .distinct().filter(MirrorsResources.type == "os",
                           MirrorsResources.status == 0)
    os_names = [row.name for row in query.all()]

    for os_name in os_names:
        # fetch all versions of the os
        os_versions = MirrorsResources.query.\
            filter_by(type="os", name=os_name, status=0).all()

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
    """Retrun list of some Open Source Softwares."""
    res = dict(count=0, targets=[])
    # query all the osses
    query = db.session.query(MirrorsResources.name).\
        distinct().filter(MirrorsResources.type == "oss",
                          MirrorsResources.status == 0)
    oss_names = [row.name for row in query.all()]

    for oss_name in oss_names:
        # fetch all versions of the oss
        oss_versions = MirrorsResources.query.\
            filter_by(type="oss", name=oss_name, status=0).all()

        # prepare the oss object
        oss_f = dict(name=oss_name, fullname='', type="oss", url='', versions=[], count=0)

        for (idx, oss) in enumerate(oss_versions):
            # init the oss object
            if idx == 0:
                oss_f["fullname"] = oss.fullname
                oss_f["url"] = ''.join([oss.protocol, "://", oss.host, oss.dir])

            # add new version of the oss
            oss_version_f = format_version(oss.version)
            oss_version_url = ''.join([oss.protocol, "://", oss.host, oss.path])
            version = dict(version=oss_version_f, url=oss_version_url)
            oss_f["versions"].append(version)
        # update count of the os's version object
        oss_f["count"] = len(oss_f["versions"])
        res["targets"].append(oss_f)
    res["count"] = len(res["targets"])
    return jsonify(res)


def check_headers(headers):
    if headers["X-Github-Event"] != "issues":
        return False

    return True


def add_mirror(body):
    pass


def add_resource(body):
    pass


def add_notice(body):
    notice = MirrorsNotices(content=body)
    db.session.add(notice)
    db.session.commit()


def dispatch(label_name, body):
    if label_name == "mirror":
        add_mirror(body)

    if label_name == "resource":
        add_resource(body)

    if label_name == "notice":
        add_notice(body)


@app.route("/api/mirrors/issue", methods=["POST"])
def post_mirrors_issue():
    github_signature = request.headers["X-Hub-Signature"]
    github_delivery_id = request.headers["X-Github-Delivery"]

    # check request body with hook secret
    signature = hmac.new(app.config["GITHUB_HOOK_SECRET"], request.data, sha1).hexdigest()
    signature_f = ''.join(["sha1=", signature])
    if signature_f != github_signature:
        abort(403)

    # fot test only
    if request.headers["X-Github-Event"] == "ping":
        return "pang"

    if not check_headers(request.headers):
        abort(403)

    issue_payload = request.get_json()

    if issue_payload["action"] == "labeled":
        dispatch(issue_payload["label"]["name"], issue_payload["issue"]["body"])

    return "ok"


@app.after_request
def custom_headers(res):
    res.headers["Server"] = app.config["APP_NAME"]
    return res
