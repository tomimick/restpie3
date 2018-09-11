#!/bin/sh
# run uwsgi in dev mode

export PYTHONPATH=`pwd`/py
export FLASK_ENV=development
export PYSRV_CONFIG_PATH=`pwd`/conf/server-config.json
uwsgi --ini conf/uwsgi.ini:uwsgi-debug

