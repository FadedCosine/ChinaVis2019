# -*- coding: UTF-8 -*-

import os
import numpy as np

start_unix_time = 1525104000 # 2018-5-1 00:00:00
end_unix_time = 1525190399 # 2018-5-1 23:59:59  左闭右闭
t_interval = 60 * 60
interval_num = int((end_unix_time-start_unix_time) / t_interval) + 1

if t_interval < 60 * 60:
	tsv_suffix = "_" + str(int(t_interval/60)) + "minutes.tsv"
	npy_suffix = "_" + str(int(t_interval/60)) + "minutes.npy"
else:
	tsv_suffix = "_" + str(int(t_interval/3600)) + "hour.tsv"
	npy_suffix = "_" + str(int(t_interval/3600)) + "hour.npy"

order_nums_list = []

road = set()

def calc_order_nums_list():
	road_file = np.load("road.npy")
	global road
	road = set(road_file.tolist())
	if os.path.exists("order_nums_list" + npy_suffix):
		print("order_nums_list" + npy_suffix + " already exists, we can just load it!")
		print("Loading ...", end = "")
		raw_file = np.load("order_nums_list" + npy_suffix)
		global order_nums_list
		order_nums_list = raw_file.tolist()
		print("\nLoad order_nums_list" + npy_suffix + " successfully")
		return
	print("Begin to load bd09_data_tuple.npy")
	print("Loading ...", end = "")
	raw_file = np.load("bd09_data_tuple.npy")
	order_list = raw_file.tolist()
	print("\nLoad bd09_data_tuple.npy successfully")
	print("Begin to load address_dict.npy")
	print("Loading ...", end = "")
	address_dict_file = np.load("address_dict.npy")
	address_dict = address_dict_file.item()
	print("\nLoad address_dict.npy successfully")
	default_nums = []
	for i in range(interval_num):
		default_nums.append(0)
		order_nums_list.append({})
	error_count, right_count, missing_count = 0, 0, 0
	road_order_dict = dict()
	for order in order_list:
		road_order_dict.clear()
		for item in order:
			time = item[0]
			pos = item[1]
			if pos not in address_dict:
				error_count += 1
				if error_count & 15 == 0:
					print("\rAddress mapping infos  Right: %6d Wrong: %4d Missing: %4d"%(right_count, error_count, missing_count), end = "")
			elif address_dict[pos]['street'] == "":
				missing_count += 1
			else:
				right_count += 1
				road.add(address_dict[pos]['street'])
				time_index = int ((time - start_unix_time) / t_interval)
				if address_dict[pos]['street'] not in road_order_dict:
					road_order_dict[address_dict[pos]['street']] = set()
				road_order_dict[address_dict[pos]['street']].add(time_index)
		for road_name in road_order_dict.keys():
			time_list = list(road_order_dict[road_name])
			for time_idx in time_list:
				if road_name not in order_nums_list[time_idx]:
					order_nums_list[time_idx][road_name] = 0
				order_nums_list[time_idx][road_name] += 1
	print("\nThere are totally %d orders"%(len(order_list)))
	print("Begin to save order_nums_list")
	np.save("order_nums_list" + npy_suffix, order_nums_list)
	print("Save order_nums_list into order_nums_list" + npy_suffix + " successfully")

def output_to_file(output_filename):
	tsv_filename = output_filename[:-3] + 'tsv'
	csv_filename = output_filename[:-3] + 'csv'

	print('Begin to output to ' + tsv_filename)
	interval = '\t'
	order_nums_file = open(tsv_filename, 'w', encoding='utf-8')
	order_nums_file.write("date");
	road_list = list(road)
	for road_name in road_list:
		order_nums_file.write(interval + road_name)
	for idx, order_item in enumerate(order_nums_list):
		order_nums_file.write('\n')
		order_nums_file.write(str(start_unix_time+t_interval*idx))
		for road_name in road_list:
			if road_name in order_item:
				order_nums_file.write(interval + str(order_item[road_name]))
			else:
				order_nums_file.write(interval + '0')
	order_nums_file.close()
	print("Output to " + tsv_filename + " successfully")

	print('Begin to output to ' + csv_filename)
	interval = ','
	order_nums_file = open(csv_filename, 'w', encoding='utf-8')
	order_nums_file.write("date");
	road_list = list(road)
	for road_name in road_list:
		order_nums_file.write(interval + road_name)
	for idx, order_item in enumerate(order_nums_list):
		order_nums_file.write('\n')
		order_nums_file.write(str(start_unix_time+t_interval*idx))
		for road_name in road_list:
			if road_name in order_item:
				order_nums_file.write(interval + str(order_item[road_name]))
			else:
				order_nums_file.write(interval + '0')
	order_nums_file.close()
	print("Output to " + csv_filename + " successfully")

calc_order_nums_list()
output_to_file("order_nums" + tsv_suffix)






