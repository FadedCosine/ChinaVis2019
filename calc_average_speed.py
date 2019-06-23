# -*- coding: UTF-8 -*-
import math
import json
import numpy as np
import os
import gc

EARTH_REDIUS = 6378.137
accuracy = 4 # 经纬度精确到小数点后 3 位
t_interval = 60 * 1 # 数据间隔30分钟
PI_x = 3.14159265358979324 * 3000.0 / 180.0
start_unix_time = 1525104000 # 2018-5-1 00:00:00
end_unix_time = 1525190399 # 2018-5-1 23:59:59  左闭右闭
interval_num = int((end_unix_time-start_unix_time) / t_interval) + 1

if t_interval < 60 * 60:
	tsv_suffix = "_" + str(int(t_interval/60)) + "minute.tsv"
	npy_suffix = "_" + str(int(t_interval/60)) + "minute.npy"
else:
	tsv_suffix = "_" + str(int(t_interval/3600)) + "hour.tsv"
	npy_suffix = "_" + str(int(t_interval/3600)) + "hour.npy"

pos_speed_list = []
average_speed = []

road = set()

def rad(d):
    return d * math.pi / 180.0

def getDistance(lng1, lat1, lng2, lat2):
    radLat1 = rad(lat1)
    radLat2 = rad(lat2)
    a = radLat1 - radLat2
    b = rad(lng1) - rad(lng2)
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2), 2) + math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b/2), 2)))
    s = s * EARTH_REDIUS
    return s

def calc_pos_speed_bd09():
	if os.path.exists("average_speed" + npy_suffix) and os.path.exists("road.npy"):
		return
	print("average_speed" + npy_suffix + " does not exist, we need to calculate pos_speed_list first")
	print("Begin to calculate pos_speed_list")
	global pos_speed_list
	if os.path.exists("pos_speed_list" + npy_suffix):
		print("pos_speed_list.npy already exists, we can just load it!")
		print("Loading ...", end = "")
		raw_file = np.load("pos_speed_list" + npy_suffix)
		pos_speed_list = raw_file.tolist()
		print("\nLoad pos_speed_list" + npy_suffix + " successfully")
		return
	print("Begin to load bd09_data_tuple.npy")
	print("Loading ...", end = "")
	order_list = (np.load('bd09_data_tuple.npy')).tolist()
	print("\nLoad bd09_data_tuple.npy successfully")
	pos_speed_index = []
	for i in range(interval_num):
		pos_speed_list.append([])
		pos_speed_index.append(0)
	right_count, error_count = 0, 0
	for order_idx, order in enumerate(order_list):
		for idx, item in enumerate(order):
			if idx == 0:
				cur_pos = item[1]
				cur_time = item[0]
				continue
			last_pos = cur_pos
			last_time = cur_time
			cur_pos = item[1]
			cur_time = item[0]
			average = getDistance(cur_pos[0], cur_pos[1], last_pos[0], last_pos[1]) * 3600 / (cur_time - last_time)
			if (average > 200):
				error_count += 1
				print("\rError Rate: %d/%d  Speed is to large! it's %f"%(error_count, error_count + right_count, average), end = "")
				continue
			else:
				right_count += 1
			point_index = int((cur_time - start_unix_time) / t_interval)
			pos_speed_list[point_index].append([])
			pos_speed_list[point_index][pos_speed_index[point_index]].append(item[1])
			pos_speed_list[point_index][pos_speed_index[point_index]].append(average)
			pos_speed_index[point_index] += 1
		order_list[order_idx] = []
	gc.collect()
	print("\nFinished calculate pos_speed_list")
	print("Begin to save pos_speed_list")
	np.save("pos_speed_list" + npy_suffix, pos_speed_list)
	print("Save pos_speed_list into pos_speed_list" + npy_suffix + " successfully")

