#!/usr/bin/env python

import os
import json

from datetime import datetime

LOG_PATH = "/var/log/mirrors/sync/"
ISO_TIME_FMT = "%Y-%m-%dT%H:%M:%SZ"
EXP_TIME_FMT = "%Y-%m-%d %H:%M:%S"

STATUS_MAPPING = {
    "syncing": 100,
    "success": 200,
    "freeze": 300,
    "failed": 400,
    "unknown": 500}

mirror_fields = [
    "archlinux-cn", "archlinux-arm", "archlinux", "centos", "cpan", "ctan",
    "cygwin", "debian", "debian-backports", "debian-cd", "debian-multimedia",
    "debian-security", "deepin", "deepin-cd", "epel", "ezgo", "kali",
    "kali-security", "kernel", "linuxmint", "raspbian", "ubuntu",
    "ubuntu-releases",]


def new_mirror(mirror_id):
    return dict(
        cname=mirror_id,
        url="https://mirrors.cqu.edu.cn/{}".format(mirror_id),
        synced_at="0000-00-00 00:00:00",
        status=500,
        has_comment=True,
        comment="new",
        has_help=True,
        help_url="https://mirrors.cqu.edu.cn/wiki/{}".format(mirror_id))


def parse_log(log):
    with open(log, "r") as fp:
        last_line = fp.readlines()[-1]
    parts = last_line.split()
    synced_time = datetime.strptime(parts[0], ISO_TIME_FMT)
    synced_time = synced_time.strftime(EXP_TIME_FMT)
    status_code = STATUS_MAPPING[parts[1]]
    return synced_time, status_code


def main():
    mirror_list = []
    for mirror_id in mirror_fields:
        mirror = new_mirror(mirror_id)
        log=os.path.join(LOG_PATH, mirror_id)
        if os.path.isfile(log):
            sycned_time, status_code = parse_log(log)
            mirror["status"] = status_code
            if status_code == 200:
                mirror["synced_at"] = sycned_time
        mirror_list.append(mirror)
    with open("index.json", "r") as fp:
        mirror_index = json.load(fp)
    mirror_index["mirrorlist"]["targets"] = mirror_list
    mirror_index["mirrorlist"]["count"] = len(mirror_list)
    with open("index.json", "w") as fp:
        json.dump(mirror_index, fp, indent=4)


if __name__ == "__main__":
    main()

