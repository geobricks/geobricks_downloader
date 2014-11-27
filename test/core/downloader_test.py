from geobricks_downloader.core.downloader_core import Downloader
from geobricks_downloader.core.downloader_core import downloaders_map
from geobricks_modis.core.modis_core import list_layers_countries_subset
import sched, time

s = sched.scheduler(time.time, time.sleep)

def progress(id, filename):
    try:
        obj = downloaders_map[id].progress(filename)
        print '[' + obj['file_name'] + '] | ' + str(obj['progress']) + '%'
    except KeyError:
        pass


# Filters
product = 'MOD13A2'
year = '2014'
day = '001'
country = 'PT'

# Get the list of layers through the Geobricks MODIS plug-in
layers_to_be_downloaded = list_layers_countries_subset(product, year, day, country)

# Target folder: MODIS layers will be downloaded here
target_root = '/Users/simona/Desktop/MODIS'
# target_root = None
file_system_structure = {'product': product, 'year': year, 'day': day}
# file_system_structure = None

# Run the downloader
my_downloader = Downloader('modis', target_root, file_system_structure, layers_to_be_downloaded, True)
downloaded_layers = my_downloader.download()['downloaded_files']
id = my_downloader.download()['id']
print downloaded_layers
print id
print 'MOD13A2.A2014001.h17v04.005.2014018084326.hdf'
print
for i in range(3, 33, 3):
    s.enter(i, 1, progress, (id, 'MOD13A2.A2014001.h17v04.005.2014018084326.hdf',))
    s.enter(i, 1, progress, (id, 'MOD13A2.A2014001.h17v05.005.2014018082847.hdf',))
s.run()