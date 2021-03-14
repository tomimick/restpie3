#!/usr/bin/python
# -*- coding: utf-8 -*-

# util.py: utility functions
#
# Author: Tomi.Mickelsson@iki.fi

import pytz
import datetime
import time
import uuid
import functools

import logging
log = logging.getLogger("util")


# --------------------------------------------------------------------------
# date related common methods

tz_hki = pytz.timezone("Europe/Helsinki")
tz_utc = pytz.utc

def utc2local(utc_dt, tz=tz_hki):
    """Convert UTC into local time, given tz."""

    if not utc_dt:
        return utc_dt

    d = utc_dt.replace(tzinfo=tz_utc)
    return d.astimezone(tz)

def local2utc(local_dt, tz=tz_hki):
    """Convert local time into UTC."""

    if not local_dt:
        return local_dt

    d = local_dt.replace(tzinfo=tz)
    return d.astimezone(tz_utc)

def utcnow():
    """Return UTC now."""
    return datetime.datetime.utcnow()

def generate_token():
    """Generate a random token
    (an uuid like 8491997531e44d37ac3105b300774e08)"""
    return uuid.uuid4().hex

def timeit(f):
    """Decorator to measure function execution time."""
    @functools.wraps(f)
    def wrap(*args, **kw):
        t1 = time.time()
        result = f(*args, **kw)
        t2 = time.time()
        log.info("%r args:[%r, %r] took: %2.4f sec" % \
          (f.__name__, args, kw, t2-t1))
        return result
    return wrap


if __name__ == '__main__':

    # quick adhoc tests
    logging.basicConfig(level=logging.DEBUG)

    @timeit
    def myfunc():
        now = utcnow()
        print(now)
        print(utc2local(now))
        time.sleep(1.0)
    myfunc()

