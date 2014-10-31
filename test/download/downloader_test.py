from geobricks_downloader.download.downloader import Downloader
from geobricks_modis.core.modis_core import list_layers_countries_subset


# Filters
product = 'MOD13A2'
year = '2010'
day = '001'
country = '8'

# Get the list of layers through the Geobricks MODIS plug-in
layers_to_be_downloaded = list_layers_countries_subset(product, year, day, country)

# Target folder: MODIS layers will be downloaded here
target = '/home/kalimaha/Desktop'

# Run the downloader
# Downloader('modis', target, layers_to_be_downloaded).download()
Downloader('modis', target, layers_to_be_downloaded, True).download()