import time
import sched
from geobricks_downloader.download.downloader import Downloader
from geobricks_modis.core.modis_core import list_layers_countries_subset


# Filters
product = 'MOD13A2'
year = '2014'
day = '001'
country = 'PT'

# Get the list of layers through the Geobricks MODIS plug-in
layers_to_be_downloaded = list_layers_countries_subset(product, year, day, country)

# Target folder: MODIS layers will be downloaded here
target = {'target': '/home/kalimaha/Desktop/MODIS', 'product': product, 'year': year, 'day': day}

# Run the downloader
my_downloader = Downloader('modis', target, layers_to_be_downloaded, True)
downloaded_layers = my_downloader.download()