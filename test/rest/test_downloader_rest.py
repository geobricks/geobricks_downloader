import json
import unittest
from flask import Flask
from geobricks_downloader.rest.downloader_rest import downloader


class GeobricksDownloaderRestTest(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(downloader, url_prefix='/download')
        self.tester = self.app.test_client(self)
        self.local_file_name = 'test.hdf'
        self.local_file_name_1 = 'test_1.hdf'
        self.local_file_name_2 = 'test_2.hdf'
        self.day = '001'
        self.year = '2015'
        self.product = 'MOD13A1'

    def test_discovery(self):
        response = self.tester.get('/download/discovery/', content_type='application/json')
        out = json.loads(response.data)
        self.assertEquals(out['name'], 'DOWNLOAD')
        self.assertEquals(out['type'], 'SERVICE')

    def test_download(self):
        response = self.tester.post('/download/modis/',
                                    data=json.dumps({
                                        'target_root': '/tmp',
                                        'layers_to_be_downloaded': [
                                            {
                                                'file_name': self.local_file_name,
                                                'file_path': 'ftp://ladsweb.nascom.nasa.gov/allData/5/MOD13A1/2015/001/'
                                                             'MOD13A1.A2015001.h13v08.005.2015027153318.hdf'
                                            }
                                        ],
                                        'file_system_structure': {
                                            'product': self.product,
                                            'year': self.year,
                                            'day': self.day
                                        }
                                    }),
                                    content_type='application/json')
        out = json.loads(response.data)
        self.assertEquals(out['downloaded_files'][0], 'test.hdf')
        self.assertEquals(len(out['downloaded_files']), 1)
        response = self.tester.post('/download/modis/',
                                    data=json.dumps({
                                        'target_root': '/tmp',
                                        'layers_to_be_downloaded': [
                                            {
                                                'file_name': self.local_file_name,
                                                'file_path': 'ftp://ladsweb.nascom.nasa.gov/allData/5/MOD13A1/2015/001/'
                                                             'MOD13A1.A2015001.h13v08.005.2015027153318.hdf'
                                            }
                                        ],
                                        'file_system_structure': {
                                            'non_valid_key': self.product,
                                            'year': self.year,
                                            'day': self.day
                                        }
                                    }),
                                    content_type='application/json')
        json.loads(response.data)

    def test_download_multiple_files(self):
        response = self.tester.post('/download/modis/',
                                    data=json.dumps({
                                        'target_root': '/tmp',
                                        'layers_to_be_downloaded': [
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
                                        ],
                                        'file_system_structure': {
                                            'product': self.product,
                                            'year': self.year,
                                            'day': self.day
                                        }
                                    }),
                                    content_type='application/json')
        out = json.loads(response.data)
        self.assertEquals(out['downloaded_files'][0], 'test_1.hdf')
        self.assertEquals(out['downloaded_files'][1], 'test_2.hdf')
        self.assertEquals(len(out['downloaded_files']), 2)
