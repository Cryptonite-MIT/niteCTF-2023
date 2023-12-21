#!/bin/sh

# cd /home/user && \
#     gunicorn -w "$((3 * $(getconf _NPROCESSORS_ONLN) / 2 + 1))" -k uvicorn.workers.UvicornWorker main:app -b "0.0.0.0:$1" --access-logfile '-'

cd /home/user && \
    gunicorn -w 3 -k main.ServerlessUvicornWorker main:app -b "0.0.0.0:$1" --access-logfile '-'
