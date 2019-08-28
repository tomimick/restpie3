#!/usr/bin/python
# -*- coding: utf-8 -*-

# fabfile.py: automated tasks
#   - deploy sources from local machine to test/production server
#   - migrate local/server database
#
# Author: Tomi.Mickelsson@iki.fi

import sys
import os
import time
import io

from fabric.api import env, run, task, sudo, local, put
from fabric.contrib.console import confirm
from fabric.contrib.project import rsync_project
from fabric.operations import prompt


# write your own server info here:
TEST_SERVER = "testserver.mydomain.com"
PRODUCTION_SERVER = "www.mydomain.com"
SSH_USER = ""
SSH_PRIVATE_KEY = "~/.ssh/xxx_rsa"


# --------------------------------------------------------------------------
# fabric reads these

env.hosts = [TEST_SERVER]
env.use_ssh_config = True
env.user = SSH_USER
env.remotedir = "/app/"
env.port = 22
env.key_filename = SSH_PRIVATE_KEY

# --------------------------------------------------------------------------
# DATABASE TASKS

@task
def postgres_migrate_local():
    """Local database migrate"""
    local("python scripts/dbmigrate.py")

@task
def postgres_migrate_remote():
    """Server database migrate"""
    dir = env.remotedir
    cmd = "cd {}; PYTHONPATH={}py PYSRV_CONFIG_PATH={} python3 scripts/dbmigrate.py".format(dir, dir, dir+"real-server-config.json")
    run(cmd)

@task
def postgres_run_server():
    local("postgres -D /usr/local/var/postgres")

@task
def postgres_list_tables():
    sql = "SELECT * FROM pg_catalog.pg_tables WHERE schemaname = 'public'"
    local("psql -d tmdb -c \"{}\"".format(sql))

@task
def postgres_list_users():
    sql = "SELECT * FROM users"
    local("psql -d tmdb -c \"{}\"".format(sql))

@task
def postgres_gen_models():
    """Generate peewee models from database: generated-models.py"""

    cmd = "pwiz.py -e postgresql -u tm -P tmdb >generated-models.py"
    local(cmd)


# --------------------------------------------------------------------------
# DEPLOY TASKS

@task
def production():
    """Set target host to production server"""

    if confirm("DEPLOY PRODUCTION, YOU SURE ??????", default=False):
        env.hosts = [PRODUCTION_SERVER]
        print("Deploying soon... ", env.hosts[0].upper())
        # wait a little so you can still stop...
        time.sleep(5)
    else:
        print("Exiting")
        sys.exit(1)

@task
def deploy():
    """Deploy current local sources to server + db migration"""

    rsync_files()

    postgres_migrate_remote()

    # touch VERSION, uwsgi will then restart automatically
    data = io.StringIO("%d" % time.time())
    put(data, "/app/VERSION", use_sudo=False)


def rsync_files():
    """rsync source files to remote server"""

    exclude_list = ['*.pyc', '.git', '.DS_Store', 'node_modules', '__pycache__',
            'doc', 'trash']

    rsync_project(env.remotedir, local_dir=".", delete=False,
            default_opts='-hrvz', exclude=exclude_list,
            extra_opts=' -O --no-perms --checksum')

@task
def deploy_mydaemon():
    """Update uwsgi master config conf/pydaemon.service, then restart"""

    sudo("systemctl stop pydaemon", warn_only=True)

    put("conf/pydaemon.service", "/etc/systemd/system/", use_sudo=True)

    sudo("systemctl enable pydaemon")
    sudo("systemctl daemon-reload")
    sudo("systemctl start pydaemon")

