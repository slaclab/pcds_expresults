import os
import logging
from flask import Blueprint, Response, abort, current_app, send_file, render_template
from config import EXP_RESULTS_FOLDER
import context
import mimetypes

__author__ = 'mshankar@slac.stanford.edu'

pages_blueprint = Blueprint('pages_api', __name__)
mimetypes.init()
logger = logging.getLogger(__name__)

# This is copied over from explgbk; that's the original for this method.
@pages_blueprint.route('/js/<path:path>')
def send_js(path):
    pathparts = os.path.normpath(path).split(os.sep)
    if pathparts[0] == 'python':
        # This is code for gettting the JS file from the package data of the python module.
        filepath = pkg_resources.resource_filename(pathparts[1], os.sep.join(pathparts[2:]))
        if os.path.exists(filepath):
            # logger.debug("Found file %s as part of a python package resources", filepath)
            return send_file(filepath)


    # $CONDA_PREFIX/lib/node_modules/jquery/dist/
    filepath = os.path.join(os.getenv("CONDA_PREFIX"), "lib", "node_modules", path)
    if not os.path.exists(filepath):
        filepath = os.path.join(os.getenv("CONDA_PREFIX"), "lib", "node_modules", pathparts[0], "dist", *pathparts[1:])
    if os.path.exists(filepath):
        return send_file(filepath)
    else:
        logger.error("Cannot find static file %s in %s", path, filepath)
        abort(404)
        return None


@pages_blueprint.route("/<instrument_name>/<experiment_id>-<experiment_name>", methods=["GET"])
@pages_blueprint.route("/<instrument_name>/<experiment_id>-<experiment_name>/summary.html", methods=["GET"])
@context.security.authentication_required
@context.security.authorization_required("read")
def mainSummary(instrument_name, experiment_id, experiment_name):
    instrument_name = instrument_name.lower()
    # First check to see if the run summary folder exists for the experiment
    expResultsFolder = os.path.join(EXP_RESULTS_FOLDER, instrument_name, experiment_name, "stats", "summary")
    logger.debug("Looking for summary results for experiment {} in folder {}".format(experiment_name, expResultsFolder))

    if not os.path.exists(expResultsFolder):
        logger.debug("Cannot find the folder %s; note this could also be a problem with file system permissions.", expResultsFolder)
        return Response("There are no summary stats for {}".format(experiment_name), mimetype='text/html')

    logger.debug("Found the path %s", expResultsFolder)
    if not os.path.isdir(expResultsFolder):
        return Response("The summary stats path {} is not a folder for {}".format(expResultsFolder, experiment_name), mimetype='text/html')

    logger.debug("Found the folder %s", expResultsFolder)
    if os.path.exists(os.path.join(expResultsFolder, "report.html")):
        logger.debug("Found an report.html")
        return send_file(os.path.join(expResultsFolder, "report.html"), mimetype='text/html')

    # The default is to send a list of folders as links.
    links = []
    for folderName in sorted(os.listdir(expResultsFolder)):
        if os.path.isdir(os.path.join(expResultsFolder, folderName)) and os.path.exists(os.path.join(expResultsFolder, folderName, "report.html")):
            links.append(folderName)
    else:
        logger.debug("'{}' does not exist?".format(os.path.join(expResultsFolder, "report.html")))

    return render_template("expsummary.html",
                           links=links,
                           experiment_id=experiment_id,
                           experiment_name=experiment_name
                           )


@pages_blueprint.route("/<instrument_name>/<experiment_id>-<experiment_name>/<path:page>", methods=["GET"])
@context.security.authentication_required
@context.security.authorization_required("read")
def otherPages(instrument_name, experiment_id, experiment_name, page):
    instrument_name = instrument_name.lower()
    # First check to see if the run summary folder exists for the experiment
    expResultsPage = os.path.join(EXP_RESULTS_FOLDER, instrument_name, experiment_name, "stats", "summary", page)
    logger.debug("Looking for page {} for experiment {} in folder {}".format(page, experiment_name, expResultsPage))

    if not os.path.exists(expResultsPage):
        abort(404)
        return
    return send_file(expResultsPage, mimetypes.guess_type(expResultsPage)[0])
