# -*- coding: UTF-8 -*-
import numpy as np
import math
import os

accuracy = 5

source_file = list()

EARTH_REDIUS = 6378.137
PI_x = 3.14159265358979324 * 3000.0 / 180.0
gcj_file = '../20180501/gps-20180501.txt'
npy_filename = "bd09_data_tuple.npy"


lng, lat = 0.0, 0.0

def bd_encrypt(gcjLng, gcjLat):
	z = math.sqrt(gcjLng * gcjLng + gcjLat * gcjLat) + 0.00002 * math.sin(gcjLat * PI_x)
	theta = math.atan2(gcjLat, gcjLng) + 0.000003  * math.cos(gcjLng * PI_x)
	bdLng = z * math.cos(theta) + 0.0065
	bdLat = z * math.sin(theta) + 0.006
	return (round(bdLng, accuracy), round(bdLat, accuracy))

def read_file(filename):
	if os.path.exists(npy_filename):
		global source_file
		raw_file = np.load(npy_filename)
		source_file = raw_file.tolist()
		print(npy_filename + " exists already!")
		return
	print("begin read file " + filename)
	last_order_name = ""
	global pos_index
	order_index = -1
	pos_index = 0
	line_index = 0
	gps_raw_file = open(filename,'rt',encoding='utf-8')
	for line in gps_raw_file:
		line_index += 1
		line_split = line.strip("\n").split(",")
		if line_split[0] != last_order_name:
			last_order_name = line_split[0]
			pos_index = 0
			order_index += 1
			source_file.append([])
		bd_pos = bd_encrypt(float(line_split[2]), float(line_split[3]))
		source_file[order_index].append([])
		source_file[order_index][pos_index].append(int(line_split[1]))
		source_file[order_index][pos_index].append(bd_pos)
		pos_index += 1
		if order_index % 37 == 0:
			print("\rorder index: %-5d line index: %-6d"%(order_index + 1, line_index), end = "")
	print("\rorder index: %-5d line index: %-6d"%(order_index + 1, line_index))


read_file(gcj_file)
if not os.path.exists(npy_filename):
	np.save(npy_filename, source_file)

print('data format:')
print('[\n[[], [], ...],\t// 订单 1\n[[], [], ...],\t// 订单 2\n...\n]')
print('data[0][0:4]:')
print(source_file[0][0:4])
print('data[0][0]:')
print(source_file[0][0])





