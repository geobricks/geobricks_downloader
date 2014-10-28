from importlib import import_module
from types import StringType
from types import DictType
from geobricks_downloader.utils.filesystem import create_filesystem


class Downloader():

    # Mandatory parameters.
    source = None
    file_paths_and_sizes = None

    # Can be a string with the folder or a hierarchical tree
    # e.g. {'target': '/home/kalimaha/Desktop/MODIS', 'product': 'MOD13Q1', 'year': '2014', 'day': '033'}
    filesystem_structure = None

    # Optional parameters.
    username = None
    password = None

    # Derived parameters.
    source_type = 'FTP'
    config = None
    target_dir = None

    def __init__(self, source, file_system_structure, file_paths_and_sizes, username=None, password=None):

        # Store parameters.
        self.source = source.lower()
        self.file_paths_and_sizes = file_paths_and_sizes
        self.file_system_structure = file_system_structure
        self.username = username
        self.password = password

        # Load configuration
        module_name = 'geobricks_' + self.source + '.config.' + self.source + '_config'
        mod = import_module(module_name)
        self.config = getattr(mod, 'config')

        # Derive other parameters.
        self.source_type = self.config['source']['type']
        self.target_dir = file_system_structure
        if type(file_system_structure) is DictType:
            self.target_dir = file_system_structure['target']
            self.target_dir = create_filesystem(self.target_dir, self.file_system_structure, self.config)

    def download_standard(self):
        pass

    def download_threaded(self):
        pass


file_system_structure = {'target': '/home/kalimaha/Desktop/MODIS', 'product': 'MOD13Q1', 'year': '2014', 'day': '033'}
# file_system_structure = '/home/kalimaha/Desktop/MODIS2'
file_paths_and_sizes = [
    {
        'target': '/home/kalimaha/Desktop/MODIS',
        'file_name': 'MOD13A2.A2010001.h22v05.005.2010028060252.hdf',
        'size': '21340759',
        'file_path': 'ftp://ladsweb.nascom.nasa.gov/allData/5/MOD13A2/2010/001/MOD13A2.A2010001.h22v05.005.2010028060252.hdf',
        'label': 'H 22, V 05 (21.34 MB)'
    }
]
d = Downloader('MOdis', file_system_structure, file_paths_and_sizes, None)
d.download_standard()
print d.source_type
print '>>> ' + d.target_dir
print type('pippo') is StringType
print type({'pippo': 'asd'}) is DictType