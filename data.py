from flask import Flask, flash, redirect, render_template, request,url_for
from collections import OrderedDict
import pandas as pd
import pickle
from flask import jsonify
import numpy as np
import json
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth',200)




heatmap_file_1h = open("static/data/heatmap_data_1h","rb")
up_order_file_1h = open("static/data/up_order_data_1h_amap","rb")
down_order_file_1h = open("static/data/down_order_data_1h_amap","rb")
current_time_idx = 0

heatmap_data_all_1h = pickle.load(heatmap_file_1h)
uporder_data_all_1h = pickle.load(up_order_file_1h)
downorder_data_all_1h = pickle.load(down_order_file_1h)

heatmap_file_1h.close()
up_order_file_1h.close()
down_order_file_1h.close()
# heatmap_data_all_30min = pickle.load(heatmap_file_30min)
# uporder_data_all_30min = pickle.load(up_order_file_30min)
# downorder_data_all_30min = pickle.load(down_order_file_30min)
# heatmap_data_all_10min = pickle.load(heatmap_file_10min)
# uporder_data_all_10min = pickle.load(up_order_file_10min)
# downorder_data_all_10min = pickle.load(down_order_file_10min)

heatmap_data_all = heatmap_data_all_1h
uporder_data_all = uporder_data_all_1h
downorder_data_all = downorder_data_all_1h

heatmap_data = heatmap_data_all[0]
uporder_data = uporder_data_all[0]
downorder_data = downorder_data_all[0]
app = Flask(__name__)
print(heatmap_data[0])


@app.route('/')

@app.route("/data", methods=['GET', 'POST'])
def data():
    return render_template('index.html', heatmap_data=heatmap_data,
                           up_order=uporder_data, down_order=downorder_data)


@app.route("/slider", methods=['POST'])
def slider():
    global current_time_idx
    current_time_idx = int(request.form["time"])
    heatmap_data = heatmap_data_all[current_time_idx]
    uporder_data = uporder_data_all[current_time_idx]
    downorder_data = downorder_data_all[current_time_idx]
    result = {"heatmap_data": heatmap_data, "uporder_data":uporder_data, "downorder_data":downorder_data}
    return jsonify(result)

@app.route("/interval", methods=['POST'])
def interval():
    global heatmap_data_all, uporder_data_all, downorder_data_all, current_time_idx
    interval_idx = int(request.form["interval"])
    print(interval_idx)
    if interval_idx == 0:
        heatmap_file_1h = open("static/data/heatmap_data_1h", "rb")
        up_order_file_1h = open("static/data/up_order_data_1h_amap", "rb")
        down_order_file_1h = open("static/data/down_order_data_1h_amap", "rb")
        heatmap_data_all = pickle.load(heatmap_file_1h)
        uporder_data_all = pickle.load(up_order_file_1h)
        downorder_data_all = pickle.load(down_order_file_1h)
        heatmap_file_1h.close()
        up_order_file_1h.close()
        down_order_file_1h.close()
    elif interval_idx == 1:
        heatmap_file_30min = open("static/data/heatmap_data_30min", "rb")
        up_order_file_30min = open("static/data/up_order_data_30min_amap", "rb")
        down_order_file_30min = open("static/data/down_order_data_30min_amap", "rb")
        heatmap_data_all = pickle.load(heatmap_file_30min)
        uporder_data_all = pickle.load(up_order_file_30min)
        downorder_data_all = pickle.load(down_order_file_30min)
        heatmap_file_30min.close()
        up_order_file_30min.close()
        down_order_file_30min.close()
    elif interval_idx == 2:
        heatmap_file_10min = open("static/data/heatmap_data_10min", "rb")
        up_order_file_10min = open("static/data/up_order_data_10min_amap", "rb")
        down_order_file_10min = open("static/data/down_order_data_10min_amap", "rb")
        heatmap_data_all = pickle.load(heatmap_file_10min)
        uporder_data_all = pickle.load(up_order_file_10min)
        downorder_data_all = pickle.load(down_order_file_10min)
        heatmap_file_10min.close()
        up_order_file_10min.close()
        down_order_file_10min.close()
    current_time_idx = int(request.form["current_time"])
    print(current_time_idx)
    heatmap_data = heatmap_data_all[current_time_idx]
    uporder_data = uporder_data_all[current_time_idx]
    downorder_data = downorder_data_all[current_time_idx]
    result = {"heatmap_data": heatmap_data, "uporder_data":uporder_data, "downorder_data":downorder_data}
    return jsonify(result)

@app.route('/rank',methods=['POST'])
def rank():
    result=list(np.load('order_nums_list_5minutes_modified.npy'))
    return jsonify(result)

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(debug=True, host='localhost', port=80)