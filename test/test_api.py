#!/usr/bin/python
# -*- coding: utf-8 -*-

# api_test.py: automated tests for HTTP API
#   - not unit tests but ordered set of automated tests
#   - the database tables are cleaned on start
#
# Author: Tomi.Mickelsson@iki.fi

import unittest
import requests
import json

# URL_BASE = "http://localhost:8100/api/"
URL_BASE = "http://localhost:80/api/" # port is 80 inside docker

URL_SIGNUP     = 'signup'
URL_LOGIN      = 'login'
URL_LOGOUT     = 'logout'
URL_ME         = 'me'
URL_USERS      = 'users'
URL_TRUNCATE   = "../apitest/dbtruncate"

URL_MOVIES     = 'movies/'


s = requests.Session() # remember session

headers = {'content-type': 'application/json',
           'User-Agent': 'Python API Test'}


class Tests(unittest.TestCase):

    inited = False

    def setUp(self):
        if not Tests.inited:
            # empty all tables before running tests
            url = URL_TRUNCATE
            self.call(url, payload={})
            Tests.inited = True

    def test001_login_signup_get_fail(self):
        self.call(URL_LOGIN, 405)
        self.call(URL_SIGNUP, 405)
        self.call(URL_LOGOUT, 405)

    def test002_login_failure(self):
        payload = {"email":"a@example.com", "password":"y"}
        self.call(URL_LOGIN, 400, payload)

    def test003_signup_failure(self):
        payload = {"email":"a@example.com", "password":"y"}
        self.call(URL_SIGNUP, 400, payload)

    def test004_signup_ok(self):
        payload = {"email":"tomi@example.com", "password":"1234",
                   "fname":"Tomi", "lname":"Mickelsson"}
        self.call(URL_SIGNUP, 400, payload) # password too small
        payload["password"] = "123abC"
        self.call(URL_SIGNUP, 201, payload)

        reply = self.call(URL_ME, 200)

        reply = self.call(URL_ME)["me"]
        self.assertIsNotNone(reply.get("id"))
        self.assertEqual(reply.get("first_name"), "Tomi")

        self.call(URL_LOGOUT, payload={})

        self.call(URL_ME, 405, {})
        self.call(URL_ME, 401)

        self.call(URL_SIGNUP, 400, payload) # email used already

    def test005_login_ok(self):
        payload = {"email":"tomi@example.com", "password":"123abC"}
        self.call(URL_LOGIN, 200, payload)

    def test006_test_roles(self):
        self.call(URL_USERS, 401)

    def test007_movies(self):
        payload = {"email":"tomi@example.com", "password":"123abC"}
        reply = self.call(URL_LOGIN, 200, payload)
        my_uid = reply["id"]

        self.assertEqual([], self.call(URL_MOVIES))

        payload = {"title":"Forrest Gump", "director":"Robert Zemeckis"}
        self.call(URL_MOVIES, 201, payload)
        payload = {"title":"Matrix", "director":"Lana Wachowsk"}
        self.call(URL_MOVIES, 201, payload)

        reply = self.call(URL_MOVIES)
        self.assertEqual(2, len(reply))
        self.assertEqual("Forrest Gump", reply[0]["title"])
        self.assertEqual("Lana Wachowsk", reply[1]["director"])
        self.assertEqual(my_uid, reply[1]["creator"])

        id_gump = reply[0]["id"]
        id_matrix = reply[1]["id"]

        reply = self.call(URL_MOVIES+id_matrix)
        self.assertEqual("Matrix", reply["title"])

        payload = {"director":"Lana Wachowski"}
        reply = self.call(URL_MOVIES+id_matrix, 200, payload, s.put)

        reply = self.call(URL_MOVIES+id_matrix)
        self.assertEqual("Lana Wachowski", reply["director"])
        self.assertEqual(2, len(self.call(URL_MOVIES)))

        reply = self.call(URL_MOVIES+"?search=matrix")
        self.assertEqual(1, len(reply))

        reply = self.call(URL_MOVIES+"?search=s")
        self.assertEqual(2, len(reply))

        reply = self.call(URL_MOVIES+"?creator="+my_uid)
        self.assertEqual(2, len(reply))

        reply = self.call(URL_MOVIES+id_matrix, 200, None, s.delete)
        self.assertEqual(1, len(self.call(URL_MOVIES)))
        reply = self.call(URL_MOVIES+id_gump, 200, None, s.delete)
        self.assertEqual([], self.call(URL_MOVIES))



    def call(self, url, httpcode=200, payload = None, request_method=False):
        """GET or POST to server REST API"""

        func = request_method if request_method else s.post if payload != None else s.get
        r = func(URL_BASE + url, data = json.dumps(payload or {}),
                headers = headers)

        self.assertEqual(r.status_code, httpcode)
        if not r.status_code in (401, 405):
            return r.json()


if __name__ == '__main__':
    unittest.main()

