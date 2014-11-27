import json
from flask import request
from flask import Response
from flask import Blueprint
from flask.ext.cors import cross_origin
from geobricks_downloader.core.downloader_core import Downloader


downloader = Blueprint('download', __name__)


@downloader.route('/discovery/')
@cross_origin(origins='*', headers=['Content-Type'])
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


@downloader.route('/<datasource>/', methods=['POST'])
@cross_origin(origins='*', headers=['Content-Type'])
def download(datasource):

    # Fetch the payload
    payload = request.get_json()

    # Store user parameters
    target_root = payload['target_root']
    layers_to_be_downloaded = payload['layers_to_be_downloaded']
    file_system_structure = None

    try:
        file_system_structure = payload['file_system_structure']
    except KeyError:
        pass

    # Start the download
    out = Downloader(datasource, target_root, file_system_structure, layers_to_be_downloaded).download()

    # Return the list of downloaded files
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')