import datetime
import math
import pickle

PI = 3.14159265358979324 * 3000.0 / 180.0


gps_file_path = "../20180501/gps-20180501.txt"
order_file_path = "../20180501/order-uniq-20180501.txt"
gps_file = open("../20180501/gps-20180501.txt", "rt")
unix_ts = 1525140657
time = datetime.datetime.fromtimestamp(unix_ts)
def get_time_range(filename):
    gps_file = open(filename, "rt")
    time_list = []
    for line in gps_file:
        line_split = line.strip("\n").split(",")
        time_list.append(int(line_split[1]))
    min_unix_time = min(time_list)
    max_unix_time = max(time_list)
    print(datetime.datetime.fromtimestamp(min_unix_time))
    print(datetime.datetime.fromtimestamp(max_unix_time))

def get_heatmap(gps_file_name,time_interval):
    gps_file = open(gps_file_name,"rt")
    point_num = {}
    start_unix_time = 1525104000 # 2018-5-1 00:00:00
    end_unix_time = 1525190399 # 2018-5-1 23:59:59  左闭右闭
    interval_num = int((end_unix_time-start_unix_time) / time_interval) + 1
    points = [ {} for i in range(interval_num)]
    for line in gps_file:
        line_split = line.strip("\n").split(",")
        unix_ts = int(line_split[1])
        point_index = int((unix_ts - start_unix_time) / time_interval)
        position = line_split[2] + "," + line_split[3]
        if position not in points[point_index]:
            points[point_index][position] = 1
        else:
            points[point_index][position] += 1
    return points

def bd_encrypt(gcjLng, gcjLat):
	z = math.sqrt(gcjLng * gcjLng + gcjLat * gcjLat) + 0.00002 * math.sin(gcjLat * PI)
	theta = math.atan2(gcjLat, gcjLng) + 0.000003  * math.cos(gcjLng * PI)
	bdLng = z * math.cos(theta) + 0.0065
	bdLat = z * math.sin(theta) + 0.006
	return bdLng, bdLat

def heatmap_output_to_jsfile(points,file_name,interval_type):
    points_file = open(file_name,"w")
    points_list = []
    points_file.write("var heatmap_data_"+interval_type+" = [\n")
    max_count = 0
    for idx, interval_points in enumerate(points):
        points_list.append([])
        for position in interval_points.keys():
            position_split = position.split(",")
            item = {}
            item["lng"] = float(position_split[0])
            item["lat"] = float(position_split[1])
            item["lnglat"] = position_split[0] + "," + position_split[1]
            item["count"] = interval_points[position]
            if idx == 9:
                max_count = max(max_count,item["count"])
            points_list[idx].append(item)
    for idx,items in enumerate(points_list):
        if idx == 0:
            points_file.write(str(items) + '\n')
        else:
            points_file.write(',' + str(items) + '\n')
    points_file.write('];')
    points_file.close()
    print(max_count)
    return points_list

def heatmap_dump_to_jsfile(points,file_name):
    points_file = open(file_name,"wb")
    points_list = []
    max_count = 0
    for idx, interval_points in enumerate(points):
        points_list.append([])
        for position in interval_points.keys():
            position_split = position.split(",")
            item = {}
            item["lng"] = float(position_split[0])
            item["lat"] = float(position_split[1])
            item["lnglat"] = position_split[0] + "," + position_split[1]
            item["count"] = interval_points[position]
            if idx == 9:
                max_count = max(max_count,item["count"])
            points_list[idx].append(item)
    pickle.dump(points_list,points_file)
    points_file.close()


def order_output_to_jsfile(points,file_name,type,interval_type):
    points_file = open(type + file_name,"wb")
    points_file.write("var "+type+"_order_"+interval_type+" = [\n")

    for idx,items in enumerate(points):
        if idx == 0:
            points_file.write(str(items) + '\n')
        else:
            points_file.write(',' + str(items) + '\n')
    points_file.write('];')

    points_file.close()

def order_dump_to_jsfile(points,file_name,type):
    points_file = open(type + file_name,"wb")
    pickle.dump(points,points_file)
    points_file.close()

def get_order_heatmap(file_path,time_interval):
    order_file = open(file_path, "rt")
    point_num = {}
    start_unix_time = 1525104000  # 2018-5-1 00:00:00
    end_unix_time = 1525190399  # 2018-5-1 23:59:59  左闭右闭
    interval_num = int((end_unix_time - start_unix_time) / time_interval) + 1
    up_points = [[] for i in range(interval_num)]
    down_points = [[] for i in range(interval_num)]
    for line in order_file:
        line_split = line.strip("\n").split(",")
        up_unix_ts = int(line_split[1])
        up_point_index = int((up_unix_ts - start_unix_time) / time_interval)
        down_unix_ts = int(line_split[2])
        down_point_index = int((down_unix_ts - start_unix_time) / time_interval)
        if down_point_index >= interval_num:
            continue
        # line_split[3], line_split[4] = bd_encrypt(float(line_split[3]), float(line_split[4]))
        # line_split[5], line_split[6] = bd_encrypt(float(line_split[5]), float(line_split[6]))
        up_points[up_point_index].append([[str(line_split[3]), str(line_split[4])],[str(line_split[5]), str(line_split[6])]])
        down_points[down_point_index].append([[str(line_split[3]), str(line_split[4])],[str(line_split[5]), str(line_split[6])]])

    return up_points, down_points



# get_time_range(file_path)
start_unix_time = 1525104000 # 2018-5-1 00:00:00
end_unix_time = 1525190399 # 2018-5-1 23:59:59  左闭右闭
heat_map_points = get_heatmap(gps_file_path,60*10)
# heatmap_output_to_jsfile(heat_map_points,"heatmap_data_10min.js","10min")
heatmap_dump_to_jsfile(heat_map_points,"heatmap_data_10min")
up_points, down_points = get_order_heatmap(order_file_path,60*10)
# order_output_to_jsfile(up_points,"_order_data_10min_amap.js","up","10min")
# order_output_to_jsfile(down_points,"_order_data_10min_amap.js","down","10min")
order_dump_to_jsfile(up_points,"_order_data_10min_amap","up")
order_dump_to_jsfile(down_points,"_order_data_10min_amap","down")

heat_map_points = get_heatmap(gps_file_path,60*30)
# heatmap_output_to_jsfile(heat_map_points,"heatmap_data_30min.js","30min")
heatmap_dump_to_jsfile(heat_map_points,"heatmap_data_30min")
up_points, down_points = get_order_heatmap(order_file_path,60*30)
# order_output_to_jsfile(up_points,"_order_data_30min_amap.js","up","30min")
# order_output_to_jsfile(down_points,"_order_data_30min_amap.js","down","30min")
order_dump_to_jsfile(up_points,"_order_data_30min_amap","up")
order_dump_to_jsfile(down_points,"_order_data_30min_amap","down")


heat_map_points = get_heatmap(gps_file_path,60*60)
# heatmap_output_to_jsfile(heat_map_points,"heatmap_data_1h.js","1h")
heatmap_dump_to_jsfile(heat_map_points,"heatmap_data_1h")
up_points, down_points = get_order_heatmap(order_file_path,60*60)
# order_output_to_jsfile(up_points,"_order_data_1h_amap.js","up","1h")
# order_output_to_jsfile(down_points,"_order_data_1h_amap.js","down","1h")
order_dump_to_jsfile(up_points,"_order_data_1h_amap","up")
order_dump_to_jsfile(down_points,"_order_data_1h_amap","down")