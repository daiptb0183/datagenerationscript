import random
import uuid
from entity import entities
import geopy.distance
import heatmap


def generate_random_test_instance_by_zone(number_of_periods, random_generator, instance):
    requests = []
    try:
        zones_list = instance.zones_list
    except AttributeError:
        zones_list = heatmap.create_zones(instance)
        instance.zones_list = zones_list

    for i in range(number_of_periods):
        period_requests = generate_random_requests_from_zone(
            zones_list, i, instance)
        requests += period_requests

    for request in requests:
        request.randomize_part(random_generator)
    return requests


def generate_requests_normal_spatial_distribution(number_of_periods,
                                                  random_generator, instance):

    requests = []
    instance.min_lat, instance.min_lon, instance.max_lat, instance.max_lon \
        = get_bounding_box(
            [instance.parameters.lineEditDepotLat,
             instance.parameters.lineEditDepotLon],
            instance.parameters.lineEditServiceArea)

    get_cluster_centers_list(instance)

    for i in range(number_of_periods):
        period_requests = generate_period_requests_sptial_distribution(
            random_generator, i, instance)
        requests += period_requests

    for request in requests:
        request.randomize_part(random_generator)
    return requests


def get_cluster_centers_list(instance):
    if instance.parameters.comboBoxZoneStyle == '2 Clusters':
        instance.cluster_centers_list = [(instance.min_lat + (instance.max_lat-instance.min_lat)*(1/5), instance.min_lon + (instance.max_lon-instance.min_lon)*(4/5)),
                                         (instance.min_lat + (instance.max_lat-instance.min_lat)*(4/5), instance.min_lon + (instance.max_lon-instance.min_lon)*(4/5))]
    elif instance.parameters.comboBoxZoneStyle == '3 Clusters':
        instance.cluster_centers_list = [(instance.min_lat + (instance.max_lat-instance.min_lat)*(1/5), instance.min_lon + (instance.max_lon-instance.min_lon)*(4/5)),
                                         (instance.min_lat + (instance.max_lat-instance.min_lat)*(
                                             4/5), instance.min_lon + (instance.max_lon-instance.min_lon)*(4/5)),
                                         (instance.min_lat + (instance.max_lat-instance.min_lat)*(1/2), instance.min_lon + (instance.max_lon-instance.min_lon)*(1/5))]
    elif instance.parameters.comboBoxZoneStyle == 'Center':
        instance.cluster_centers_list = [(instance.min_lat + (instance.max_lat-instance.min_lat)*(
            1/2), instance.min_lon + (instance.max_lon-instance.min_lon)*(1/2))]


def generate_period_requests_sptial_distribution(random_generator, period, instance, unbalanced=False):
    requests_list = []
    number_of_request = random_generator.poisson(
        instance.parameters.lineEditNumberOfRequests)

    standard_deviation_lat_1km = (
        instance.max_lat - instance.min_lat)/((instance.parameters.lineEditServiceArea)*2)
    standard_deviation_lon_1km = (
        instance.max_lon - instance.min_lon)/((instance.parameters.lineEditServiceArea)*2)

    for i in range(number_of_request):
        request_uuid = uuid.uuid4()
        if unbalanced:
            if instance.parameters.comboBoxZoneStyle == '2 Clusters':
                p = [0.66, 1-0.66]
            elif instance.parameters.comboBoxZoneStyle == '3 Clusters':
                p = [0.25, 0.25, 0.5]
            else:
                p = [1]
        else:
            p = [1/len(instance.cluster_centers_list)
                 for i in range(len(instance.cluster_centers_list))]

        selected_center = instance.cluster_centers_list[random_generator.choice(
            list(range(len(instance.cluster_centers_list))), p=p)]
        if instance.parameters.comboBoxZoneStyle != 'Center':
            lat = random_generator.normal(
                selected_center[0], standard_deviation_lat_1km*1)
            lon = random_generator.normal(
                selected_center[1], standard_deviation_lon_1km*1)
        else:
            lat = random_generator.normal(
                selected_center[0], standard_deviation_lat_1km*4)
            lon = random_generator.normal(
                selected_center[1], standard_deviation_lon_1km*4)
        request = entities.Request(str(period)+"_"+str(i),
                                   request_uuid,
                                   entities.Location(lat, lon),
                                   period,
                                   instance.possible_parts,
                                   instance.possible_parts_probability,
                                   None)
        requests_list.append(request)
    return requests_list


