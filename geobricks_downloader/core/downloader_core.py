import uuid

from geobricks_downloader.core import log
from geobricks_downloader.config.downloader_config import config
from geobricks_downloader.core.filesystem import create_filesystem
from geobricks_downloader.core.downloads_thread_manager import DownloadsThreadManager


downloaders_map = {}


class Downloader():

    # Mandatory parameters.
    source = None
    file_paths_and_sizes = None
    filesystem_structure = None
    target_root = None

    # Optional parameters.
    username = None
    password = None
    threaded = False

    # Derived parameters.
    id = None
    source_type = 'FTP'
    config = None
    target_dir = None
    download_manager = None

    def __init__(self, source, target_root, file_system_structure, file_paths_and_sizes,
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

        # Store object
        self.id = str(uuid.uuid4())
        downloaders_map[self.id] = self

        # Store parameters.
        self.source = source.lower()
        self.file_paths_and_sizes = file_paths_and_sizes
        self.file_system_structure = file_system_structure
        self.target_root = target_root
        self.username = username
        self.password = password
        self.threaded = threaded
        self.block_size = block_size

        # Merge datasource specific configuration with generic configuration
        self.config = config

        # Derive other parameters.
        self.log = log.logger(self.__class__.__name__)
        self.target_dir = self.target_root

        # Read target root from common settings, if available
        if self.target_dir is None:
            try:
                self.target_dir = self.config['settings']['target_root']
            except KeyError:
                raise Exception('Please provide the target folder.')

        self.target_dir = create_filesystem(self.target_dir, self.file_system_structure, self.config)
        self.uuid = str(uuid.uuid4())

    def download(self):
        self.download_manager = DownloadsThreadManager(self.uuid,
                                                       self.target_dir,
                                                       self.file_paths_and_sizes,
                                                       self.threaded)
        self.download_manager.start()
        out = {
            'id': self.id,
            'downloaded_files': self.download_manager.downloaded_files
        }
        return out

    def progress(self, filename):
        return self.download_manager.progress(filename)