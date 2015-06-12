import os
import unittest
from geobricks_downloader.core.filesystem import create_filesystem
from geobricks_downloader.core.filesystem import create_folder


class GeobricksFilesystemTest(unittest.TestCase):

    def setUp(self):
        self.day = '001'
        self.year = '2015'
        self.product = 'MOD13A1'
        self.root = '/tmp'
        self.structure = {'product': self.product, 'year': self.year, 'day': self.day}
        self.config = {'settings': {'target_root': None}}
        self.folder = {'folder_name': '{{tmp}}'}

    def test_create_filesystem(self):
        create_filesystem(self.root, self.structure, self.config)
        local_path = os.path.join(self.root, self.product, self.year, self.day)
        self.assertTrue(os.path.exists(local_path))

    def test_create_folder(self):
        create_folder(self.config, self.structure, self.folder, self.root)
        local_path = os.path.join(self.root, self.product, self.year, self.day)
        self.assertTrue(os.path.exists(local_path))

    def test_root_does_not_exist(self):
        root = '/tmp/tmp2'
        create_filesystem(root, self.structure, self.config)
        local_path = os.path.join(root, self.product, self.year, self.day)
        self.assertTrue(os.path.exists(local_path))
