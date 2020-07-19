#!/bin/bash

source /reg/g/psdm/sw/dm/conda/etc/profile.d/conda.sh
conda activate /reg/g/psdm/sw/dm/conda/envs/psdm_ws_0_0_10

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

# Assume that the current directory for the process is this directory.
export PYTHONPATH="modules/flask_authnz:${PYTHONPATH}"

export ACCESS_LOG_FORMAT='%(h)s %(l)s %({REMOTE_USER}i)s %(t)s "%(r)s" %(s)s %(b)s %(D)s'

export SERVER_IP_PORT=${SERVER_IP_PORT:-"0.0.0.0:9471"}

exec gunicorn start:app -b ${SERVER_IP_PORT} --worker-class eventlet --no-sendfile --reload \
       --log-level=DEBUG --capture-output --enable-stdio-inheritance \
       --access-logfile - --access-logformat "${ACCESS_LOG_FORMAT}" \
       --timeout 300 --graceful-timeout 1