def generate_random_requests_from_zone(zones_list, period, instance):
    requests_list = []
    i = 0
    for zone in zones_list:
        random_number = random.random()
        if random_number <= zone.zone_probability:
            request_uuid = uuid.uuid4()
            lat = random.uniform(zone.zone_start_lat, zone.zone_end_lat)
            lon = random.uniform(zone.zone_start_lon, zone.zone_end_lon)
            request = entities.Request(str(period)+"_"+str(i),
                                       request_uuid,
                                       entities.Location(lat, lon),
                                       period,
                                       instance.possible_parts,
                                       instance.possible_parts_probability,
                                       zone)
            """ request.neighouring_zones = get_neighouring_zones(
                zones_list, request) """
            requests_list.append(request)
            i += 1
    return requests_list


def get_neighouring_zones(zones_list, request):
    neighouring_zones = []
    request_coordinates = [
        request.zone.zone_start_lat, request.zone.zone_end_lat,
        request.zone.zone_start_lon, request.zone.zone_end_lon]
    for zone in zones_list:
        zone_coordinate = [
            zone.zone_start_lat, zone.zone_end_lat,
            zone.zone_start_lon, zone.zone_end_lon]
        number_of_intersections = len(
            set(request_coordinates).intersection(zone_coordinate))
        if number_of_intersections >= 3:
            neighouring_zones.append(zone)
        elif (request.zone.zone_end_lon == zone.zone_start_lon and
              request.zone.zone_start_lat == zone.zone_end_lat) or \
            (request.zone.zone_end_lat == zone.zone_start_lat and
             request.zone.zone_end_lon == zone.zone_start_lon) or \
            (request.zone.zone_end_lat == zone.zone_start_lat and
             request.zone.zone_start_lon == zone.zone_end_lon) or \
            (request.zone.zone_start_lat == zone.zone_end_lat and
             request.zone.zone_start_lon == zone.zone_end_lon):
            neighouring_zones.append(zone)
    return list(set(neighouring_zones))


def get_nearby_point(origin, radius):
    dist = geopy.distance.distance(kilometers=random.uniform(0, radius))
    pt = dist.destination(point=geopy.Point(
        (origin[0], origin[1])), bearing=random.random()*360)
    return pt[0], pt[1]


def get_bounding_box(depot_location, radius):
    dist = geopy.distance.distance(kilometers=radius)
    top_pt = dist.destination(point=geopy.Point(
        (depot_location[0], depot_location[1])), bearing=0)
    right_pt = dist.destination(point=geopy.Point(
        (depot_location[0], depot_location[1])), bearing=90)
    bottom_pt = dist.destination(point=geopy.Point(
        (depot_location[0], depot_location[1])), bearing=180)
    left_pt = dist.destination(point=geopy.Point(
        (depot_location[0], depot_location[1])), bearing=270)

    min_lat = min([p.latitude for p in [top_pt, right_pt, bottom_pt, left_pt]])
    min_lon = min(
        [p.longitude for p in [top_pt, right_pt, bottom_pt, left_pt]])

    max_lat = max([p.latitude for p in [top_pt, right_pt, bottom_pt, left_pt]])
    max_lon = max(
        [p.longitude for p in [top_pt, right_pt, bottom_pt, left_pt]])

    return min_lat, min_lon, max_lat, max_lon
