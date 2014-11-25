import json
from flask import Blueprint
from flask import Response
from flask.ext.cors import cross_origin


download = Blueprint('download', __name__)


@download.route('/discovery/')
@cross_origin(origins='*')
def discovery():
    """
    Discovery service available for all Geobricks libraries that describes the plug-in.
    @return: Dictionary containing information about the service.
    """
    out = {
        'name': 'DOWNLOAD',
        'description': 'Geobricks download functionalities and services.',
        'type': 'SERVICE'
    }
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')