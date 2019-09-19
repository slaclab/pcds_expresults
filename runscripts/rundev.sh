#!/bin/bash

source /reg/g/psdm/sw/dmconda/etc/profile.d/conda.sh
conda activate /reg/g/psdm/sw/dmconda/envs/psdm_ws_0_0_5

[ -z "$ROLES_DATABASE_HOST" ] && export ROLES_DATABASE_HOST="localhost"
[ -z "$ROLES_DATABASE_DB" ] && export ROLES_DATABASE_DB="roles"
[ -z "$ROLES_DATABASE_USER" ] && export ROLES_DATABASE_USER="test"
[ -z "$ROLES_DATABASE_PASSWORD" ] && export ROLES_DATABASE_PASSWORD="test"


# Assume that we are running the in root folder of this package
PRNT_DIR=`dirname $PWD`
G_PRNT_DIR=`dirname $PRNT_DIR`;
GG_PRNT_DIR=`dirname $G_PRNT_DIR`;
GGG_PRNT_DIR=`dirname $GG_PRNT_DIR`;


CONFIG_FILE="${GGG_PRNT_DIR}/appdata/pcds_expresults/pcds_expresults.sh"
echo "External config file is ${CONFIG_FILE}"

if [[ -f "${CONFIG_FILE}" ]]
then
   echo "Sourcing deployment specific configuration from ${CONFIG_FILE}"
   source "${CONFIG_FILE}"
fi


# Pick up psdmauth for the test deployment
export PYTHONPATH="${GG_PRNT_DIR}/psdmauth/src:${PYTHONPATH}"
echo "Using psdmauth from ${PYTHONPATH}"

export ACCESS_LOG_FORMAT='%(h)s %(l)s %({REMOTE_USER}i)s %(t)s "%(r)s" %(s)s %(b)s %(D)s'
exec gunicorn start:app -b 0.0.0.0:9471 --worker-class eventlet --reload \
       --log-level=DEBUG --capture-output --enable-stdio-inheritance \
       --access-logfile - --access-logformat "${ACCESS_LOG_FORMAT}"


#       --log-file /u1/logs/pcds_expresults.log \
