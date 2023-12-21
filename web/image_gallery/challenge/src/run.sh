#!/bin/sh

# cd /home/user && \
#     gunicorn -w "$((3 * $(getconf _NPROCESSORS_ONLN) / 2 + 1))" -b "0.0.0.0:1337" --access-logfile '-' main:app

cd /home/user && \
    gunicorn -w 3 -b "0.0.0.0:1337" --access-logfile '-' main:app
