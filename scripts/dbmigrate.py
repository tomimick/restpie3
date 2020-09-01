#!/usr/bin/python
# -*- coding: utf-8 -*-

# dbmigrate.py: migrate the local database
#   - run either on dev machine or at server
#
# Author: Tomi.Mickelsson@iki.fi

import os
import config

if config.DATABASE_HOST.startswith("/"):
    # sqlite
    # note: can't use full path here!
    # db will appear in "/app/data/mydb.sqlite" (mapped volume locally)
    cmd = "pw_migrate migrate --directory=/app/migrations_sqlite --database=sqlite:/data/mydb.sqlite"
else:
    # postgresql
    cmd = "pw_migrate migrate --database=postgresql://{}:{}@{}:{}/{}".format(
        config.DATABASE_USER,
        config.DATABASE_PASSWORD,
        config.DATABASE_HOST,
        config.DATABASE_PORT,
        config.DATABASE_NAME)

print(cmd)

ret = os.system(cmd)
if ret:
    print("migrate ERROR", ret)
else:
    print("migrate OK")

