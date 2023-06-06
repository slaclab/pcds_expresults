#!/bin/bash

cd /work/pcds_expresults

export MONGODB_USERNAME=$(< /work/secrets/username)
export MONGODB_PASSWORD=$(< /work/secrets/password)
export MONGODB_HOSTS=$(< /work/secrets/hosts)

export PYTHONPATH="modules/flask_authnz:${PYTHONPATH}"

export ACCESS_LOG_FORMAT='%(h)s %(l)s %({REMOTE_USER}i)s %(t)s "%(r)s" %(s)s %(b)s %(D)s'
export LOG_LEVEL=${LOG_LEVEL:-"DEBUG"}

export SERVER_IP_PORT=${SERVER_IP_PORT:-"0.0.0.0:5000"}

gunicorn start:app -b ${SERVER_IP_PORT} --worker-class gthread --reload \
       --log-level=${LOG_LEVEL} --capture-output --enable-stdio-inheritance \
       --access-logfile - --access-logformat "${ACCESS_LOG_FORMAT}" \
       --timeout 300 --graceful-timeout 1
