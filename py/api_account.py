#!/usr/bin/python
# -*- coding: utf-8 -*-

# api.py: REST API for basic account related stuff: signup/login/logout
#
# Author: Tomi.Mickelsson@iki.fi

from flask import request, session, g, jsonify

import db
import webutil
import account
from webutil import app, login_required, get_myself

import logging
log = logging.getLogger("api")


@app.route('/api/login', methods = ['POST'])
def login():
    """Logs the user in with email+password.
       On success returns the user object,
       on error returns 400 and json with err-field."""

    input = request.json or {}
    email = input.get('email')
    password = input.get('password')

    if not email or not password:
        return webutil.warn_reply("Missing input")

    u = db.get_user_by_email(email)
    if not u or not account.check_password(u.password, password):
        # error
        return webutil.warn_reply("Invalid login credentials")
    else:
        # success
        account.build_session(u, is_permanent=input.get('remember', True))

        log.info("LOGIN OK agent={}".format(webutil.get_agent()))
        return jsonify(u), 200


@app.route('/api/signup', methods = ['POST'])
def signup():
    """Signs a new user to the service. On success returns the user object,
       on error returns 400 and json with err-field."""

    input = request.json or {}
    email  = input.get('email')
    password = input.get('password')
    fname  = input.get('fname')
    lname  = input.get('lname')
    company  = input.get('company')

    if not email or not password or not fname or not lname:
        return webutil.warn_reply("Invalid signup input")

    u = db.get_user_by_email(email)
    if u:
        msg = "Signup email taken: {}".format(email)
        return webutil.warn_reply(msg)

    err = account.check_password_validity(password)
    if err:
        return jsonify({"err":err}), 400

    # create new user
    u = db.User()
    u.email = email
    u.company = company
    u.first_name = fname
    u.last_name = lname
    u.password = account.hash_password(password)
    u.tags = []
    u.role = 'editor' # set default to what makes sense to your app
    u.save(force_insert=True)

    account.new_signup_steps(u)
    account.build_session(u, is_permanent=input.get('remember', True))

    log.info("SIGNUP OK agent={}".format(webutil.get_agent()))

    return jsonify(u), 201


@app.route('/api/logout', methods = ['POST'])
@login_required
def logout():
    """Logs out the user, clears the session."""
    session.clear()
    return jsonify({}), 200


@app.route('/api/me')
@login_required
def me():
    """Return info about me. Attach more data for real use."""

    me = get_myself()
    reply = {"me": me}

    return jsonify(reply), 200


@app.route('/api/users')
@login_required(role='superuser')
def users():
    """Search list of users. Only for superusers"""

    input = request.args or {}
    page = input.get('page')
    size = input.get('size')
    search = input.get('search')

    reply = db.query_users(page, size, search)

    return jsonify(reply), 200

