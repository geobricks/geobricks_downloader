import os
import unittest
from geobricks_downloader.core.downloader_core import Downloader


class GeobricksDownloaderTest(unittest.TestCase):

    def setUp(self):
        self.day = '001'
        self.year = '2015'
        self.product = 'MOD13A1'
        self.target_root = '/tmp'
        self.file_system_structure = {'product': self.product, 'year': self.year, 'day': self.day}
        self.local_file_name = 'test.hdf'
        self.local_file_name_1 = 'test_1.hdf'
        self.local_file_name_2 = 'test_2.hdf'
        self.layers_to_be_downloaded = [
            {
                'file_name': self.local_file_name,
                'file_path': 'ftp://ladsweb.nascom.nasa.gov/'
                             'allData/5/MOD13A1/2015/001/MOD13A1.A2015001.h13v08.005.2015027153318.hdf'
            }
        ]
        self.multiple_layers_to_be_downloaded = [
            {
                'file_name': self.local_file_name_1,
                'file_path': 'ftp://ladsweb.nascom.nasa.gov/allData/5/MOD13A1/2015/001/'
                             'MOD13A1.A2015001.h13v08.005.2015027153318.hdf'
            },
            {
                'file_name': self.local_file_name_2,
                'file_path': 'ftp://ladsweb.nascom.nasa.gov/allData/5/MOD13A1/2015/001/'
                             'MOD13A1.A2015001.h13v01.005.2015027152312.hdf'
            }
        ]

    def test_download_tiles(self):
        my_downloader = Downloader('modis',
                                   self.target_root,
                                   self.file_system_structure,
                                   self.layers_to_be_downloaded,
                                   True)
        downloaded_layers = my_downloader.download()['downloaded_files']
        self.assertEquals(len(downloaded_layers), 1)
        download_in_progress = True
        while download_in_progress:
            try:
                download_in_progress = my_downloader.progress(
                    self.local_file_name)['download_size'] != my_downloader.progress(self.local_file_name)['total_size']
            except TypeError:
                pass
            except KeyError:
                pass
        local_path = os.path.join(self.target_root, self.product, self.year, self.day)
        self.assertTrue(os.path.exists(local_path))
        local_file = os.path.join(local_path, self.local_file_name)
        self.assertTrue(os.path.isfile(local_file))
        actual = os.stat(local_file).st_size
        desired = 2824180
        self.assertTrue(float(actual) / float(desired) >= 0.95)

    def test_download_multiple_tiles(self):
        my_downloader = Downloader('modis',
                                   self.target_root,
                                   self.file_system_structure,
                                   self.multiple_layers_to_be_downloaded,
                                   True)
        downloaded_layers = my_downloader.download()['downloaded_files']
        self.assertEquals(len(downloaded_layers), 2)
        download_in_progress_1 = True
        download_in_progress_2 = True
        while download_in_progress_1 or download_in_progress_2:
            try:
                download_in_progress_1 = my_downloader.progress(
                    self.local_file_name_1)['download_size'] != my_downloader.progress(
                    self.local_file_name_1)['total_size']
                download_in_progress_2 = my_downloader.progress(
                    self.local_file_name_2)['download_size'] != my_downloader.progress(
                    self.local_file_name_2)['total_size']
            except TypeError:
                pass
            except KeyError:
                pass
        local_path = os.path.join(self.target_root, self.product, self.year, self.day)
        self.assertTrue(os.path.exists(local_path))
        local_file_1 = os.path.join(local_path, self.local_file_name_1)
        self.assertTrue(os.path.isfile(local_file_1))
        actual = os.stat(local_file_1).st_size
        desired = 2824180
        self.assertTrue(float(actual) / float(desired) >= 0.95)
        local_file_2 = os.path.join(local_path, self.local_file_name_2)
        self.assertTrue(os.path.isfile(local_file_2))
        actual = os.stat(local_file_2).st_size
        desired = 2564354
        self.assertTrue(float(actual) / float(desired) >= 0.95)
