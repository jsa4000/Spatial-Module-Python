========================
 NOTES
 =======================

The idea is to develop a tool that will generate some geometry and spatial data by using some API availabile to download real data from the Earth.

DEFINITIONS
========================

**Geographic Information System (GIS)** is a system designed to capture, store, manipulate, analyze, manage, and present spatial or geographic data. The acronym GIS is sometimes used for geographic information science (GIScience) to refer to the academic discipline that studies geographic information systems and is a large domain within the broader academic discipline of geoinformatics. What goes beyond a GIS is a spatial data infrastructure, a concept that has no such restrictive boundaries

**Digital Elevation Model (DEM)** is a digital model or 3D representation of a terrain's surface — commonly for a planet (including Earth), moon, or asteroid — created from terrain elevation data.


**Nominatim** is a geocoder and reverse-geocoder. You can search for an address and it will return the location. Likewise you can search for a location and it will return its full address hierarchy. Nominatim usually only returns address-related tags from OSM.

**Overpass API** instead can query for all tags in OSM. You can search for POIs, parking spaces, roads, rivers, speed cameras, traffic lights, ... However it just allows you to search for raw tags. It doesn't know about addresses (except for the raw address tags in OSM), especially it lacks the knowledge of address hierarchies.


Sources
========================

1. Open Street Map

Open Street Map it's a Free service to retrieve GIS data based on the information shared by the people. This means this is a social-community-based resource that will depended on the informaion upload/updated by the people.

1.1. Overpass API. This servide allows to download datasets by specifiing some parameters. The way that it works it by using querys to send the parameters.

1.1.1 Functionality

> http://wiki.openstreetmap.org/wiki/Overpass_API

The way it works it's based on queries. Here are some exmples

- Overpass QL

    (
        node(51.249,7.148,51.251,7.152);
        <;
    );
    out meta;

- Overpass XML:

    <union>
        <bbox-query s="51.249" w="7.148" n="51.251" e="7.152"/>
        <recurse type="up"/>
    </union>
    <print mode="meta"/>

- Complex Query:

    <bbox-query s="51.15" n="51.35" w="7.0" e="7.3"/>
    <recurse type="node-way"/>
    <query type="way">
        <item/>
        <has-kv k="highway" v="motorway"/>
    </query>
    <print/>

1.1.2 Extensions

- Metro Extracts

Much of the time when we’re working with OpenStreetMap data, we’re only focusing on a single city. If that’s the case for you, you’re in luck: you can use MapZen’s convenient Metro Extracts service to download all the city’s OpenStreetMap data in one convenient zip file.

- GeoPandas

 GeoPandas is an extension of Pandas that integrates a bunch of other Python geo libraries: **fiona** for input/output of a bunch of different geo file formats, **shapely** for geodata manipulation, and **descartes** for generating matplotlib plots, all in the familiar Pandas interface.

> An example of ifs usage can be seen in the following link:
>    https://michelleful.github.io/code-blog/2015/04/27/osm-data/

- geopandas_osm

A GeoPandas interface to query OpenStreetMap Overpass API

1.2. GET/POST Api. This method will retrieve the data for the speci a location by a bbox and it download all the data inside that area. This way, it doesn't allow to specify the type of data to download: highways, roads, etc...

    http://api.openstreetmap.org/api/0.6/map?bbox=11.54,48.14,11.543,48.145

where:
- bbox: left, bottom, right, top

>The API is limited to bounding boxes of about 0.5 degree by 0.5 degree and you should avoid using it if possible. For larger areas you might try to use XAPI, for example: 
>   http://overpass.osm.rambler.ru/cgi/xapi_meta?*[bbox=11.5,48.1,11.6,48.2]

1.3 Tile Maps. This option allows to donwload raster tiles from Open Street Maps. Due some policy terms this is not allowed ecause of legal termns and servers overloads. To see all the tiles available to download you can refer to the following URL:

> http://wiki.openstreetmap.org/wiki/Tiles

>Here are an example of its usage:
>   http://michal.rawlik.pl/2013/03/19/openstreetmap-maps-in-python/

You can also download the tiles from the current URL:
    https://openmaptiles.com/downloads/

2. Open Topography

This source is intended to get an image with the elevation data by specifing a bbox with the area to recover.
Also, it allows to specify the level of detail, image type and different types of data to retrieve suh as: `SRTMGL3`, `SRTMGL1`, `AW3D30` or `SRTMGL1_`.

>http://www.opentopography.org/developers#GMRT

The url to retreieve the elevation is the following (POST):

    http://opentopo.sdsc.edu/otr/getdem?demtype=SRTMGL3&west=-120&south=34&east=-119&north=35&outputFormat=GTiff

Where:
- demtype:	The global raster dataset: SRTM GL3 (90m) is 'SRTMGL3', SRTM GL1 (30m) is 'SRTMGL1', SRTM GL1 (Ellipsoidal) is 'SRTMGL1_E', and ALOS World 3D 30m is 'AW3D30'
- west, south, east, north: WGS 84 bounding box coordinates
- outputFormat: outputFormat Output Format (optional) - GTiff for GeoTiff, AAIGrid for Arc ASCII Grid, HFA for Erdas Imagine (.IMG). Defaults to GTiff if parameter is not provided

> For GET capabilities
> http://opentopo.sdsc.edu/geoportal/csw/discovery?Request=GetCapabilities&Service=CSW&Version=2.0.2

3. Google Maps/Earth


4 . Other Resources:

- http://wiki.openstreetmap.org/wiki/TMS
- https://pypi.python.org/pypi/elevation