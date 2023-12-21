#!/bin/sh

/usr/local/bin/gunicorn -w 1 -k main.ServerlessUvicornWorker main:app -b "0.0.0.0:$1" --access-logfile '-'

# /usr/local/bin/uvicorn main:app --no-server-header --host 0.0.0.0 --port "$1"
