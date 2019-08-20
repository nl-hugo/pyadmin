import json
import logging

import requests
from geopy.geocoders import Nominatim

BASE_URL = 'http://router.project-osrm.org/route/v1/driving/'

logger = logging.getLogger(__name__)


def get_driving_distance(origin, destination):
    """Returns the driving distance between origin and destination 
    coordinates using the OSMR backend.

    See: 
    https://github.com/Project-OSRM/osrm-backend/blob/master/docs/http.md
    """
    distance = 0
    return_code = message = None

    try:
        url = '{}{},{};{},{}?overview=false'.format(BASE_URL,
                                                    origin.longitude, origin.latitude, destination.longitude,
                                                    destination.latitude)
        logger.info('GET {}'.format(url))

        r = requests.get(url)
        return_code = r.status_code
        if r.status_code == requests.codes.ok:
            route = json.loads(r.text)['routes'][0]
            distance = route['distance'] / 1000  # to km
        else:
            r.raise_for_status()
    except AttributeError as e:
        logger.error('Invalid location')
    except Exception as e:
        logger.error(e)  # 429 = too many requests
        message = e

    logger.info('Distance {}'.format(distance))

    return round(distance, 0), return_code, message


def geo_code(zip_code):
    """Returns geocoded location for the zip code. 

    See: https://geopy.readthedocs.io/en/stable/#
    """
    geolocator = Nominatim(user_agent='driving-distance/1')
    return geolocator.geocode(zip_code, country_codes='NL')
