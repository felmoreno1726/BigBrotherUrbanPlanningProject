import hashlib
import hmac
import base64
import urllib.parse as urlparse
import googlemaps
from datetime import datetime
import numpy as np
import google_streetview.api
import google_streetview.helpers
import generate_circle_linspace
# Function to generate the points in between
from generate_circle_linspace import latt_long_linspace

# Define API keys and signed URL
api_key = "YOURAPIKEYS"

# Return URL array for the images
def get_url(_points):
    # Define parameters for street view api
    _param = {
        'size': '640x640', # max 640x640 pixels
        'location': '', # lattitude and longitude for the location
        'key': api_key, # api key
        'heading': '' # indicates the compass heading, 0 for North, 90 for East
    }
    # Heading to create a 360 view
    _headings = [0, 90, 180, 270]
    # Empty list for parameters
    _params_list, _urls_list = [], []
    # Obtain the points into the parameters
    for _point in _points:
        _latt_long = '{},{}'.format(_point[0], _point[1])
        # Assign the location to the list of dict in parameters
        _param['location'] = _latt_long
        # Loop through the headings
        for _h in _headings:
            _param['heading'] = str(_h)
            # Append to the list of params
            _params_list.append(_param.copy())
    # Obtain the URL list
    _urls_list = google_streetview.api.results(_params_list).links

    return _urls_list

# Get the number of points from Google
def get_url_from_points(_start_point, _end_point, _N_points=10):
    # Allocate the Google API key
    _gmaps = googlemaps.Client(key=api_key)
    # Generate a bunch of data points
    _test_points = latt_long_linspace(_start_point, _end_point, _N_points)
    # Snapped points onto Google's Maps street
    _snapped_points = _gmaps.snap_to_roads(_test_points)
    # Collect them into a list of just longitude and latitude
    _result_points = []
    for _points in _snapped_points:
        _result_points.append((_points['location']['latitude'],
                               _points['location']['longitude']))
    return get_url(_result_points)

if __name__ == "__main__":
    # Generate a bunch of data points
    start = (42.348933, -71.097594)
    end = (42.352140, -71.123463)
    # Number of points in the middle
    N = 1
    # Return the URL
    image_urls = get_url_from_points(start, end, N)
    print(image_urls)
