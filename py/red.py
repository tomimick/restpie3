#!/usr/bin/python
# -*- coding: utf-8 -*-

# red.py: read/write data in Redis
#   - get/set key values with expiration time
#   - simple list operations
#   - atomic increment, getset
#
# Note: stores pickled data in Redis. If you want to interoperate with the
# data with other tools, you'd better change pickle to json (a bit slower
# but interoperates better).
#
# https://redis.io/commands
# https://github.com/andymccurdy/redis-py
#
# Author: Tomi.Mickelsson@iki.fi

import redis
import pickle

import config

import logging
log = logging.getLogger("cache")


#rdb = redis.StrictRedis(host=config.redishost)
rdb = redis.from_url('redis://{}'.format(config.redishost))

# --------------------------------------------------------------------------
# key values

def set_keyval(key, val, expiration_secs=0):
    """Sets key value. Value can be any object. Key is optionally discarded
    after given seconds."""

    try:
        s = pickle.dumps(val)
        rdb.set(key, s, expiration_secs or None)
    except:
        log.error("redis set_keyval %s", key)

def get_keyval(key, default=None):
    """Returns key value or default if key is missing."""

    try:
        v = rdb.get(key)
        return pickle.loads(v) if v else default
    except:
        log.error("redis get_keyval %s", key)
        return default

def delete_key(key):
    """Deletes key. Can be a list too."""

    try:
        rdb.delete(key)
    except:
        log.error("redis del %s", key)


# --------------------------------------------------------------------------
# list operations

def list_append(name, item, max_size=None):
    """Inserts item at the end of the list. If max_size is given, truncates
    the list into max size, discarding the oldest items."""
    try:
        s = pickle.dumps(item)
        rdb.rpush(name, s)

        if max_size:
            rdb.ltrim(name, -int(max_size), -1)
    except:
        log.error("redis list_append")

def list_pop(name, timeout=None):
    """Returns first item in the list. If timeout is given, wait that many
    seconds."""

    if timeout != None:
        s = rdb.blpop(name, timeout=timeout)
        if s:
            s = s[1] # with timeout, value is the 2nd item
    else:
        s = rdb.lpop(name)
    return pickle.loads(s) if s else None

def list_peek(name):
    """Returns first item in queue or None. Does not remove the item."""
    s = rdb.lrange(name, 0, 0)
    return pickle.loads(s[0]) if s else None

def list_fetch(name):
    """Returns all items in queue or None. Does not remove the items."""
    slist = rdb.lrange(name, 0, -1)
    if slist:
        return [pickle.loads(s) for s in slist]

def list_length(name):
    """Returns the length of the list."""
    return rdb.llen(name)


# --------------------------------------------------------------------------
# atomic operations

def incr(name, num=1):
    """Increments a count by num. Returns value after increment."""
    return rdb.incrby(name, num)

def get_set(key, val):
    """Sets key value atomically. Returns the previous value."""
    s = pickle.dumps(val)
    oldval = rdb.getset(key, s)
    return pickle.loads(oldval) if oldval else None

