#!/usr/bin/python
# -*- coding: utf-8 -*-

# ui_auth.py: quick HTML pages for login/signup/forgot/reset password
#
# Author: Tomi.Mickelsson@iki.fi

from flask import redirect, request, render_template

import db
import account
import util
import red
from webutil import app, get_ip

import logging
log = logging.getLogger("uiauth")


@app.route('/auth/login', methods = ['GET'])
def ui_login():
    """Login page"""
    return render_template('auth.html', mode="login")


@app.route('/auth/signup', methods = ['GET'])
def ui_signup():
    """Signup page"""
    return render_template('auth.html', mode="signup")


@app.route('/auth/forgot', methods = ['GET'])
def ui_forgot():
    """Forgot password page"""
    return render_template('auth.html', mode="forgot")


@app.route('/auth/reset', methods = ['GET'])
def ui_reset():
    """Reset password page"""

    # token must point to a user
    token = request.args.get("token") or "-"
    data = red.get_keyval(token)
    errmsg = "Token is missing or expired" if not data else ""

    # show email
    email = "?"
    try:
        log.info(f"reset token={token} data={data}")
        u = db.get_user(data["uid"])
        email = u.email
    except:
        log.error(f"no user {data}")

    return render_template('auth.html', mode="reset",
            email=email, err=errmsg, token=token)


@app.route('/auth/postform', methods = ['POST'])
def postform():
    """Form POST endpoint for all form variations."""

    input = request.form
    mode = input["mode"]
    email = input["email"]
    passwd = input.get("passwd")
    token = input.get("token")

    u = db.get_user_by_email(email)

    errmsg = ""
    if not email:
        errmsg = "Email is missing"

    elif mode == "login":
        if not u or not account.check_password(u.password, passwd):
            errmsg = "Invalid login credentials"
        else:
            account.build_session(u, is_permanent=True)

            log.info(f"LOGIN OK {email}")

            # you should redirect to real ui...
            return redirect("/api/me")

    elif mode == "signup":
        if u:
            errmsg = f"Account exists already {email}"
        elif passwd != input.get("passwd2"):
            errmsg = f"Passwords differ"
        else:
            errmsg = account.check_password_validity(passwd)
            if not errmsg:
                # create new user
                u = db.User()
                u.email = email
                u.first_name = input["firstname"]
                u.last_name = input["lastname"]
                u.password = account.hash_password(passwd)
                u.role = 'editor' # set default to what makes sense to your app
                u.save(force_insert=True)

                account.new_signup_steps(u)
                account.build_session(u, is_permanent=True)

                log.info(f"SIGNUP OK {email}")

                # you should redirect to real ui...
                return redirect("/api/me")

    elif mode == "forgot":
        # request a new password
        if u:
            # generate an expiring token and store in redis
            token = str(util.generate_token())
            data = {"uid":f"{u.id}", "ip":get_ip()}
            expire_secs = 60*60 # 1h
            red.set_keyval(token, data, expire_secs)

            # email the link to the user
            link = f"DOMAIN/auth/reset?token={token}"
            errmsg = f"Server should now send a reset email to {email}..."
            log.info(f"password reset link = {link}")

        else:
            errmsg = f"Unknown account {email}"

    elif mode == "reset":
        # reset a password
        data = red.get_keyval(token)
        if data:
            try:
                u = db.get_user(data["uid"])

                # extra security: make sure ip addresses match, only the
                # requester can use the link
                if get_ip() != data["ip"]:
                    errmsg = "Invalid IP"

                elif passwd != input.get("passwd2"):
                    errmsg = "Passwords differ"

                else:
                    # ok, reset the password
                    u.password = account.hash_password(passwd)
                    u.save()
                    account.build_session(u, is_permanent=True)

                    # security: disable link from further use
                    red.delete_key(token)

                    log.info(f"PASSWD RESET OK {email}")
                    return redirect("/api/me")

            except:
                log.error(f"no user {value}")
                errmsg = "Invalid token"
        else:
            errmsg = "Invalid token"

    if errmsg:
        log.warn(errmsg)

    return render_template('auth.html', mode=mode, email=email,
            err=errmsg, token=token)

