import os
import urlparse

__author__ = 'mshankar@slac.stanford.edu'

DEBUG = True

# Various constants used for configuration. 
# The experiment result stats will be stored in a folder like /reg/d/psdm/dia/diadaq13/stats/summary
EXP_RESULTS_FOLDER = os.environ.get("EXP_RESULTS_FOLDER", "/reg/g/psdm")