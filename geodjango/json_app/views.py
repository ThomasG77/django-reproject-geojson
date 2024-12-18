# from django.shortcuts import render
from pyproj import CRS, Transformer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from urllib.request import urlopen

# Open the URL that contains JSON
"""
response = urlopen('https://jsonplaceholder.typicode.com/posts')

if response.getcode() == 200:
    # Parse JSON in Python
    data = json.loads(response.read().decode('utf-8'))
    # Print the title of each post
    for post in data:
        print(post['title'])
else:
    print('Error fetching data')
"""

def geometryPoint(entry, transformer):
    return transformer.transform(*entry)
def geometryLineString(entry, transformer):
    return [transformer.transform(*coord) for coord in entry]
def geometryPolygon(entry, transformer):
    return [[transformer.transform(*coord) for coord in part] for part in entry]
geometryMultiPoint = geometryLineString
geometryMultiLineString = geometryPolygon
def geometryMultiPolygon(entry, transformer):
    return [[[transformer.transform(*coord) for coord in part] for part in multipart] for multipart in entry]

transform_geojson_geom = [
    geometryPoint,
    geometryLineString,
    geometryPolygon,
    geometryMultiPoint,
    geometryMultiLineString,
    geometryMultiPolygon
]

convert_info = dict(zip(['Point', 'LineString', 'Polygon', 'MultiPoint', 'MultiLineString', 'MultiPolygon'], transform_geojson_geom))

def convert_remote_geojson(url):
    try:
        response = urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        if data.get('crs') is not None:
            crs_urn = data.get('crs').get('properties').get('name')
            crs_origin = CRS.from_string(crs_urn)
        if crs_origin.to_epsg() != 4326:
            transformer = Transformer.from_crs(crs_origin, 4326, always_xy=True)
            return {
                "type": "FeatureCollection",
                "features": [{
                    'type': feature.get('type'),
                    'properties': feature.get('properties'),
                    'geometry': {
                        'type': feature.get('geometry').get('type'),
                        'coordinates': convert_info[feature.get('geometry').get('type')](feature.get('geometry').get('coordinates'), transformer)
                    }
                } for feature in data.get('features')]
            }
        else:
            return data
    except json.JSONDecodeError:
        return {
            'status': 'error',
            'message': 'Invalid JSON data'
        }

@csrf_exempt
def json_handler(request):
    if request.method == 'GET':
        url = request.GET.get('url', None)
        if url is not None:
            response = convert_remote_geojson(url)
    else:
        response = {
            'status': 'error',
            'message': 'Only GET requests are allowed'
        }
    return JsonResponse(response)

# Create your views here.

point = {
    "type": "Point",
    "coordinates": [100.0, 0.0]
}
line = {
    "type": "LineString",
    "coordinates": [
        [100.0, 0.0],
        [101.0, 1.0]
    ]
}
poly_simple = {
    "type": "Polygon",
    "coordinates": [
        [
            [100.0, 0.0],
            [101.0, 0.0],
            [101.0, 1.0],
            [100.0, 1.0],
            [100.0, 0.0]
        ]
    ]
}

poly_hole = {
    "type": "Polygon",
    "coordinates": [
        [
            [100.0, 0.0],
            [101.0, 0.0],
            [101.0, 1.0],
            [100.0, 1.0],
            [100.0, 0.0]
        ],
        [
            [100.8, 0.8],
            [100.8, 0.2],
            [100.2, 0.2],
            [100.2, 0.8],
            [100.8, 0.8]
        ]
    ]
}

multipoint = {
    "type": "MultiPoint",
    "coordinates": [
        [100.0, 0.0],
        [101.0, 1.0]
    ]
}

multiline = {
    "type": "MultiLineString",
    "coordinates": [
        [
            [100.0, 0.0],
            [101.0, 1.0]
        ],
        [
            [102.0, 2.0],
            [103.0, 3.0]
        ]
    ]
}

multipoly = {
    "type": "MultiPolygon",
    "coordinates": [
        [
            [
                [102.0, 2.0],
                [103.0, 2.0],
                [103.0, 3.0],
                [102.0, 3.0],
                [102.0, 2.0]
            ]
        ],
        [
            [
                [100.0, 0.0],
                [101.0, 0.0],
                [101.0, 1.0],
                [100.0, 1.0],
                [100.0, 0.0]
            ],
            [
                [100.2, 0.2],
                [100.2, 0.8],
                [100.8, 0.8],
                [100.8, 0.2],
                [100.2, 0.2]
            ]
        ]
    ]
}
