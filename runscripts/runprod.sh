#!/bin/bash

export PATH=/reg/g/psdm/sw/conda/inst/miniconda2-prod-rhel7/bin:${PATH}
source activate ana-1.2.12

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

