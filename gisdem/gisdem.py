from downloader import download
from utils import timeit

@timeit
def tstDownload(url, filename=None, filepath=None, rawdata=False):
    return download(url, filename, filepath,rawdata)

    
# Declare global nam and paths
name = "test.exe"
path = "C:/jsantos"

# url = "http://www.7-zip.org/a/lzma1700.7z"
# url = "https://repo.continuum.io/archive/.winzip/Anaconda3-4.3.1-Windows-x86.zip"
#url = "http://api.openstreetmap.org/api/0.6/map?bbox=11.54,48.14,11.543,48.145"
#url = "https://pypi.python.org/packages/99/d9/cbe540a9fe5aa7a7f13f500ebdea37a129b59864409ad6ea3f1498765d3a/lxml-3.4.4-cp26-none-win_amd64.whl#md5=8be9744c37f912849797e54af79944b4"
url = "http://erki.lap.ee/downloads/skyperious/skyperious_3.4_x64_setup.exe"

# Check wether this is the start for the application
if  __name__ == "__main__":
    file = tstDownload(url, path)
    print("File donwloaded: " + file)
    

    #http://www.opentopography.org/developers#GMRT
    # Open Topology -> to download Elevation Maps in SRTMGL3, SRTMGL3, etc..

    #Base URL
    #http://opentopo.sdsc.edu/otr/

    #Required Parameters
    #You must POST the following parameters:

    #For GET capabilities
    # http://opentopo.sdsc.edu/geoportal/csw/discovery?Request=GetCapabilities&Service=CSW&Version=2.0.2

    #demtype 	The global raster dataset - SRTM GL3 (90m) is 'SRTMGL3', SRTM GL1 (30m) is 'SRTMGL1', SRTM GL1 (Ellipsoidal) is 'SRTMGL1_E', and ALOS World 3D 30m is 'AW3D30'
    #west, south, east, north 	WGS 84 bounding box coordinates
    #outputFormat 	outputFormat Output Format (optional) - GTiff for GeoTiff, AAIGrid for Arc ASCII Grid, HFA for Erdas Imagine (.IMG). Defaults to GTiff if parameter is not provided

    # Open Street map