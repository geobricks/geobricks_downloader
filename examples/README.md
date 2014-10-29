Examples
========
Download MODIS tiles
--------------------
```python
from geobricks_downloader.download.downloader import Downloader


layers_to_be_downloaded = [
    {
        'file_name': 'my_modis_tile.hdf',
        'file_path': 'ftp://ladsweb.nascom.nasa.gov/allData/5/MOD13Q1/2014/001/MOD13Q1.A2014001.h02v08.005.2014018082809.hdf'
    }
]
target = '/home/user/Desktop'
d = Downloader('modis', target, layers_to_be_downloaded)
d.download()
```
The `layers_to_be_downloaded` variable is a Python array, and each element must have the following structure:
```python
{
    'file_path': 'ftp://path/to/your/resource',
    'file_name': 'my_modis_tile.hdf'
}
```
where `file_path` is the URL to the remote resource to be downloaded and `file_name` is the name of the file that will be stored on the local file system. This method is quite tedious and not very convenient. The best way to take advantage of the Geobricks Downloader is through the use of its plug-ins, as described in the next example.
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
target = '/home/user/Desktop'

# Initiate the downloader
my_downloader = Downloader('modis', target, layers_to_be_downloaded)

# Run the downloader
my_downloader.download()
```
This example produces an output similar to the following:
```
29-10-2014 | 16:03:1414594992 | INFO     | Downloader | Line: 98    | Downloading: MOD13A2.A2010001.h19v09.005.2010026214458.hdf
29-10-2014 | 16:03:1414594994 | INFO     | Downloader | Line: 110   | Progress: 0.1 (16384 / 17203608)
29-10-2014 | 16:03:1414594994 | INFO     | Downloader | Line: 110   | Progress: 0.19 (32768 / 17203608)
...
29-10-2014 | 16:03:1414594992 | INFO     | Downloader | Line: 110   | Progress: 99.89 (17874944 / 17894371)
29-10-2014 | 16:03:1414594992 | INFO     | Downloader | Line: 110   | Progress: 99.98 (17891328 / 17894371)
29-10-2014 | 16:03:1414594992 | INFO     | Downloader | Line: 110   | Progress: 100.0 (17894371 / 17894371)
29-10-2014 | 16:03:1414594992 | INFO     | Downloader | Line: 114   | MOD13A2.A2010001.h19v09.005.2010026214458.hdf downloaded.
```
There are several ways to filter the MODIS FTP, please refer to the [Geobricks MODIS plug-in example page](https://github.com/geobricks/geobricks_modis/tree/master/examples) for further details.
