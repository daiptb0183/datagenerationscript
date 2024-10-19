import numpy as np
import matplotlib.pyplot as plt
import string
import data_generation
import gaussian_kernel
import os


def create_zones(instance):

    matrix_size = instance.parameters.lineEditMatrixSize

    min_lat, min_lon, max_lat, max_lon = data_generation.get_bounding_box(
        [instance.parameters.lineEditDepotLat,
            instance.parameters.lineEditDepotLon],
        instance.parameters.lineEditServiceArea)

    instance.min_lat = min_lat
    instance.min_lon = min_lon
    instance.max_lat = max_lat
    instance.max_lon = max_lon

    lat_interval_size = (max_lat - min_lat)/(matrix_size)
    arr_start_lat = np.arange(
        min_lat, max_lat, lat_interval_size)

    lon_interval_size = (max_lon - min_lon)/(matrix_size)
    arr_start_lon = np.arange(
        min_lon, max_lon, lon_interval_size)

    zone_numbers = np.arange(matrix_size-1, -1, -1)
    zone_letters = list(string.ascii_uppercase)[0:matrix_size]

    if instance.parameters.comboBoxZoneStyle == '3 Clusters':
        center1 = (int((matrix_size)/4),
                   int((matrix_size)/4))

        center2 = (int((matrix_size*3)/4),
                   int((matrix_size)/4))

        center3 = (int((matrix_size)/2),
                   int((matrix_size*3)/4))

        centers_list = [center1, center2, center3]

    elif instance.parameters.comboBoxZoneStyle == 'Center':
        center1 = (int((matrix_size)/2),
                   int((matrix_size)/2))
        centers_list = [center1]

    else:
        center1 = (int((matrix_size)/4),
                   int((matrix_size)/4))

        center2 = (int((matrix_size*3)/4),
                   int((matrix_size)/4))

        centers_list = [center1, center2]

    kernels_list = []
    for center in centers_list:
        kernel = gaussian_kernel.gaussian_heatmap(
            center=center, image_size=(matrix_size, matrix_size),
            sig=(4-instance.parameters.horizontalSliderZoneDivergingLevel))
        kernels_list.append(kernel)

    probabilities = sum(kernels_list)

    normalization_factor = np.sum(
        probabilities)/instance.parameters.lineEditNumberOfRequests
    probabilities = probabilities/normalization_factor
    probabilities = probabilities.round(2)

    zones_list = []
    for i, number in enumerate(zone_numbers):
        for j, letter in enumerate(zone_letters):
            current_zone = Zone([number, letter],
                                arr_start_lat[j],
                                arr_start_lat[j] + lat_interval_size,
                                arr_start_lon[matrix_size - 1 - i],
                                arr_start_lon[matrix_size - 1 - i] +
                                lon_interval_size,
                                probabilities[i, j])
            zones_list.append(current_zone)
    fig, ax = plt.subplots()
    im = ax.imshow(probabilities)
    fig.colorbar(im, orientation='vertical')


    ax.set_xticks(np.arange(len(zone_letters)))
    ax.set_yticks(np.arange(len(zone_numbers)))

    ax.set_xticklabels(zone_letters)
    ax.set_yticklabels(zone_numbers)

    plt.setp(ax.get_xticklabels(), ha="center")

    ax.set_title("Zone and Request Probability Heatmap")
    fig.tight_layout()
    try:
        filename = 'output_picture/instance_' + instance.test_utc_start_time+'/seed_'+ str(instance.parameters.spinBoxSeed) + '/heatmap'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        plt.savefig(filename)
    except AttributeError:
        plt.savefig('output_picture/heatmap')
    return zones_list


class Zone(object):
    zone_name = list
    zone_start_lat = float
    zone_end_lat = float
    zone_start_lon = float
    zone_end_lon = float
    zone_probability = float

    def __init__(self, zone_name, zone_start_lat, zone_end_lat,
                 zone_start_lon, zone_end_lon, zone_probability):
        self.zone_name = zone_name
        self.zone_start_lat = zone_start_lat
        self.zone_end_lat = zone_end_lat
        self.zone_start_lon = zone_start_lon
        self.zone_end_lon = zone_end_lon
        self.zone_probability = zone_probability

    def __repr__(self):
        return str(self.zone_name)
