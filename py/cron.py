#!/usr/bin/python
# -*- coding: utf-8 -*-

# cron.py: cron tasks (called by uwsgi daemon, not linux cron)
#
# Author: Tomi.Mickelsson@iki.fi

from uwsgidecorators import timer, cron, filemon

import db
import util
import webutil
import config

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


# @filemon("/tmp/foobar")
# def file_has_been_modified(num):
#     """Runs when a file has been modified."""
#     log.info("cron task: file has been modified")

