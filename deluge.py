#!/usr/bin/python

import sys
import os
import datetime
import shutil
import time

DESTINATION = "CHANGE ME"
LOG_FILE = "CHANGE ME"

current_millis = lambda: int(round(time.time() * 1000))


def print_help():
    log("Usage:%s 'torrentId' 'torrentName' 'torrentPath'" % sys.argv[0])


# returns size of tree/file in bytes
def get_total_size(source):
    total_size = os.path.getsize(source)
    if os.path.isdir(source):
        for item in os.listdir(source):
            item_path = os.path.join(source, item)
            if os.path.isfile(item_path):
                total_size += os.path.getsize(item_path)
            elif os.path.isdir(item_path):
                total_size += get_total_size(item_path)
    return total_size


# converts a byte quantity into human readable units
def human_readable(num):
    for unit in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, unit)
        num /= 1024.0
    # stop at TB
    return "%3.2f%s" % (num, 'TB')


def copyfile(source, destination):
    log("Copying file '%s' to '%s'" % (source, destination))
    shutil.copy(source, destination)


def copydir(source, destination):
    log("Copying directory '%s' to '%s'" % (source, destination))
    shutil.copytree(source, destination)


def log(message):
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_file = open(LOG_FILE, 'a')
    log_file.write("[%s] %s\n" % (date, message))


def main():
    sys.stderr = open(LOG_FILE, 'a')
    sys.stdout = open(LOG_FILE, 'a')
    log(str(sys.argv))
    if len(sys.argv) == 4:
        torrent_name = sys.argv[2]
        torrent_path = sys.argv[3]
        log("torrent name %s" % torrent_name)  # debug
        log("torrent path %s" % torrent_path)  # debug
    else:
        print_help()
        exit(1)

    start_time = current_millis()

    if os.path.isfile(os.path.join(torrent_path, torrent_name)):
        # torrent is a single file
        move_size = get_total_size(torrent_path)
        copyfile(os.path.join(torrent_path, torrent_name),
        os.path.join(DESTINATION, torrent_name))
    elif os.path.isdir(os.path.join(torrent_path, torrent_name)):
        # torrent is a directory torrent_path + torrent_name
        move_size = get_total_size(os.path.join(torrent_path, torrent_name))
        copydir(os.path.join(torrent_path, torrent_name),
             os.path.join(DESTINATION, torrent_name))
    else:
        log("Your file/directory could not be found !")
        exit(2)
    # get elapsed time in seconds
    elapsed = (current_millis() - start_time) / 1000.0
    speed = "%s/s" % human_readable(move_size / elapsed)
    log("Moved %s in %.2f seconds. Speed: %s" %
    (human_readable(move_size), elapsed, speed))


if __name__ == "__main__":
    main()
