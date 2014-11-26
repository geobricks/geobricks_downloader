from geobricks_downloader.core.downloader_core import Downloader
from geobricks_modis.core.modis_core import list_layers_countries_subset


# Filters
product = 'MOD13A2'
year = '2014'
day = '001'
country = 'PT'

# Get the list of layers through the Geobricks MODIS plug-in
layers_to_be_downloaded = list_layers_countries_subset(product, year, day, country)

# Target folder: MODIS layers will be downloaded here
target_root = '/home/kalimaha/Desktop/MODIS'
target_root = None
file_system_structure = {'product': product, 'year': year, 'day': day}
# file_system_structure = None

# Run the downloader
my_downloader = Downloader('modis', target_root, file_system_structure, layers_to_be_downloaded, True)
downloaded_layers = my_downloader.download()