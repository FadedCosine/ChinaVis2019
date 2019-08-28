# ChinaVis2019

In recent years, with the rise of the network car platform, the deep integration of traffic and the Internet, the surge in the number of online car orders has caused urban congestion to become a phenomenal problem. This paper is based on the order data within 10 km of Chengdu China Modern Pentathlon Center on May 1, 2018 and the trajectory data within a radius of 10 km. The map visualization and heat map, contour and dispersion of the main view are used. The combination of dot plots reveals the spatial dimension of the data, the dynamic road ranking histogram and the line graph of the secondary view, and the multi-view collaborative visual analysis method is used to analyze traffic flow evolution, congestion analysis and give traffic grooming scheme.

Our data visualization project is shown as follows.

### data process
gcj02_to_bd09.py is used to get the gps infos list from origin data.

cal_average_speed is used to calculate the average speed of each road in each time interval

cal_order_nums is used to calculate the order nums of each road in each time interval

distance_classify is used to calculate the order nums percent within 1km to the the centerpre

processing.py is used to extract the heatmap data and order data. It need the original data be saved in "../20180501".

### run the application

After data extraction, the generated file should be save in "static/data".

Since the data we need is already generated,  just run data.py, then enter http://localhost:80/ in Chrome or Firefox to see the result.




