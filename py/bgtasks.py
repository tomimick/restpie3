#!/usr/bin/python
# -*- coding: utf-8 -*-

# bgtasks.py: background tasks, which are run in separate worker processes
#   - execute these just by spooling arguments to functions, like:
#       bgtasks.send_email.spool(arg_list_here)
#
# Author: Tomi.Mickelsson@iki.fi

from uwsgidecorators import spool

import db
import util
import webutil
import config
import time
import uwsgi

import logging
log = logging.getLogger("bgtasks")


@spool(pass_arguments=True)
def send_email(*args, **kwargs):
    """A background worker that is executed by spooling arguments to it."""

    log.info("send_email started, got arguments: {} {}".format(args, kwargs))

    try:
        log.info("processing emails...")

        # do the stuff...
        time.sleep(3)

        log.info("processing done!")

    except:
        log.exception("send_email")

        # returning SPOOL_OK here signals to uwsgi to not retry this task
        # if the exception propagates up, uwsgi will call us again in
        # N secs, configured in uwsgi.ini: spooler-frequency
        return uwsgi.SPOOL_OK

