import requests
import shutil

def download(url, opath = None):
    """
        Download a file from the current URL by doing an http request via GET.
        Returns the name of the file downloaded if succesful.
        None is there was an error in the conexion or donwloading the file.
    """
    # get the name of the file
    if opath is None:
        local_filename = url.split('/')[-1]
    else:
        local_filename = opath + "/" + url.split('/')[-1]
    # Do the GET request to the url passed by commands
    #   request.request("GET",url)
    r = requests.get(url, stream=True)
    # Check the response status after the request
    if r.status_code == requests.codes.ok:
        # Open the file in write mode
        with open(local_filename, 'wb') as f:
            # Copu the content of the buffer in the response to the file
            shutil.copyfileobj(r.raw, f)
        # Finall return the file name is succesful
        return local_filename
    else:
        return None
    