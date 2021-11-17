import os
import logging
from flask import Blueprint, Response, abort, current_app, send_file, render_template, jsonify
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

@pages_blueprint.route("/<instrument>/<experiment>/", methods=["GET"])
@context.security.authentication_required
@context.security.authorization_required("read")
def mainSummary(instrument, experiment):
    instrument = instrument.lower()
    # First check to see if the run summary folder exists for the experiment
    expResultsFolder = os.path.join(EXP_RESULTS_FOLDER, instrument, experiment, "stats", "summary")
    logger.debug("Looking for summary results for experiment {} in folder {}".format(experiment, expResultsFolder))

    if not os.path.exists(expResultsFolder):
        logger.debug("Cannot find the folder %s; note this could also be a problem with file system permissions.", expResultsFolder)
        return Response("There are no summary stats for {}".format(experiment), mimetype='text/html')

    logger.debug("Found the path %s", expResultsFolder)
    if not os.path.isdir(expResultsFolder):
        return Response("The summary stats path {} is not a folder for {}".format(expResultsFolder, experiment), mimetype='text/html')

    logger.debug("Found the folder %s", expResultsFolder)
    if os.path.exists(os.path.join(expResultsFolder, "report.html")):
        logger.debug("Found an report.html")
        return send_file(os.path.join(expResultsFolder, "report.html"), mimetype='text/html')

    return render_template("expsummary.html", experiment=experiment, instrument=instrument)


@pages_blueprint.route("/<instrument>/<experiment>/<path:page>", methods=["GET"])
@context.security.authentication_required
@context.security.authorization_required("read")
def otherPages(instrument, experiment, page):
    instrument = instrument.lower()
    expResultsFolder = os.path.join(EXP_RESULTS_FOLDER, instrument, experiment, "stats", "summary")
    expResultsPage = os.path.join(expResultsFolder, page)
    logger.debug("Looking for page {} for experiment {} in folder {}".format(page, experiment, expResultsPage))

    if os.path.exists(expResultsPage):
        return send_file(expResultsPage, mimetypes.guess_type(expResultsPage)[0])


    abort(404)
    return


@pages_blueprint.route("/ws/<instrument>/<experiment>/reportfolders", methods=["GET"])
@context.security.authentication_required
@context.security.authorization_required("read")
def svc_walk_stats_summary_tree(instrument, experiment):
    """
    Walk the stats summary and return a list of paths that have report.htmls in them.
    Return an array of dicts of paths with report.html's in them. For example, if subF1/subF2/subf-uglymol/report.html, return { "root": "subF1/subF2/subf-uglymol" }
    """
    instrument = instrument.lower()
    expResultsFolder = os.path.join(EXP_RESULTS_FOLDER, instrument, experiment, "stats", "summary")
    fldrs = []
    for (root, dirs, files) in os.walk(expResultsFolder, followlinks=False):
        if "report.html" in files:
            fldrs.append({"root": root[len(expResultsFolder)+1:], "hasReport": True})
    return jsonify({'success': True, 'value': fldrs})
