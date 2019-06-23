# -*- coding: utf-8 -*-

import numpy as np


name="order_nums_list_5minutes"

INTERVAL=300
average_speed=list(np.load(name+".npy"))


result=np.zeros(len(average_speed)-1).astype(object)
for i in range(len(average_speed)-1):
    dic=average_speed[i]
    interval_item=list()
    for item in dic:
        if item in average_speed[i+1]:
            lastValue=average_speed[i+1][item]
        else:
            lastValue=0
        interval_item.append({
                'value':dic[item],
                'location':item,
                'time':1525104000+i*INTERVAL,
                'lastValue':lastValue
                })
    interval_item.sort(key=lambda x: x['value'],reverse=True)
    for j in range(len(interval_item)):
        interval_item[j]['rank']=j+1
    result[i]=interval_item
    
np.save(name+"_modified.npy",result)