
RESTPie3 - Python REST API Server Starter Kit
=============================================

This is a lightweight REST API server implemented in Python3 offering
essential web service features in a simple package. This is not a framework,
just a practical and clean codebase that relies on few core components that do
the job well. Fork and create your own REST API server quickly.

Created on Sep 2018

**Table of contents**

* [Features](#features)
* [Building blocks](#building-blocks)
* [What about the front-end?](#what-about-the-front-end)
* [Source files](#source-files)
* [Setup local dev environment](#setup-local-dev-environment)
* [API methods](#api-methods)
* [Authentication & authorization](#authentication--authorization)
* [Session data](#session-data)
* [Redis storage](#redis-storage)
* [Background workers & cron](#background-workers--cron)
* [Logging](#logging)
* [Tests](#tests)
* [Docker](#docker)
* [Script deployment](#script-deployment)
* [Setup the server](#setup-the-server)
* [Security](#security)
* [Scaling up](#scaling-up)
* [Need help?](#need-help)
* [License](#license)
* [Screenshot](#screenshot)


Features
--------

A quick list of the features of this Python API server:

* Simple and flexible server with minimum dependencies
* Process-based request workers, not thread-based nor async
* Secure server-side sessions with Redis storage
* Robust worker management: restarts, timecapping, max life
* Background tasks
* Built-in cron
* Automatic directory page listing the API methods and their docstrings [Screenshot](#screenshot)
* Redis as a generic storage with expiring keys, lightweight queues
* Email & password authentication with secure algorithms
* User role model and authorization of API methods via simple decorator
* Logging system with practical data for troubleshooting, detects slow
  requests
* Server reload on code change
* Database migrations
* Docker image for the "big cloud"
* Fast rsync deployment of updates to servers
* Tests for the API


Building blocks
---------------

The core building blocks of this server are mature open-source components that
I have years of experience of.

* [Python](http://python.org) is a high-level and versatile scripting language
  that provides powerful features with an exceptionally clear syntax.

  The language is well designed and has received increased fame and
  popularity over the recent years. Huge number of developers are picking
  Python in their work. In Sep 2017, a StackOverflow study writes about [The Incredible
  Growth of Python](https://stackoverflow.blog/2017/09/06/incredible-growth-python/):
  "Python has a solid claim to being the fastest-growing major programming
  language." In the [TIOBE index](http://www.tiobe.com/tiobe-index/)
  Python stands at position 3 as of Sep 2018.

  Having been coding Python professionally for close to two decades, I can say
  it has boosted my productivity and still is my primary language for many
  tasks, including developing the business logic in the back-end.

* [Flask](http://flask.pocoo.org/) is the Python web framework. Flask is
  considered as an unopinionated micro-framework that only provides the
  essentials of a web framework without enforcing other components (like
  database, orm, admin interface, sessions etc.) As a webdev veteran I
  appreciate this flexibility since I do want to pick the best of breed
  components myself. The core stays but other needs may vary from project to
  project, from Raspberry to the AWS cloud. The flexibility lets me be in
  control and simplify.

* [uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/) is the master daemon
  that runs and supervises the Python worker processes. uwsgi has a list of
  power features that are essential to a robust back-end: timecapped requests,
  recycling of workers, background tasks, cron jobs, timers, logging, auto
  reloads on code change, run-as privileges.

* [PostgreSQL](http://postgresql.org) is the main database, "the most advanced
  open source database" that is getting stronger every year. PostgreSQL is a
  powerhouse of features with a rock-solid implementation. Personally I enjoy
  the JSON functionality the most, since it provides good amount of
  flexibility to the relational model that I still prefer in a master database
  over the schema-free solutions.

* [Redis](https://redis.io/) is a persistent in-memory database that is used
  as a storage for server-side session data and as a lightweight caching and
  queueing system. Fast and solid.

* [Peewee](http://docs.peewee-orm.com/en/latest/) is a straightforward
  database ORM library.  It is small and easy to learn, and has all the
  necessary features.  I favor the simplicity of the ActiveRecord pattern with
  1-1 mapping of classes and database, as opposed to more complex data mapper
  pattern that is followed by the big
  [SQLAlchemy](https://www.sqlalchemy.org/) library. I know SQL and like to
  operate at the row level, and have explicit control.
  Peewee makes database access a breeze and allows you to execute raw
  SQL if you need the full power of the database. Peewee supports SQLite,
  MySQL and PostgreSQL.

  For scheme migrations,
  [Peewee-migrate](https://github.com/klen/peewee_migrate) is an easy choice
  that fits well with Peewee.


If you'd like to replace some of these components, it is possible, this is a
small codebase.


What about the front-end?
-------------------------

This is primarily a back-end Python server that provides a REST API to the
world. There is no front-end implementation in this project. This is because
the focus is on creating a good REST API server that serves web front-ends and
native mobile apps, but also because I think that it is good to modularize the
front-end and back-end code cleanly into separate code bases.

A web front-end in 2018 can be a big project with gazillion of Javascript
libraries and tools. It is better to clearly separate the front and back parts
from each other.  This can also make it easier to divide the work among
in-house/outsourced teams.

However, nothing stops you from implementing the front-end in this server
project if you want to have all the code in a single place. And if you only
need a few server generated HTML pages, you can take a look of included
[example.html](templates/example.html).

If you want inspiration of how to develop a modern web front-end that consumes
a REST API, take a look of my 2 open-sourced starter kits, one developed with
[React/Nextjs](https://github.com/tomimick/tm-nextjs-starter) and the other
with [Vue/Nuxtjs](https://github.com/tomimick/tm-nuxtjs-starter).  React and
Vue are currently the most popular Javascript frameworks to create front-ends.

The 2 front-end starters and this server handle movie data as an example. You
can connect the 2 front-ends to this server but first you need to allow
visitor access for the API methods in `api_movies.py` as the front-ends do not
implement a login.


Source files
------------

The whole of this server fits into a small set of files:

```
├── /conf/                  # configuration files
│   ├── /favicon.ico        #   site icon
│   ├── /pydaemon.service   #   systemd daemon config (if you run in a VPS)
│   ├── /robots.txt         #   deny all from robots
│   ├── /server-config.json #   main server config: db, redis, etc
│   └── /uwsgi.ini          #   uwsgi daemon config, for localdev & server
├── /migrations/            # db migrations, schema changes
│   ├── /001_users.py       #   users table, the foundation
│   └── /002_movies.py      #   movies table, just as an example
├── /py/                    # python modules
│   ├── /account.py         #   account related: passwords, user session
│   ├── /api_account.py     #   API-endpoints for login/signup/logout
│   ├── /api_dev.py         #   API-endpoints for dev/testing/api list
│   ├── /api_movies.py      #   API-endpoints for movies basic crud
│   ├── /bgtasks.py         #   background tasks, 1 sample method
│   ├── /config.py          #   central config for the app
│   ├── /cron.py            #   cron methods: run every min, hourly, daily
│   ├── /db.py              #   database classes and methods
│   ├── /main.py            #   server main
│   ├── /red.py             #   redis: get/set keyvals, lists, atomic
│   ├── /util.py            #   misc utility functions
│   └── /webutil.py         #   core web flow: before/after request, auth, role check
├── /scripts/               # scripts
│   └── /dbmigrate.py       #   db migration
├── /templates/             # templates (if you really need them)
│   └── /example.html       #   very basic jinja2 example
├── /test/                  # test scripts
│   ├── /quick.sh           #   quick adhoc calls with httpie
│   ├── /test_api.py        #   test API methods
│   ├── /test_redis.py      #   test redis module
│   └── /sample.log.txt     #   sample logging output from api test
├── Dockerfile              # docker image config
├── fabfile.py              # automation tasks: rsync deploy, migrations
├── requirements.txt        # python 3rd party dependencies
└── run.sh                  # run server locally in dev mode
```

So how do you get started with your own project? I suggest to take this route:

* browse briefly the source files, understand their role
* read and throw away `002_movies.py` and `api_movies.py`, they exist only as
  a sample
* discard `cron.py, bgtasks.py` if you don't need background processing
* discard `templates` if you only create an API server
* write your own business logic:
  * create data classes and methods in `db.py or db_x.py`
  * create API modules in `api_x.py`
  * create database migrations
  * create tests


Setup local dev environment
---------------------------

The server components run on all common OS. To start development on OSX
machine, first install [Homebrew](https://brew.sh/). You also need to have
XCode installed. (Read [Docker](#docker) if you want to take the Docker
route.)

Install the 2 external components PostgreSQL and Redis, their latest versions:

    brew install redis
    brew install postgresql

Then start the 2 components:

    brew services start postgresql
    redis-server /usr/local/etc/redis.conf

Install Python3:

    brew install python3

Python virtualenv is a tool to create isolated Python environments for project
dependencies.  Let's create and activate our environment:

    pip install virtualenv
    virtualenv --python=/usr/local/bin/python3 ~/PYSTARTERENV
    source ~/PYSTARTERENV/bin/activate
    export SERVER_VIRTUALENV=~/PYSTARTERENV/


Redis does not require more setup. For PostgreSQL, create the database and
the user: (pick your own names and secrets for the capital parts!)

    createuser MY_USER
    createdb -O tm MY_DATABASE
    psql MY_DATABASE
    alter user MY_USER with encrypted password 'MY_PASSWORD';
    create extension if not exists "uuid-ossp";


Download the sources to your local disk and install dependencies:

    git clone https://github.com/tomimick/restpie3
    cd restpie3
    pip3 install -r requirements.txt

Then clone the [config template json](conf/server-config.json) into a file
OUTSIDE the repository, and write your own PostgreSQL names and secrets from
above in the config. (It is not a good practice to commit the secrets into a
repository, so let's keep them in an external json file. Or alternatively you
can store them in environment variables.)

    cp conf/server-config.json <MY_PATH>
    pico <MY_PATH>/server-config.json
    export PYSRV_CONFIG_PATH=<MY_PATH>/server-config.json

Then initialize the database by executing the database migrations:

    python3 scripts/dbmigrate.py

Finally start the python server!

    ./run.sh

If you had trouble with these steps, please first Google around as the setup
steps may vary a little depending on OS type and component versions. Then you
could post an issue to this repository, possibly with a solution that you
found out.

If all went ok, the API site is available at localhost and you can see
the list of available API methods at
[localhost:8100/api/list](http://localhost:8100/api/list).

Whenever you modify any of the Python files, the server reloads itself.


API methods
-----------

The available API methods are implemented in api_x.py modules:

* `api_account.py` contains the core email/password login/signup/logout
  methods that you most likely need anyway.
* `api_dev.py` contains misc methods for testing and developing which you can
  discard after learning the mechanics.
* `api_movies.py` is just a sample module to demonstrate a basic CRUD REST
  API.  You definately want to discard this and transform into your actual
  data models - just read and learn it.

The server has built-in little [introspection](#screenshot) for listing the available APIs as
a HTML page.  You just declare, implement and document the API methods
normally with the Flask decorator, docstrings and the methods will be
automatically listed at
[localhost:8100/api/list](http://localhost:8100/api/list). This is a neat way
to document your server API. You can decide whether you want to disable this
functionality in production or not.

To parse and serialize JSON data I am simply using the Flask and Peewee
primitives: `jsonify, JSONEncoder and Peewee
model_to_dict/dict_to_model`. I am not using other libraries such as
[Flask-RestPlus](https://flask-restplus.readthedocs.io/en/stable/) or
[Connexion](https://github.com/zalando/connexion). I have used
[Flask-Restful](https://flask-restful.readthedocs.io/en/latest/) before but I
am not sure these libs add value. You might be able to reduce the number
of code lines a little with them but possibly loosing simplicity and control.
In my opinion Flask already provides the core I need. Adding one of these libs
is perfectly possible though should you want it.

Also I am not using [Swagger](https://swagger.io/) here but I do have felt the
temptation! The first question with Swagger would be which way to go: To first
create the API spec manually and then generate the method stubs, or first
write the methods with annotations and then generate the API spec? I am not
sure about the order and [neither is the community](https://news.ycombinator.com/item?id=14035936).  Swagger maybe good for big projects but this is a
small and cute project :)


Authentication & authorization
------------------------------

Simple email-password based signup and login authentication is included in the
server. It relies on [PassLib](https://passlib.readthedocs.io/en/stable/)
Python library for strong uptodate hashing algorithms.

A Python decorator called `login_required` can be inserted before an API
method that controls that the method requires an authenticated user session,
and optionally to specify if the method requires a certain user level. User
accounts have a role-field whose value is one of:

```python
    user.role = (disabled, readonly, editor, admin, superuser)
```

You can set the user roles that are meaningful for your project, see the
migration [001_users.py](migrations/001_users.py). If this simple linear role
model is too limited, you can introduce a capability model perhaps with a text
array field, similar to `user.tags`.

For example, this method requires that the user is logged on and has a role
editor:

```python
    @app.route('/api/movies/', methods = ['POST'])
    @login_required(role='editor')
    def movie_create():
        """Creates a movie and returns it."""
        #...code here...
```

If the user does not have an editor role or above, the API server returns 401
Unauthorized to the client.

API methods which don't have a `login_required` decorator attached are
available for anybody, including non authenticated visitors.

Accounts with role=disabled are stopped at the door and not let in to the
server at all.

If you want to support Facebook or Google OAuth authentication method, I
recommend you use the [rauth](https://github.com/litl/rauth) library.

By default the server allows accessing the API from all domains, CORS
`Access-Control-Allow-Origin value='*'` but it can be set in the config file.


Session data
------------

Server-side session data is stored in Redis. Data written into a session is
not visible at the client side.

Flask provides a thread-global session object that acts like a dictionary. You
set keys to values in the session. A value can be any object that can be
[pickled](https://docs.python.org/3/library/pickle.html). Modifications to the
session data are automatically saved to Redis by Flask at the end of the
request.

This starter stores two core data in the session: `userid` and `role` of the
user.

A common operation in an API method is to access the calling user object,
myself.  There is a call `webutil.get_myself()` that loads myself from the
database, or None for a visitor.

Flask also provides a thread-global object called `g` where you can store
data, but this data is *only stored for the duration of the request.* This
data is not stored in Redis and is discarded when the request ends. `g` can be
used for caching common data during the request, but don't overuse it.

Redis is a persistent storage, unlike memcached, which means that if the
server gets rebooted, the user sessions will be restored and logged-in users
do not need to relogin.

By default, the session is remembered for 1 month. If there is no user
activity during 1 month, the session gets deleted. This time is controlled by
PERMANENT_SESSION_LIFETIME in [config.py](py/config.py).


Redis storage
-------------

You can also use Redis for other than session data. Redis can act as a
convenient schema-free storage for various kinds of data, perhaps for
temporary data, or for lists whose size can be limited, or act as a
distributed cache within a cluster of servers.

A typical case might be that a background worker puts the calculation results
into Redis where the data is picked from by an API method (if the result is
secondary in nature and does not belong to the master database).

The module [red.py](py/red.py) provides simple methods for using Redis:

```python
    # store a value into Redis (here value is a dict but can be anything)
    value = {"type":"cat", "name":"Sophia"}
    red.set_keyval("mykey", value)

    # get a value
    value = red.get_keyval("mykey")

    # store a value that will expire/disappear after 70 minutes:
    red.set_keyval("cron_calculation_cache", value, 70*60)
```

To append data into a list:

```python
    # append item into a list
    item = {"action":"resize", "url":"https://example.org/a.jpg"}
    red.list_append("mylist", item)

    # take first item from a list
    item = red.list_pop("mylist")

    # append item into a FIFO list with a max size of 100
    # (discards the oldest items first)
    red.list_append("mylist", data_item, 100)
```

red.py can be extended to cover more functionality that
[Redis provides](https://redis.io/commands).


Background workers & cron
-------------------------

uwsgi provides a simple mechanism to run long running tasks in background
worker processes.

In any Python module (like in [bgtasks.py](py/bgtasks.py)) you have this code:

```python
    @spool(pass_arguments=True)
    def send_email(*args, **kwargs):
        """A background worker that is executed by spooling arguments to it."""
        #...code here...
```

You start the above method in a background worker process like this:

```python
    bgtasks.send_email.spool(email="tomi@tomicloud.com",
            subject="Hello world!", template="welcome.html")
```

The number of background worker processes is controlled by `spooler-processes`
configuration in [uwsgi.ini](conf/uwsgi.ini). The spooled data is written and
read into a temp file on disk, not in Redis.

Crons are useful for running background tasks in specified times, like in
every hour or every night. uwsgi has an easy built-in support for crons. To
have a nightly task you simple code:

```python
    @cron(0,2,-1,-1,-1)
    #(minute, hour, day, month, weekday) - in server local time
    def daily(num):
        """Runs every night at 2:00AM."""
        #...code here...
```


Logging
-------

Logging is an essential tool in monitoring and troubleshooting the server
operation. This server automatically logs several useful data in the log file,
including the request path, method and parameters, and return codes and
tracebacks. Userid and origin ip address is logged too.

Secrets should not be written into a log file to prevent unnecessary leakage
of data.  Currently this server automatically prevents logging keys
["password", "passwd", "pwd"] if they exist in the input parameters of an API
method. You should extend this list to cover your secret keys.

In local development, the log is dumped to the console, and at server the log
is dumped to a file `/app/app.log`. It is also possible to send the logging
output to a remote `rsyslog`. This can be useful in a cluster setup.

Slow queries that take more than 1 second to finish are logged with a warning
SLOW! and the log line includes the actual amount of time it took to respond.
It is good to monitor where the pressure starts to cumulate in a server and
then optimize the code or put the execution into a background worker.

Requests that take more than 20 seconds get terminated and the following line
is logged: `HARAKIRI ON WORKER 1 (pid: 47704, try: 1)`. This harakiri time is
configurable.

To log the executed SQL statements during development, you can execute:

    # dump SQL
    export PYSRV_LOG_SQL=1
    # stop dumping SQL
    export PYSRV_LOG_SQL=

Note that as the server logs may contain sensitive data, you should not keep
the production logs for too long time, and you should mention in the policy
statement what data you collect. The GDPR legislation in Europe has a saying
on this.

To monitor the log file in realtime at server you can invoke:

    tail -f -n 500 /app/app.log

As an example, the server logs [this output](test/sample.log.txt) when the
included API tests are run.


Tests
-----

The test folder contains two test scripts for testing the server API and the
Redis module. Keeping tests up-todate and running them frequently or
automatically during the process is a safety net that protects you from
mistakes and bugs.  With dynamic languages such as Python or Javascript or
Ruby, tests are even more important than with compiled languages.

For locally run tests I expose a method `/apitest/dbtruncate` in
[api_dev.py](py/api_dev.py) that truncates the data in the database tables
before running the API tests. If you like to write tests in a different way,
just remove it.


Docker
------
The server can be dockerized with the included [Dockerfile](Dockerfile). The
base image is the popular lightweight Alpine Linux with the latest Python 3.7.

Build the docker image:

    docker build -t pysrv:0.0.1 .

Run the docker image locally:

    docker run -p 8100:80 pysrv:0.0.1

The generated image size is 256MB. With some docker tricks it might be
possible to reduce the build size further.

If you use PostgreSQL and Redis that are installed in the localhost, the
configured host for both should be `host.docker.internal`.

If you plan to developed with Docker locally, and not with Python virtualenv,
use volumes that map Linux folders to your host folders and enable uwsgi hot
reload `py-autoreload=1` on code change.


Script deployment
-----------------

Even though the world is crazy about Docker, I still often like to deploy code
directly and quickly to VPS servers, especially during project start and early
development. Setting up the components and the environment at server requires
some initial effort but you then have absolute control and visibility to
the whole server. Not every project needs a big cluster first.

Setting up a whole cluster at [AWS ECS](https://aws.amazon.com/ecs/) is no
easy feat, you need to learn and configure A LOT.
[Dokku](http://dokku.viewdocs.io/dokku/) seems nice but has limitations,
allowing to run only a single Docker image. I wish the container/Kubernetes industry still matures more and provides a
[Heroku](https://www.heroku.com/)-like effortless deployments of Docker
images.

So if you have plain VPS servers, and want to have super speedy updates from
localhost to the servers, I have created a single Python script
[fabfile.py](fabfile.py) that automates the deployment. It relies on [Fabric tool](http://www.fabfile.org/) that rsyncs the source code securely over SSH.

The deployment is activated just with:

    fab deploy

This transfers only the changed source files from localhost to a server,
performs database migrations and restarts the Python server. All in just
4 seconds. This makes the core dev/test loop really fast.

In any case, this is just an optional script. If you have a big environment,
you most likely have a Continous Integration / Deployment solution in place.


Setup the server
----------------

Here are rough steps about how to setup a VPS server for this Python server.
This is not a tutorial, I assume you know Linux and SSH basics.

During the development of this project I used latest Ubuntu 18.04 myself.
These steps should work for Ubuntu. Steps will vary depending on your OS and
version. Python3.x comes pre-installed in recent Ubuntus.

Install PostgreSQL and Redis at server:

    sudo apt-get update
    sudo apt-get install redis-server
    sudo apt-get install postgresql
    sudo apt-get install python3-pip
    mkdir /app/

Then configure PostgreSQL at server in a similar way as explained for a local
setup [above](#setup-local-dev-environment).

Write the IP-address or server name locally in your fabfile.py as
TEST_SERVER. Plus add your SSH credentials and a path to your public key.
Then transfer source files to the server, and install the
[systemd daemon](conf/pydaemon.service):

    # locally
    fab deploy
    fab deploy_mydaemon

Install Python libraries:

    sudo pip3 install -r /app/requirements.txt

Edit the json config file at server, write PostgreSQL credentials:

    cd /app/
    cp conf/server-config.json real-server-config.json
    pico /app/real-server-config.json

And finally re-deploy: (does database migration, server restart)

    # locally
    fab deploy

For a production setup you must also configure uwsgi to run as a lower
privileged user and not as a root! Check the [uwsgi guide](https://uwsgi-docs.readthedocs.io/en/latest/).


Security
--------

A few words about security practices in this software:

* no secrets are stored in code but in an external configuration file or in
  environment variables
* all requests are logged and can be inspected later
* no secrets are leaked to the log file
* server based sessions with an opaque uuid cookie
* no Javascript access to uuid cookie
* config to require https for cookies (do enable in production)
* strong algorithms are used for password auth
* only salt and password hash is stored in the database
* session can be either permanent or end on browser close
* sensitive user objects have a random uuid and not an integer id
* possible to add a fresh cookie check by saving IP+agent string to session
* database code is not vulnerable to SQL injections
* authorization is enforced via user roles and function decorator, not
  requiring complex code
* uwsgi supports running code as a lower privileged user
* uwsgi supports SSL certificates (but a load balancer or nginx in front is
  recommended as SSL endpoint)

Of course the overall security of the service is also heavily dependent on the
configuration of the server infrastructure and access policies.


Scaling up
----------

While the codebase of this server is small, it has decent muscle. The
*stateless* design makes it perfectly possible to scale it up to work in a
bigger environment. There is nothing in the code that "does not scale". The
smallness and flexibility of the software makes it actually easier to scale,
allowing easier switch of components in case that is needed. For
example, you can start with the uwsgi provided background tasks framework and
replace that later on with, say [Celery](http://www.celeryproject.org/), if
you see it scales and fits better.

In a traditional setup you first scale up vertically, you "buy a bigger
server".  This code contains a few measures that helps scaling up
vertically:

* you can add worker processes to match the single server capacity
* you can add more background processes if there is a lot of background jobs
* slow requests are logged so you see when they start to cumulate
* stuck requests never halt the whole server - stuck workers are killed after
  20 seconds by default, freeing resources to other workers (harakiri)
* you can optimize SQL, write raw queries, let the database do work better
* you can cache data in Redis

When you outgrow the biggest single server, and start adding servers, you
scale horizontally. The core API server component can be cloned into a cluster
of servers where each of them operates independently of the others. Scaling
the API server here is easy, it is the other factors that become harder, like
database scaling and infra management.


Need help?
----------

This starter is intended to provide you a quick start in building a great
foundation for an API back-end. Take this code and see if it works for you.
This server is not a toy - it is a practical, solid server that is based on my
experience in building full-stack services over the years.

If you need dev power in building your great service, back or front, you can
[contact me](mailto:tomi.mickelsson@gmail.com) to ask if I am available for
freelancing work.


License
-------
MIT License


Screenshot
----------

[/api/list](http://localhost:8100/api/list) returns an HTML page that lists
the available API methods and their docstring automatically.

![API-listing](test/api-list.png)

