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
    