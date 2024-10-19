import math
import config


def compute_airdist(point1, point2):
    a = (math.sin(math.radians(point1.lat - point2.lat) / 2) ** 2
         + math.cos(math.radians(point1.lat))
         * math.cos(math.radians(point2.lat))
         * (math.sin(math.radians(point1.lon - point2.lon) / 2)
            ** 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = config.earth_radius * c
    return d


def compute_travel_time(instance, point1, point2):
    return compute_airdist(point1, point2)/instance.parameters.lineEditTravelSpeed


def compute_airdist_with_lat_lon(lat1, lon1, lat2, lon2):
    a = (math.sin(math.radians(lat1 - lat2) / 2) ** 2
         + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2))
         * (math.sin(math.radians(lon1 - lon2) / 2)
            ** 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = config.earth_radius * c
    return d
