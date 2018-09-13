#!/bin/sh
# run uwsgi in dev mode

uwsgi --ini conf/uwsgi.ini:uwsgi-debug

