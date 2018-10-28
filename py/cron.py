#!/usr/bin/python
# -*- coding: utf-8 -*-

# cron.py: cron tasks (called by uwsgi daemon, not linux cron)
#
#   - Note that these funcs are subject to the same "harakiri" timeout as
#   regular requests. If you need to run longer, spool a background worker
#   from a cron func. Spooler workers have a timeout "spooler-harakiri"
#   specified in uwsgi.ini.
#
# Author: Tomi.Mickelsson@iki.fi

from uwsgidecorators import timer, cron, filemon
import datetime

import db
import util
import webutil
import config
import red

import logging
log = logging.getLogger("cron")


@timer(60)
def every_minute(num):
    """Runs every minute."""

    log.info("every_minute")


@cron(0,-1,-1,-1,-1)
#(minute, hour, day, month, weekday) - in local time
def every_hour(num):
    """Runs every hour at X:00."""

    log.info("every_hour")


@cron(0,2,-1,-1,-1)
def daily(num):
    """Runs every night at 2:00AM."""

    log.info("daily task here - it is 2:00AM")

    # if you have a cluster of servers, this check ensures that
    # only one server performs the task
    today = str(datetime.date.today())
    if today != red.get_set("nightlycron", today):
        daily_single_server()

def daily_single_server():

    log.info("daily task here - only 1 server in a cluster runs this")


# @filemon("/tmp/foobar")
# def file_has_been_modified(num):
#     """Runs when a file has been modified."""
#     log.info("cron task: file has been modified")

