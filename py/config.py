#!/usr/bin/python
# -*- coding: utf-8 -*-

# config.py: configuration data of this app
#   - other modules should read config from here
#   - the config is first read from a json file
#   - env variables may override (in docker setup etc)

import sys
import os
import redis
import json
import time

# first load config from a json file,
srvconf = json.load(open(os.environ["PYSRV_CONFIG_PATH"]))

# then override with env variables
for k, v in os.environ.items():
    if k.startswith("PYSRV_"):
        print("env override ", k)
        srvconf[k] = v

# grand switch to production!
IS_PRODUCTION = bool(srvconf['PYSRV_IS_PRODUCTION'] or False)

# local dev flag
IS_LOCAL_DEV = os.environ.get("FLASK_ENV") == "development" and not IS_PRODUCTION
# IS_LOCAL_DEV = False

print("\nCONFIG: prod={},localdev={} ({})\n".format(
    IS_PRODUCTION, IS_LOCAL_DEV, srvconf["name"]))

# database config
DATABASE_HOST = srvconf['PYSRV_DATABASE_HOST']
DATABASE_PORT = srvconf['PYSRV_DATABASE_PORT']
DATABASE_NAME = srvconf['PYSRV_DATABASE_NAME']
DATABASE_USER = srvconf['PYSRV_DATABASE_USER']
DATABASE_PASSWORD = srvconf['PYSRV_DATABASE_PASSWORD']
IS_SQLITE = DATABASE_HOST.startswith("/")

# Flask + session config
# http://flask.pocoo.org/docs/1.0/config/
# https://pythonhosted.org/Flask-Session/
redishost = srvconf['PYSRV_REDIS_HOST']

flask_config = dict(
    # app config
    TESTING = IS_LOCAL_DEV,
    SECRET_KEY = None, # we have server-side sessions

    # session config - hardcoded to Redis
    SESSION_TYPE = 'redis',
    SESSION_REDIS = redis.from_url('redis://{}'.format(redishost)),
    SESSION_COOKIE_NAME = "mycookie",
    SESSION_COOKIE_SECURE = srvconf['PYSRV_COOKIE_HTTPS_ONLY'] if not IS_LOCAL_DEV else False, # require https?
    SESSION_COOKIE_HTTPONLY = True, # don't allow JS cookie access
    SESSION_KEY_PREFIX = 'pysrv',
    PERMANENT_SESSION_LIFETIME = 60*60*24*30, # 1 month
    SESSION_COOKIE_DOMAIN = srvconf['PYSRV_DOMAIN_NAME'] or None if not IS_LOCAL_DEV else None,
)

# dump sql statements in log file?
PYSRV_LOG_SQL = srvconf.get('PYSRV_LOG_SQL')

# allow API access to this domain
CORS_ALLOW_ORIGIN = srvconf.get('PYSRV_CORS_ALLOW_ORIGIN', '*')

START_TIME = int(time.time())


def started_ago(as_string=False):
    """Returns how many seconds ago the server was started. Or as a string."""

    ago = int(time.time()) - START_TIME
    if as_string:
        return "{}d {:02d}:{:02d}:{:02d}".format(int(ago/60/60/24),
                int(ago/60/60)%24, int(ago/60)%60, ago%60)
    else:
        return ago

