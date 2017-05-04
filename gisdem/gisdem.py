from downloader import download

# Check wether this is the start for the application
if  __name__ == "__main__":
    # Test download the dile
    #file = download("http://www.7-zip.org/a/lzma1700.7z", "C:/jsantos")
    file = download("http://api.openstreetmap.org/api/0.6/map?bbox=11.54,48.14,11.543,48.145", outname="map.osm", outpath="C:/jsantos")
    print(file)