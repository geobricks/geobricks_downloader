import unittest
from geobricks_downloader.core.utils import dict_merge


class GeobricksUtilsTest(unittest.TestCase):

    def setUp(self):
        self.a = {'name': 'Guido', 'family': 'Barbaglia', 'role': 'developer'}
        self.b = {'name': 'Simone', 'family': 'Murzilli'}

    def test_dict_merge(self):
        c = dict_merge(self.a, self.b)
        self.assertEquals(c['name'], 'Simone')
        self.assertEquals(c['family'], 'Murzilli')
        self.assertEquals(c['role'], 'developer')