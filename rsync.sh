#!/bin/sh
# rsync files to server and reload

# HOST: replace with your real data
HOST='pi@192.168.100.10'

echo "RSYNCING in 3secs..."
sleep 3

rsync -av --exclude '.git' --exclude '__pycache__' --exclude '*.pyc' --exclude '*.sqlite' * $HOST:/app/

# ask python server to reload sources
ssh $HOST touch /app/VERSION

