FROM python:3.7-alpine3.8

WORKDIR /app

# add dependencies, use --virtual deps for build time modules only,
# then remove to reduce image size
COPY requirements.txt /app/requirements.txt
RUN apk update && apk add --virtual deps gcc linux-headers musl-dev postgresql-dev libffi-dev make
RUN pip install -r /app/requirements.txt
RUN apk del deps

# this postgresql lib is needed
RUN apk add --no-cache libpq

# copy source files
COPY conf /app/conf
COPY py /app/py
COPY migrations /app/migrations
COPY scripts /app/scripts
COPY templates /app/templates
COPY test /app/test

# background spooler dir
RUN mkdir /tmp/pysrv_spooler

# we don't need this file with Docker but uwsgi looks for it
RUN echo `date +%s` >/app/VERSION

EXPOSE 80


# our server config file
# - you should write your own config file and put OUTSIDE the repository
#   since the config file contains secrets
# - here I use the sample template from repo
# - it is also possible to override the config with env variables, either here
#   or in Amazon ECS or Kubernetes configuration
COPY conf/server-config.json /app/real-server-config.json
# ENV PYSRV_DATABASE_HOST host.docker.internal
# ENV PYSRV_REDIS_HOST host.docker.internal
# ENV PYSRV_DATABASE_PASSWORD x

# build either a production or dev image
ARG BUILDMODE=production
ENV ENVBUILDMODE=$BUILDMODE

RUN echo "BUILDMODE $ENVBUILDMODE"

# run in shell mode with ENV expansion
CMD uwsgi --ini /app/conf/uwsgi.ini:uwsgi-$ENVBUILDMODE

