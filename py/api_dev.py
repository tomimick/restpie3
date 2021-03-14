#!/usr/bin/python
# -*- coding: utf-8 -*-

# api_dev.py: misc methods for testing and development
#   - remove if not needed, and make sure there is no risk for production
#
# Author: Tomi.Mickelsson@iki.fi

from flask import jsonify, redirect, render_template
import datetime
import html

import db
import config
import bgtasks
import red
from webutil import app

import logging
log = logging.getLogger("api")


@app.route('/', methods = ['GET'])
def index():
    """Just a redirect to api list."""
    return redirect('/api/list')


@app.route('/api/list', methods = ['GET'])
def list_api():
    """List the available REST APIs in this service as HTML. Queries
    methods directly from Flask, no need to maintain separate API doc.
    (Maybe this could be used as a start to generate Swagger API spec too.)"""

    # decide whether available in production
#     if config.IS_PRODUCTION:
#         return "not available in production", 400

    # build HTML of the method list
    apilist = []
    rules = sorted(app.url_map.iter_rules(), key=lambda x: str(x))
    for rule in rules:
        f = app.view_functions[rule.endpoint]
        docs = f.__doc__ or ''
        module = f.__module__ + ".py"

        # remove noisy OPTIONS
        methods = sorted([x for x in rule.methods if x != "OPTIONS"])
        url = html.escape(str(rule))
        if not "/api/" in url and not "/auth/" in url:
            continue
        apilist.append("<div><a href='{}'><b>{}</b></a> {}<br/>{} <i>{}</i></div>".format(
            url, url, methods, docs, module))

    header = """<body>
        <title>RESTPie3</title>
        <style>
            body { width: 80%; margin: 20px auto;
                 font-family: Courier; }
            section { background: #eee; padding: 40px 20px;
                border: 1px dashed #aaa; }
            i { color: #888; }
        </style>"""
    title = """
        <section>
        <h2>REST API ({} end-points)</h2>
        <h3>IS_PRODUCTION={}  IS_LOCAL_DEV={} Started ago={}</h3>
        """.format(len(apilist), config.IS_PRODUCTION, config.IS_LOCAL_DEV,
                config.started_ago(True))
    footer = "</section></body>"

    return header + title + "<br/>".join(apilist) + footer


if config.IS_LOCAL_DEV:
    @app.route('/apitest/dbtruncate', methods = ['POST'])
    def truncate():
        """For testing: Empty all data from all tables. An external test script
        can call this at start. Only accessible in local dev machine."""

        cursor = db.database.execute_sql("truncate users, movies")
        return jsonify({}), 200


@app.route('/apitest/sendemail', methods = ['GET'])
def send():
    """For testing: Example of activating a background task."""

    log.info("executing a background task")

    bgtasks.send_email.spool(email="tomi@tomicloud.com",
            subject="Hello world!", template="welcome.html")

    return jsonify({"reply":"background task will start"}), 200


@app.route('/apitest/counter', methods = ['GET'])
def testcounter():
    """For testing: Increment redis counter."""

    num = red.incr("testcounter")
    return jsonify({"counter":num}), 200


@app.route('/examplehtml', methods = ['GET'])
def htmlpage():
    """For testing: Example HTML page, if you want to use templates."""

    # just some data for the template
    clock = datetime.datetime.now()

    return render_template('example.html', clock=clock)

