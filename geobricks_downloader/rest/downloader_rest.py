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

    # Filters
    product = 'MOD13A2'
    year = '2010'
    day = '001'
    country = '8'

    # Get the list of layers through the Geobricks MODIS plug-in
    layers_to_be_downloaded = [
        {
            'file_name': 'my_modis_tile.hdf',
            'file_path': 'ftp://ladsweb.nascom.nasa.gov/allData/5/MOD13Q1/2014/001/MOD13Q1.A2014001.h02v08.005.2014018082809.hdf'
        }
    ]

    # Target folder: MODIS layers will be downloaded here
    target_root = '/home/kalimaha/Desktop/MODIS'
    target_root = None
    file_system_structure = {'product': product, 'year': year, 'day': day}

    # Initiate the downloader
    my_downloader = Downloader('modis', target_root, file_system_structure, layers_to_be_downloaded)

    # Run the downloader
    print my_downloader.download()

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