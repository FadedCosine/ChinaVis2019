# -*- coding: UTF-8 -*-

import os
import math
import numpy as np

EARTH_REDIUS = 6378.137
PI_x = 3.14159265358979324 * 3000.0 / 180.0
center_pos = (104.041, 30.466)
center_radius = 1.6
area_interval = center_radius * center_radius # 1.5 * 1.5 每个圆或环面积为 PI * 1.5 * 1.5


start_unix_time = 1525104000 # 2018-5-1 00:00:00
end_unix_time = 1525190399 # 2018-5-1 23:59:59  左闭右闭
t_interval = 60 * 5
interval_num = int((end_unix_time-start_unix_time) / t_interval) + 1


if t_interval < 60 * 60:
	tsv_suffix = "_" + str(int(t_interval/60)) + "minutes" + "_radius_" + str(center_radius) + ".tsv"
	npy_suffix = "_" + str(int(t_interval/60)) + "minutes" + "_radius_" + str(center_radius) + ".npy"
else:
	tsv_suffix = "_" + str(int(t_interval/3600)) + "hour" + "_radius_" + str(center_radius) + ".tsv"
	npy_suffix = "_" + str(int(t_interval/3600)) + "hour" + "_radius_" + str(center_radius) + ".npy"

distance_classify_list = []

road = set()

def rad(d):
    return d * math.pi / 180.0

def getDistance(lng1, lat1, lng2, lat2) -> float:
    radLat1 = rad(lat1)
    radLat2 = rad(lat2)
    a = radLat1 - radLat2
    b = rad(lng1) - rad(lng2)
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2), 2) + math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b/2), 2)))
    s = s * EARTH_REDIUS
    return s

def distance_classify():
	if os.path.exists("distance_classify_list" + npy_suffix):
		global distance_classify_list
		print("distance_classify_list" + npy_suffix + " already exists, we can just load it!")
		print("Loading ...", end = "")
		raw_file = np.load("distance_classify_list" + npy_suffix)
		global distance_classify_list
		distance_classify_list = raw_file.tolist()
		print("\nLoad distance_classify_list" + npy_suffix + " successfully")
		return
	for i in range(interval_num):
		distance_classify_list.append({})
	print("Begin to load bd09_data_tuple.npy")
	print("Loading ...", end = "")
	raw_file = np.load("bd09_data_tuple.npy")
	order_list = raw_file.tolist()
	print("\nLoad bd09_data_tuple.npy successfully")
	distance_dict = dict()
	for order in order_list:
		distance_dict.clear()
		for item in order:
			time = item[0]
			pos = item[1]
			dist = getDistance(pos[0], pos[1], center_pos[0], center_pos[1])
			time_index = int((time - start_unix_time) / t_interval)
			dist_index = int(dist * dist / area_interval)
			if dist_index not in distance_dict:
				distance_dict[dist_index] = set()
			distance_dict[dist_index].add(time_index)
			break
		for dist_index in distance_dict.keys():
			time_list = list(distance_dict[dist_index])
			for time_index in time_list:
				if dist_index not in distance_classify_list[time_index]:
					distance_classify_list[time_index][dist_index] = 0
				distance_classify_list[time_index][dist_index] += 1
	np.save("distance_classify_list" + npy_suffix, distance_classify_list)

def output_to_file(output_filename):
	csv_filename = output_filename[:-3] + 'csv'

	print('Begin to output to ' + csv_filename)
	interval = ','
	distance_classify_file = open(csv_filename, 'w', encoding='utf-8')
	distance_classify_file.write("date");
	road_list = list(road)
	max_dist_index = 0
	for distance_item in distance_classify_list:
		max_dist_tmp = max(distance_item.keys())
		if max_dist_index < max_dist_tmp:
			max_dist_index = max_dist_tmp
	for dist_index in range(max_dist_index):
		distance_classify_file.write(interval + str(dist_index))
	for idx, distance_item in enumerate(distance_classify_list):
		distance_classify_file.write('\n')
		distance_classify_file.write(str(start_unix_time+t_interval*idx))
		line_sum = 0
		for dist_index in range(max_dist_index):
			if dist_index in distance_item:
				line_sum += distance_item[dist_index]
		for dist_index in range(max_dist_index):
			if dist_index in distance_item:
				distance_classify_file.write(interval + "%.2f%%"%(distance_item[dist_index]/line_sum * 100))
			else:
				distance_classify_file.write(interval + '0')
	distance_classify_file.close()
	print("Output to " + csv_filename + " successfully")

distance_classify()
output_to_file("distance_classify" + tsv_suffix)




