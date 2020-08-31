#!/bin/sh
# run in dev mode

docker build --build-arg BUILDMODE=debug-docker -t restpie-dev-image .

