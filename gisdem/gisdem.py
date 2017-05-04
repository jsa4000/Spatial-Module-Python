from downloader import download

# Check wether this is the start for the application
if  __name__ == "__main__":
    # Test download the dile
    file = download("http://www.7-zip.org/a/lzma1700.7z", "C:/jsantos")
    print(file)