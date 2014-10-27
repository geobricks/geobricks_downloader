from importlib import import_module


class Downloader():

    # Mandatory parameters.
    source = None
    file_paths_and_sizes = None

    # Optional parameters.
    filesystem_structure = None
    username = None
    password = None

    # Derived parameters.
    source_type = 'FTP'
    config = None

    def __init__(self, source, file_paths_and_sizes, username=None, password=None):

        # Store parameters.
        self.source = source.lower()
        self.file_paths_and_sizes = file_paths_and_sizes
        self.username = username
        self.password = password

        # Load configuration
        module_name = 'geobricks_' + self.source + '.config.' + self.source + '_config'
        mod = import_module(module_name)
        self.config = getattr(mod, 'config')

        # Derive other parameters.
        self.source_type = self.config['source']['type']

    def download_standard(self):
        pass

    def download_threaded(self):
        pass


file_paths_and_sizes = [
    {
        'file_name': 'MOD13A2.A2010001.h22v05.005.2010028060252.hdf',
        'size': '21340759',
        'file_path': 'ftp://ladsweb.nascom.nasa.gov/allData/5/MOD13A2/2010/001/MOD13A2.A2010001.h22v05.005.2010028060252.hdf',
        'label': 'H 22, V 05 (21.34 MB)'
    }
]
d = Downloader('MOdis', file_paths_and_sizes, None)
d.download_standard()
print d.source_type