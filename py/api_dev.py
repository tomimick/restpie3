#!/usr/bin/python
# -*- coding: utf-8 -*-

# api_dev.py: misc methods for testing and development
#   - remove if not needed, and make sure there is no risk for production
#
# Author: Tomi.Mickelsson@iki.fi

import html
from flask import request, session, jsonify, g, abort
from webutil import app, local_dev_only

import db
import util
import webutil
import config
import bgtasks

import logging
log = logging.getLogger("api")


@app.route('/api/list_api', methods = ['GET'])
def list_api():
    """For testing: List the available REST APIs in this service. Queries
    methods directly from Flask, no need to maintain separate API doc.
    (Maybe this could be used as a start to generate Swagger API spec too.)"""

    # not available in production
    if config.IS_PRODUCTION:
        abort(400)

    # build HTML of the method list
    apilist = []
    rules = sorted(app.url_map.iter_rules(), key=lambda x: str(x))
    for rule in rules:
        f = app.view_functions[rule.endpoint]
        docs = f.__doc__ or ''

        # remove noisy OPTIONS
        methods = sorted([x for x in rule.methods if x != "OPTIONS"])
        url = html.escape(str(rule))
        apilist.append("<div><a href='{}'><b>{}</b></a> {}<br/>{}</div>".format(
            url, url, methods, docs))

    header = """<body>
        <style>
            body { width: 80%; margin: 20px auto;
                 font-family: Courier; }
            section { background: #eee; padding: 40px 20px;
                border: 1px dashed #aaa; }
        </style>
        <section>
        <h2>REST API (_COUNT_ end-points)</h2>
        """.replace('_COUNT_', str(len(apilist)))
    footer = "</section></body>"

    return header + "<br/>".join(apilist) + footer


@app.route('/api/dbtruncate', methods = ['POST'])
@local_dev_only
def truncate():
    """For testing: Empty all data from all tables. An external test script
    can call this at start. Only accessible in local dev machine."""

    cursor = db.database.execute_sql("truncate users, movies")
    return jsonify({}), 200


@app.route('/api/sendemail', methods = ['GET'])
def send():
    """For testing: Example of activating a background task."""

    log.info("executing a background task")

    bgtasks.send_email.spool(email="tomi@tomicloud.com",
            subject="Hello world!", template="welcome.html")

    return jsonify({"reply":"background task will start"}), 200

