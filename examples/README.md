Examples
========
Download MODIS tiles
--------------------
```python
from geobricks_downloader.download.downloader import Downloader


file_paths_and_sizes = [
    {
        'file_name': 'my_modis_tile.hdf',
        'file_path': 'ftp://ladsweb.nascom.nasa.gov/allData/5/MOD13Q1/2014/001/MOD13Q1.A2014001.h02v08.005.2014018082809.hdf'
    }
]
file_system_structure = '/home/user/Desktop/MODIS'
d = Downloader('modis', file_system_structure, file_paths_and_sizes)
d.download()
```
Download MODIS tiles with the Geobricks MODIS plug-in
-----------------------------------------------------
The Geobricks MODIS plug-in is available on [GitHub](https://github.com/geobricks/geobricks_modis) and on [PyPi](https://pypi.python.org/pypi/GeobricksMODIS). The plug-in provides methods to filter the MODIS FTP based on the product code, the datetime and the geographic area. The following example shows how to download the tiles covering Angola for the MOD13A2 product on January 1st 2010 through the use of the Geobricks MODIS plug-in.
```python
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
target = '/home/user/Desktop/MODIS'

# Run the downloader
Downloader('modis', target, layers_to_be_downloaded).download()
```
