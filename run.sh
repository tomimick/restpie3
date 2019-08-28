#!/bin/sh
# run in dev mode

# uwsgi --ini conf/uwsgi.ini:uwsgi-debug
docker run --rm --name restpie-dev -p 8100:80 -v ~/Downloads/restpie3/py:/app/pylocal restpie-dev-image

