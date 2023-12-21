"""Functions for getting maps to embed for Flask Cafe app."""
import os
from dotenv import load_dotenv
load_dotenv()
# Found resource to create URL from key/val dict here:
# https://stackoverflow.com/questions/15799696/how-to-build-urls-in-python-with-the-standard-library
# https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlencode
from urllib.parse import urlencode

GMAPS_API_KEY = os.environ['GMAPS_API_KEY']
GMAPS_BASE_API_URL = "https://www.google.com/maps/embed/v1/"


def get_map_url(address):
    """Get Google Maps URL to embed a map for this location."""

    params = urlencode({'key': GMAPS_API_KEY, 'q': address})
    url = f"{GMAPS_BASE_API_URL}place?{params}"
    # print('url: ', url)
    return url
