from geobricks_downloader.download.downloader import Downloader
from geobricks_modis.core.modis_core import list_layers_countries_subset


layers_to_be_downloaded = list_layers_countries_subset('MOD13A2', '2010', '001', '8')
print layers_to_be_downloaded
target = '/home/kalimaha/Desktop'

Downloader('modis', target, layers_to_be_downloaded).download()