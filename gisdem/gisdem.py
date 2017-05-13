from downloader import download
from utils import timeit


@timeit
def tstDownload(*args, **kw):
    return download(*args, **kw)


# Check wether this is the start for the application
if  __name__ == "__main__":
    file = tstDownload(url, path, overwrite=False)
    print("File donwloaded: " + file)
