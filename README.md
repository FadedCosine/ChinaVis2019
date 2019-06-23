# ChinaVis2019
ChinaVis2019 for SJTU CS239
=======
#### data process
gcj02_to_bd09.py is used to get the gps infos list from origin data.

cal_average_speed is used to calculate the average speed of each road in each time interval

cal_order_nums is used to calculate the order nums of each road in each time interval

distance_classify is used to calculate the order nums percent within 1km to the the centerpre

processing.py is used to extract the heatmap data and order data. It need the original data be saved in "../20180501".

#### run the application

After data extraction, the generated file should be save in "static/data".

Since the data we need is already generated,  just run data.py, then enter http://localhost:80/ in Chrome or Firefox to see the result.




