import os
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
            self.log.info(layer)
            local_file = os.path.join(self.target_dir, layer['file_name'])
            self.log.info(local_file)

    def download_threaded(self):
        print 'THREADED'


file_paths_and_sizes = [
    {
        'size': '21340759',
        'label': 'H 22, V 05 (21.34 MB)',
        'file_name': 'MOD13A2.A2010001.h22v05.005.2010028060252.hdf',
        'file_path': 'ftp://ladsweb.nascom.nasa.gov/allData/5/MOD13A2/2010/001/MOD13A2.A2010001.h22v05.005.2010028060252.hdf'
    }
]
file_system_structure = {'target': '/home/kalimaha/Desktop/MODIS', 'product': 'MOD13Q1', 'year': '2014', 'day': '033'}
# file_system_structure = '/home/kalimaha/Desktop/MODIS'
d = Downloader('MOdis', file_system_structure, file_paths_and_sizes)
print d.target_dir
# d = Downloader('MOdis', file_system_structure, file_paths_and_sizes, True)
d.download()