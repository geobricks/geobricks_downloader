import os
import urllib2
from importlib import import_module
from types import DictType
from geobricks_downloader.utils.filesystem import create_filesystem
from geobricks_downloader.utils import log


class Downloader():

    # Mandatory parameters.
    source = None
    file_paths_and_sizes = None

    # This can be a string with the target folder or a hierarchical tree
    # e.g. {'target': '/home/kalimaha/Desktop/MODIS', 'product': 'MOD13Q1', 'year': '2014', 'day': '033'}
    filesystem_structure = None

    # Optional parameters.
    username = None
    password = None
    threaded = False

    # Derived parameters.
    source_type = 'FTP'
    config = None
    target_dir = None

    def __init__(self, source, file_system_structure, file_paths_and_sizes, threaded=False, username=None, password=None):

        """
        @type source:                   String
        @param source:                  e.g. 'modis', either lower or upper case.

        @type file_system_structure:    String | Dict
        @param file_system_structure:   This parameter can be either a String, representing the target directory for the
                                        downloads (e.g. '/home/user/Desktop'), or a Dict, describing the file system
                                        structure (e.g. {'target': '/home/kalimaha/Desktop/MODIS', 'product': 'MOD13Q1',
                                        'year': '2014', 'day': '033'})

        @type file_paths_and_sizes:     Array
        @param file_paths_and_sizes:    Collection of objects containing the following fields: 'file_name', 'size',
                                        'file_path', 'label'.

        @type threaded:                 Boolean
        @param threaded:                Run the downloader in multiple or single thread mode.

        @type username:                 String
        @param username:                Optional parameter.

        @type password:                 String
        @param password:                Optional parameter.

        """

        # Store parameters.
        self.source = source.lower()
        self.file_paths_and_sizes = file_paths_and_sizes
        self.file_system_structure = file_system_structure
        self.username = username
        self.password = password
        self.threaded = threaded

        # Load configuration
        module_name = 'geobricks_' + self.source + '.config.' + self.source + '_config'
        mod = import_module(module_name)
        self.config = getattr(mod, 'config')

        # Derive other parameters.
        self.log = log.logger(self.__class__.__name__)
        self.source_type = self.config['source']['type']
        self.target_dir = file_system_structure
        if type(file_system_structure) is DictType:
            self.target_dir = file_system_structure['target']
            self.target_dir = create_filesystem(self.target_dir, self.file_system_structure, self.config)

    def download(self):
        return self.download_threaded() if self.threaded else self.download_standard()

    def download_standard(self):
        for layer in self.file_paths_and_sizes:
            download_size = 0
            total_size = 0
            block_sz=16384
            local_file = os.path.join(self.target_dir, layer['file_name'])
            if 'size' in layer and layer['size'] is not None:
                total_size = layer['size']
            else:
                u = urllib2.urlopen(layer['file_path'])
                meta = u.info()
                total_size = int(meta.getheaders('Content-Length')[0])
            allow_layer_download = True
            try:
                allow_layer_download = int(os.stat(local_file).st_size) < int(total_size)
            except OSError:
                pass
            if allow_layer_download:
                self.log.info('Downloading: ' + layer['file_name'])
                u = urllib2.urlopen(layer['file_path'])
                f = open(local_file, 'wb')
                if not os.path.isfile(local_file) or os.stat(local_file).st_size < total_size:
                    file_size_dl = 0
                    while download_size < total_size:
                        chunk = u.read(block_sz)
                        if not buffer:
                            break
                        file_size_dl += len(chunk)
                        f.write(chunk)
                        download_size += len(chunk)
                        self.log.info('Progress: ' + str(self.progress(download_size, total_size)))
                        if download_size == total_size:
                            break
                f.close()
                self.log.info(layer['file_name'] + ' downloaded.')
            else:
                self.log.info(layer['file_name'] + ' is already in the filesystem.')

    def download_threaded(self):
        pass

    def progress(self, downloaded, total):
        return round(float(downloaded) / float(total) * 100, 2)


file_paths_and_sizes = [
    {
        'size': None,
        'label': 'H 22, V 05 (21.34 MB)',
        'file_name': 'MOD13Q1.A2014001.h02v08.005.2014018082809.hdf',
        'file_path': 'ftp://ladsweb.nascom.nasa.gov/allData/5/MOD13Q1/2014/001/MOD13Q1.A2014001.h02v08.005.2014018082809.hdf'
    },
    {
        'size': None,
        'label': None,
        'file_name': 'MyMODIS.hdf',
        'file_path': 'ftp://ladsweb.nascom.nasa.gov/allData/5/MOD13Q1/2014/001/MOD13Q1.A2014001.h02v09.005.2014018084818.hdf'
    }
]
file_system_structure = {'target': '/home/kalimaha/Desktop/MODIS', 'product': 'MOD13Q1', 'year': '2014', 'day': '001'}
# file_system_structure = '/home/kalimaha/Desktop/MODIS'
d = Downloader('MOdis', file_system_structure, file_paths_and_sizes)
# d = Downloader('MOdis', file_system_structure, file_paths_and_sizes, True)
d.download()