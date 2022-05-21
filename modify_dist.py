import gpxpy.gpx
import datetime
from geopy.distance import distance
import copy
import math


def gpx_distance(segment_points, start=0):
    last = None
    tot_dist = 0
    for point in segment_points[start:]:
        if last is not None:
            d = distance((point.latitude, point.longitude), (last.latitude, last.longitude)).m
            tot_dist += d
        last = point
    return tot_dist


def run(activity_gpx, target_dist, target_time):

    gpx = activity_gpx

    d = 0
    end = False
    segment = gpx.tracks[0].segments[0]
    ori_d = gpx_distance(segment.points)
    new_segment = copy.deepcopy(segment)
    segment_points = copy.deepcopy(segment.points)
    # modify distance
    while not end:
        segment_points.reverse()
        for i in range(1, len(segment_points)-1):
            new_segment.points.append(segment_points[i])
            d += gpx_distance(new_segment.points, len(new_segment.points)-2)
            if d >= target_dist:
                end = True
                break

    # modify time
    segment_points = copy.deepcopy(segment.points)
    added_points = len(new_segment.points) - len(segment.points)
    time = segment_points[-1].time
    print(time)
    delta = target_time / added_points
    delta_m = (delta * 1000) % 1000
    delta_s = math.floor((delta))
    delta_t = datetime.timedelta(seconds=delta_s, milliseconds=delta_m)
    for i in range(len(segment_points), len(new_segment.points)):
        time += delta_t
        new_segment.points[i].time = time
    print((segment_points[-1].time - segment_points[0].time).total_seconds()/60)
    print((time - segment_points[-1].time).total_seconds()/60)
    print((time - segment_points[0].time).total_seconds()/60)

    final_dist = d + ori_d
    print('Final distance:', final_dist)
    print('Added GPS points:', added_points)
    print('Final time:', time)

    ret_data = {'add_p': added_points, 'final_d': final_dist,
                'init_d': ori_d}

    gpx.tracks[0].segments[0] = new_segment

    gpx_xml = gpx.to_xml()
    return gpx_xml, ret_data


if __name__ == '__main__':
    activity_gpx = 'gpx/summer_palace.gpx'
    gpx_file = open(activity_gpx, 'r')
    gpx = gpxpy.parse(gpx_file)
    activity_name = activity_gpx.split('.')[0] + '_modify.gpx'
    gpx_xml, data = run(gpx, 6000, 24*60+12)
    with open(activity_name, 'w') as f:
        f.write(gpx_xml)
    print('Created {}'.format(activity_name))