def calc_average_speed_bd09():
	print("Begin to calculate average_speed")
	if os.path.exists("average_speed" + npy_suffix):
		print("average_speed" + npy_suffix + " already exists, we can just load it!")
		print("Loading ...", end = "")
		raw_file = np.load("average_speed" + npy_suffix)
		global average_speed
		average_speed = raw_file.tolist()
		print("\nLoad average_speed" + npy_suffix + " successfully")
		road_file = np.load("road.npy")
		global road
		road = set(road_file.tolist())
		return
	global pos_speed_list
	average_speed_list = []
	print("Begin to load address_dict.npy")
	print("Loading ...", end = "")
	address_dict = (np.load("address_dict.npy")).item()
	print("\nLoad address_dict.npy successfully")
	for i in range(interval_num):
		average_speed_list.append({})
		average_speed.append({})
	right_count, error_count, not_in_road = 0, 0, 0
	for idx, speed_list in enumerate(pos_speed_list):
		for item in speed_list:
			pos = item[0]
			speed = item[1]
			if pos not in address_dict:
				error_count += 1
				if error_count & 15 == 0:
					print("\rAddress mapping infos  Right: %6d Wrong: %4d Missing: %4d"%(right_count, error_count, not_in_road), end = "")
			elif address_dict[pos]["street"] == "":
				not_in_road += 1
			else:
				right_count += 1
				road.add(address_dict[pos]["street"])
				if not address_dict[pos]["street"] in average_speed_list[idx]:
					average_speed_list[idx][address_dict[pos]["street"]] = []
				average_speed_list[idx][address_dict[pos]["street"]].append(speed)
		pos_speed_list[idx] = []
	print("\rAddress mapping infos  Right: %6d Wrong: %4d Missing: %4d"%(right_count, error_count, not_in_road))
	print(("There are totally %d points\n" +
		"Among them:\n" +
		"\t%d points can find its street name\n" +
		"\t%d points can find its address, but they don't have a street name\n" +
		"\t%d points can not find its address")%(right_count + not_in_road + error_count, right_count, not_in_road, error_count))
	pos_speed_list = []
	for idx, speed_list in enumerate(average_speed_list):
		print("\rhandle time intervel [" + str(idx) + ", " + str(idx + 1) + "]", end = "")
		for items in speed_list.keys():
			average_speed[idx][items] = sum(speed_list[items])/len(speed_list[items])
	print("\nFinished calculate average_speed")
	print("Begin to save road")
	np.save("road.npy", road)
	print("Save road into road.npy successfully")

def linear_interpolate():
	print("Begin linear interpolate for average_speed")
	road_list = list(road)
	for road_name in road_list:
		for i in range(0, interval_num):
			if road_name not in average_speed[i]:
				average_speed[i][road_name] = 0
			if average_speed[i][road_name] < 0:
				average_speed[i][road_name] = - average_speed[i][road_name]
	for road_name in road_list:
		i, j = 0, 0
		while i < interval_num:
			if i == 0 and average_speed[0][road_name] == 0:
				j += 1
				while j < interval_num and average_speed[j][road_name] == 0:
					j += 1
				if j == interval_num:
					break
				for k in range(1, j):
					average_speed[k][road_name] = k / j * average_speed[j][road_name]
				i = j
			while i < interval_num and average_speed[i][road_name] != 0:
				i += 1
			i -= 1
			j = i + 1
			while j < interval_num and average_speed[j][road_name] == 0:
				j += 1
			if j == interval_num:
				j -= 1
			for k in range(i + 1, j):
				average_speed[k][road_name] = (k - i) / (j - i) * average_speed[i][road_name] + (j - k) / (j - i) * average_speed[j][road_name]
			k = j
			if j == interval_num - 1:
				break
	print("Begin to save average_speed")
	np.save("average_speed" + npy_suffix, average_speed)
	print("Save average_speed into average_speed" + npy_suffix + " successfully")
	print("Finished linear interpolate")


def output_to_file(output_filename):
	tsv_filename = output_filename[:-3] + 'tsv'
	csv_filename = output_filename[:-3] + 'csv'

	print('Begin to output to ' + tsv_filename)
	interval = '\t'
	average_speed_file = open(tsv_filename, 'w', encoding='utf-8')
	average_speed_file.write("date");
	road_list = list(road)
	for road_name in road_list:
		average_speed_file.write(interval + road_name)
	for idx, speed_item in enumerate(average_speed):
		average_speed_file.write('\n')
		average_speed_file.write(str(start_unix_time+t_interval*idx))
		for road_name in road_list:
			if road_name in speed_item:
				average_speed_file.write(interval + str(speed_item[road_name]))
			else:
				average_speed_file.write(interval + '\t')
	average_speed_file.close()
	print("Output to " + tsv_filename + " successfully!")

	print('Begin to output to ' + csv_filename)
	interval = ','
	average_speed_file = open(csv_filename, 'w', encoding='utf-8')
	average_speed_file.write("date");
	road_list = list(road)
	for road_name in road_list:
		average_speed_file.write(interval + road_name)
	for idx, speed_item in enumerate(average_speed):
		average_speed_file.write('\n')
		average_speed_file.write(str(start_unix_time+t_interval*idx))
		for road_name in road_list:
			if road_name in speed_item:
				average_speed_file.write(interval + str(speed_item[road_name]))
			else:
				average_speed_file.write(interval + '0')
	average_speed_file.close()
	print("Output to " + csv_filename + " successfully!")


calc_pos_speed_bd09()
calc_average_speed_bd09()
linear_interpolate()
output_to_file("average_speed" + tsv_suffix)