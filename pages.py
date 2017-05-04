from flask import Blueprint, Response
import context

__author__ = 'mshankar@slac.stanford.edu'

pages_blueprint = Blueprint('pages_api', __name__)

@pages_blueprint.route("/<experiment_name>/", methods=["GET"])
@pages_blueprint.route("/<experiment_name>/summary.html", methods=["GET"])
@context.security.authentication_required
@context.security.authorization_required("read")
def mainSummary(experiment_name):
    return Response("This is the summary page with a link to <a href='a/child/page'>a child page</a>", mimetype='text/html')

@pages_blueprint.route("/<experiment_name>/<path:page>", methods=["GET"])
@context.security.authentication_required
@context.security.authorization_required("read")
def otherPages(experiment_name, page):
    return Response("You want {} for experiment {}".format(page, experiment_name), mimetype='text/html')
