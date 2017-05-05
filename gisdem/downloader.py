import shutil
import requests
from utils import ProgressBar

def get_filename_from_header(header):
    # This function will look for the following field in the header.
    # 'Content-Disposition': 'attachment; filename="skyperious_3.4_x64_setup.exe"',
    if 'Content-Disposition' in header:
        return header['Content-Disposition'].split('filename=')[-1].strip('"')
    return None

def download(url, filepath=None, filename=None, rawdata=False, chunk_size=512):
    """
        Download a file from the current URL by doing an http request via GET.
        Returns the name of the file downloaded if succesful.
        None is there was an error in the conexion or donwloading the file.

        HTTP Headers:
            {
            'Connection': 'Keep-Alive',
            'Server': 'Apache/2.4.18 (Ubuntu)', 
            'Content-Disposition': 'attachment; filename="map.osm"', 
            'Transfer-Encoding': 'chunked',
            'Content-Encoding': 'gzip', 
            'Keep-Alive': 'timeout=5, max=100',
            'Content-Type': 'text/xml; charset=utf-8',
            'Cache-Control': 'private, max-age=0, must-revalidate', 
            'Date': 'Fri, 05 May 2017 11:04:47 GMT'
            }

            {
            'Content-Disposition': 'attachment; filename="skyperious_3.4_x64_setup.exe"',
            'Last-Modified': 'Wed, 15 Apr 2015 19:56:30 GMT',
            'Server': 'Apache', 
            'Content-Length': '19461432',
            'Keep-Alive':
            'timeout=15, max=100', 
            'Content-Type': 'application/x-msdownload',
            'Connection': 'Keep-Alive',
            'Date': 'Fri, 05 May 2017 10:10:13 GMT',
            'Accept-Ranges': 'bytes'
            }

            {
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-7z-compressed',
            'Last-Modified': 'Sat, 29 Apr 2017 10:30:32 GMT',
            'Date': 'Fri, 05 May 2017 10:33:35 GMT', 
            'Content-Length': '984103',
            'Accept-Ranges': 'bytes',
            'Server': 'nginx/1.6.2 (Ubuntu)',
            'ETag': '"59046b48-f0427"'
            }
    """
    # Do the GET request to the url passed by commands
    #   request.request("GET",url) -> "GET, "POST", "UPDATE", other RESTFUL commands
    response = requests.get(url, stream=True)
    # Check the response status after the request
    if response.status_code == requests.codes.ok:
        #print (response.headers)
        filesize = 0
        # Check the total length of the file to donwload
        if 'Content-Length' in response.headers:
            filesize = int(response.headers['Content-Length'])
        else:
            filesize = len(response.content)

        # Check first if a name is given in the condition
        if filename is not None:
            local_filename = filename
        else:
            # Try to get the name of the file directly from the request
            local_filename = get_filename_from_header(response.headers)
            # If not name is given in the request then try to inference from the url
            if local_filename is None:
                # Get the name of the file using the URL
                local_filename = url.split('/')[-1].split("#")[0].split("?")[0]

        # get full path of the file
        if filepath is not None:
            local_filename = filepath + "/" + local_filename
        # Open the file in write mode
        with open(local_filename, 'wb') as file:
            # Check if the reponse must be stored in raw data or using the decoding
            # type inside content-type
            if rawdata:
                # Copy directly the content of the buffer in the response to the file
                shutil.copyfileobj(response.raw, file)
            else:
                with ProgressBar(filesize) as pbar:
                    # Get the decoded data using the headers content type.
                    # Lets requests/urllib do the conversion ('Content-Encoding')
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:  # filter out keep-alive new chunks
                            file.write(chunk)
                            pbar.update(chunk_size)
        # Finall return the file name is succesful
        return local_filename
    # Anyways return None
    return None
    