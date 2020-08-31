#!/usr/bin/python
# -*- coding: utf-8 -*-

# webutil.py: low level page request related methods, decorators, Flask app
#
# Author: Tomi.Mickelsson@iki.fi

import time
import peewee
import functools
from flask import Flask, request, session, g, redirect, abort, jsonify
from flask_session import Session
from flask.json import JSONEncoder

import db
import config
import datetime

import logging
log = logging.getLogger("webutil")


# create and configure the Flask app
app = Flask(__name__, static_folder=None, template_folder="../templates")
app.config.update(config.flask_config)
Session(app)


# --------------------------------------------------------------------------
# API decorator

def login_required(func=None, role=None):
    """Decorator: must be logged on, and optionally must have the given role.
       Insert after app.route like this:
       @app.route('/api/users')
       @login_required(role='superuser')"""

    # yes, this is python magic, see https://blogs.it.ox.ac.uk/inapickle/2012/01/05/python-decorators-with-optional-arguments/
    if not func:
        return functools.partial(login_required, role=role)
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return _check_user_role(role) or func(*args, **kwargs)
    return inner


# --------------------------------------------------------------------------
# get data about me, return error replys

def get_myself():
    """Return the user object of the caller or None if he is a visitor.
    Loads the user from the database, then caches it during request."""

    if not "userid" in session:
        return None

    if hasattr(g, "MYSELF"):
        return g.MYSELF # use cache
    else:
        g.MYSELF = db.get_user(session["userid"])
        return g.MYSELF

def error_reply(errmsg, httpcode=400):
    """Logs an error and returns error code to the caller."""
    log.error(errmsg)
    return jsonify({"err":"{}: {}".format(httpcode, errmsg)}), httpcode

def warn_reply(errmsg, httpcode=400):
    """Logs a warning and returns error code to the caller."""
    log.warning(errmsg)
    return jsonify({"err":"{}: {}".format(httpcode, errmsg)}), httpcode

def get_agent():
    """Returns browser of caller."""
    return request.headers.get('User-Agent', '')

def get_ip():
    """Returns IP address of caller."""
    return request.headers.get('X-Real-IP') or request.remote_addr


# --------------------------------------------------------------------------
# before/after/error request handlers

@app.before_request
def before_request():
    """Executed always before a request. Connects to db, logs the request,
       prepares global data, loads current user."""

    # log request path+input, but not secrets
    try:
        params = request.json or request.args or request.form
    except:
        params = None
    if params:
        cloned = None
        secret_keys = ["password", "passwd", "pwd"]
        for k in secret_keys:
            if k in params:
                if not cloned:
                    cloned = params.copy()
                cloned[k] = 'X'
        if cloned:
            params = cloned

    params = str(params or '')[:1000]
    method = request.method[:2]
    log.info("{} {} {}".format(method, request.path, params))

    # connect to db
    g.db = db.database
    g.db.connection()

    # have common data available in global g
    # but do not pollute g, store only the most relevant data
    g.HOST = request.headers.get('X-Real-Host', '')
    g.ISLOGGED = "userid" in session
    myrole = session.get("role") or ""
    g.IS_SUPER_USER = myrole == "superuser"

    if myrole == "disabled":
        err = "account disabled"
        log.warn(err)
        return jsonify({"err":err}), 400

    # time the request
    g.t1 = time.time()

    # where did we link from? (but filter our internal links)
#     if request.referrer:
#         log.info("linked from "+request.referrer)


@app.after_request
def after_request(response):
    """Executed after a request, unless a request occurred."""

    # log about error
    logmethod = None
    if 400 <= response.status_code <= 599:
        logmethod = log.error
    elif not 200 <= response.status_code < 399:
        logmethod = log.warn
    if logmethod:
        logmethod("  {} {} {}".format(response.status_code,
            request.method, request.url))

    # set CORS headers
    response.headers['Access-Control-Allow-Origin'] = config.CORS_ALLOW_ORIGIN
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
#     response.headers['Access-Control-Expose-Headers'] = 'Access-Control-Allow-Origin'

    return response

@app.teardown_request
def teardown(error):
    """Always executed after a request."""

    if hasattr(g, "db"):
        g.db.close()

    # log warning when a request takes >1.0sec
    # (put long-running tasks into background)
    if hasattr(g, "t1"):
        delta = time.time()-g.t1
        if delta > 1.0:
            log.warn("SLOW! {} time={}".format(request.path, delta))


@app.errorhandler(404)
def page_not_found(error):
    err = "404: " + request.path
    return jsonify({"err":err}), 404


# --------------------------------------------------------------------------
# logging (is in this module because binds to session)

class ColorFormatter(logging.Formatter):
    """Colorize warnings and errors"""

    def format(self, rec):
        if rec.levelno == logging.WARNING:
            rec.msg = "\033[93m{}\033[0m".format(rec.msg)
        elif rec.levelno in (logging.ERROR, logging.CRITICAL):
            rec.msg = "\033[91m{}\033[0m".format(rec.msg)
        return logging.Formatter.format(self, rec)


class MyLogContextFilter(logging.Filter):
    """Injects contextual info, ip+userid, into the log."""

    def filter(self, record):
        if request:
            # take ip from a header or actual
            ip = get_ip()
            # take userid from the session
            uid = session.get("userid", "anon")
        else:
            ip = ""
            uid = "  -WORKER" # background worker

        record.ip = "local" if config.IS_LOCAL_DEV else ip
        record.uid = uid
        return True


def init_logging():
    """Initialize logging system."""

    prefix = "PROD " if config.IS_PRODUCTION else ""
    format = prefix+"%(levelname)3.3s %(uid)s@%(ip)s %(asctime)s %(filename)s %(message)s"
    dfmt = "%d%m%y-%H:%M:%S"
    logging.basicConfig(level=logging.INFO, format=format, datefmt=dfmt)

    formatter = ColorFormatter(format, datefmt=dfmt)

    # custom log data: userid + ip addr
    f = MyLogContextFilter()
    for handler in logging.root.handlers:
        handler.addFilter(f)
        handler.setFormatter(formatter) # remove if coloring not wanted

    if config.PYSRV_LOG_SQL:
        logging.getLogger('peewee').setLevel(logging.DEBUG)


# --------------------------------------------------------------------------
# internal methods, serializing models

def _check_user_role(rolebase):
    """Check that my role is atleast the given role. If not, log and return
    an error."""

    myrole = session.get("role") or ""

    if not _is_role_atleast(myrole, rolebase):
        uid = session.get("userid") or ""
        err = "Unauthorized! {} {} user={}".format(
                request.method, request.path, uid)
        return warn_reply(err, 401)

def _is_role_atleast(myrole, rolebase):
    """Checks that myrole is same or above rolebase. Assumes a
    simple role model where roles can be arranged from lowest
    access to highest access level."""

    if not rolebase:
        # no role required, but I need to be logged-on
        return "userid" in session

    levels = {"readonly":1, "editor":2, "admin":3, "superuser":4}
    try:
        return levels[myrole] >= levels[rolebase]
    except:
        return False


class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, peewee.SelectQuery):
            return list(obj)
        if isinstance(obj, db.BaseModel):
            return obj.serialize()
        elif isinstance(obj, datetime.datetime):
#             dt_local = util.utc2local(obj)
            return obj.isoformat() if obj else None
        return JSONEncoder.default(self, obj)

app.json_encoder = MyJSONEncoder

init_logging()

