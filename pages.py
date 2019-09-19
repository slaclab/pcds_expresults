import os
from flask import Blueprint, Response, abort, current_app, send_file, render_template
from config import EXP_RESULTS_FOLDER
import context
import mimetypes

__author__ = 'mshankar@slac.stanford.edu'

pages_blueprint = Blueprint('pages_api', __name__)
mimetypes.init()

@pages_blueprint.route("/<instrument_name>/<experiment_id>-<experiment_name>", methods=["GET"])
@pages_blueprint.route("/<instrument_name>/<experiment_id>-<experiment_name>/summary.html", methods=["GET"])
@context.security.authentication_required
@context.security.authorization_required("read")
def mainSummary(instrument_name, experiment_id, experiment_name):
    instrument_name = instrument_name.lower()
    # First check to see if the run summary folder exists for the experiment
    expResultsFolder = os.path.join(EXP_RESULTS_FOLDER, instrument_name, experiment_name, "stats", "summary")
    current_app.logger.debug("Looking for summary results for experiment {} in folder {}".format(experiment_name, expResultsFolder))

    if not os.path.exists(expResultsFolder):
        return Response("There are no summary stats for {}".format(experiment_name), mimetype='text/html')

    if not os.path.isdir(expResultsFolder):
        return Response("The summary stats path {} is not a folder for {}".format(expResultsFolder, experiment_name), mimetype='text/html')
    
    if os.path.exists(os.path.join(expResultsFolder, "report.html")):
        current_app.logger.debug("Found an report.html")
        return send_file(os.path.join(expResultsFolder, "report.html"), mimetype='text/html')
    # The default is to send a list of folders as links.
    links = []
    for folderName in sorted(os.listdir(expResultsFolder)):
        if os.path.isdir(os.path.join(expResultsFolder, folderName)) and os.path.exists(os.path.join(expResultsFolder, folderName, "report.html")):
            links.append(folderName)
	else:
	    current_app.logger.debug("'{}' does not exist?".format(os.path.join(expResultsFolder, folderName, "report.html")))
    
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
    current_app.logger.debug("Looking for page {} for experiment {} in folder {}".format(page, experiment_name, expResultsPage))

    if not os.path.exists(expResultsPage):
        abort(404)
        return
    return send_file(expResultsPage, mimetypes.guess_type(expResultsPage)[0])