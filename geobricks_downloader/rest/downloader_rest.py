import json
from flask import Blueprint
from flask import Response
from flask.ext.cors import cross_origin
from geobricks_downloader.core.downloader_core import Downloader


downloader = Blueprint('download', __name__)


@downloader.route('/discovery/')
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
    target = '/home/user/Desktop'

    # Initiate the downloader
    my_downloader = Downloader('modis', None, layers_to_be_downloaded)

    # Run the downloader
    my_downloader.download()

    return Response(json.dumps(out), content_type='application/json; charset=utf-8')