import unittest
from geobricks_downloader.core.utils import dict_merge


class GeobricksUtilsTest(unittest.TestCase):

    def setUp(self):
        self.a = {'name': 'Guido', 'family': 'Barbaglia', 'role': 'developer'}
        self.b = {'name': 'Simone', 'family': 'Murzilli'}
        self.d = {'name': 'Guido', 'family': 'Barbaglia', 'role': {'title': 'developer', 'short': 'dev'}}

    def test_dict_merge(self):
        c = dict_merge(self.a, self.b)
        self.assertEquals(c['name'], 'Simone')
        self.assertEquals(c['family'], 'Murzilli')
        self.assertEquals(c['role'], 'developer')
        c = dict_merge(self.a, 'Hallo, World!')
        self.assertEquals(c, 'Hallo, World!')
        c = dict_merge(self.d, self.b)
        self.assertEquals(c['name'], 'Simone')
        self.assertEquals(c['family'], 'Murzilli')
        self.assertTrue(type(c['role']), dict)
