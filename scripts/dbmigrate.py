#!/usr/bin/python
# -*- coding: utf-8 -*-

# dbmigrate.py: migrate the local database
#   - run either on dev machine or at server
#
# Author: Tomi.Mickelsson@iki.fi

import os
import config

cmd = "pw_migrate migrate --database=postgresql://{}:{}@localhost/{}".format(
        config.DATABASE_USER,
        config.DATABASE_PASSWORD,
        config.DATABASE_NAME)

ret = os.system(cmd)
if ret:
    print("migrate ERROR", ret)
else:
    print("migrate OK")

