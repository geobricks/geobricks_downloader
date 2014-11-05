import os
import urllib2
from importlib import import_module
from types import DictType
from geobricks_downloader.download.downloads_thread_manager import DownloadsThreadManager
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

    def __init__(self, source, file_system_structure, file_paths_and_sizes,
                 threaded=False, block_size=16384, username=None, password=None):

        """
        @type source:                   str
        @param source:                  e.g. 'modis', either lower or upper case.

        @type file_system_structure:    str | dict
        @param file_system_structure:   This parameter can be either a String, representing the target directory for the
                                        downloads (e.g. '/home/user/Desktop'), or a Dict, describing the file system
                                        structure (e.g. {'target': '/home/kalimaha/Desktop/MODIS', 'product': 'MOD13Q1',
                                        'year': '2014', 'day': '033'})

        @type file_paths_and_sizes:     collection
        @param file_paths_and_sizes:    Collection of objects containing the following fields: 'file_name', 'size',
                                        'file_path', 'label'.

        @type threaded:                 bool
        @param threaded:                Run the downloader in multiple or single thread mode.

        @type block_size:               float
        @param block_size:              The remote file is downloaded in chunk, each one of 'block_size' size.

        @type username:                 str
        @param username:                Optional parameter.

        @type password:                 str
        @param password:                Optional parameter.

        """

        # Store parameters.
        self.source = source.lower()
        self.file_paths_and_sizes = file_paths_and_sizes
        self.file_system_structure = file_system_structure
        self.username = username
        self.password = password
        self.threaded = threaded
        self.block_size = block_size

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
        downloaded_layers = []
        for layer in self.file_paths_and_sizes:
            download_size = 0
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
                        chunk = u.read(self.block_size)
                        if not buffer:
                            break
                        file_size_dl += len(chunk)
                        f.write(chunk)
                        download_size += len(chunk)
                        self.log.info('Progress: ' + str(progress(download_size, total_size)))
                        if float(download_size) == float(total_size):
                            break
                f.close()
                self.log.info(layer['file_name'] + ' downloaded.')
            else:
                self.log.info(layer['file_name'] + ' is already in the filesystem.')
            downloaded_layers.append(local_file)
        return downloaded_layers

    def download_threaded(self):
        mgr = DownloadsThreadManager('uid', self.target_dir, self.file_paths_and_sizes)
        mgr.start()
        return mgr.downloaded_files


def progress(downloaded, total):
    return round(float(downloaded) / float(total) * 100, 2)