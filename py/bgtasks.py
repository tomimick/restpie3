#!/usr/bin/python
# -*- coding: utf-8 -*-

# bgtasks.py: background tasks
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

import logging
log = logging.getLogger("bgtasks")


@spool(pass_arguments=True)
def send_email(*args, **kwargs):
    """A background worker that is executed by spooling arguments to it."""

    log.info("send_email started, got arguments: {} {}".format(args, kwargs))


    log.info("processing emails...")

    # do the stuff...
    time.sleep(3)

    log.info("processing done!")

