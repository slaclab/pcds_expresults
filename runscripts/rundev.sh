#!/bin/bash

source /reg/g/psdm/bin/conda_setup ""

[ -z "$ROLES_DATABASE_HOST" ] && export ROLES_DATABASE_HOST="localhost"
[ -z "$ROLES_DATABASE_DB" ] && export ROLES_DATABASE_DB="roles"
[ -z "$ROLES_DATABASE_USER" ] && export ROLES_DATABASE_USER="test"
[ -z "$ROLES_DATABASE_PASSWORD" ] && export ROLES_DATABASE_PASSWORD="test"


# Assume that we are running the in root folder of this package
PRNT_DIR=`dirname $PWD`
G_PRNT_DIR=`dirname $PRNT_DIR`;

# Pick up psdmauth for the test deployment
export PYTHONPATH="${PRNT_DIR}/psdmauth/src:${PYTHONPATH}"
echo "Using psdmauth from ${PYTHONPATH}"

export ACCESS_LOG_FORMAT='%(h)s %(l)s %({REMOTE_USER}i)s %(t)s "%(r)s" %(s)s %(b)s %(D)s'
gunicorn start:app -b 0.0.0.0:5000 --worker-class eventlet --reload \
       --log-level=DEBUG --capture-output --enable-stdio-inheritance \
       --access-logfile - --access-logformat "${ACCESS_LOG_FORMAT}"


#       --log-file /u1/logs/pcds_expresults.log \


