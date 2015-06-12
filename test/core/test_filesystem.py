import os
import unittest
from geobricks_downloader.core.filesystem import create_filesystem


class GeobricksFilesystemTest(unittest.TestCase):

    def test_create_filesystem(self):
        day = '001'
        year = '2015'
        product = 'MOD13A1'
        root = '/tmp'
        structure = {'product': product, 'year': year, 'day': day}
        config = {'settings': {'target_root': None}}
        create_filesystem(root, structure, config)
        local_path = os.path.join(root, product, year, day)
        self.assertTrue(os.path.exists(local_path))
