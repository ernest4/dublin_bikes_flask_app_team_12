'''
Created on 12 Apr 2018

@author: naomiwang
'''
from dublinBikes import myDatabase
from dublinBikes.dataAnalytics import analytic
from datetime import datetime
import time
import numpy as np
import json

def dailyBarChart(stationID):
    timeMilis = (time.time() + 3600)//1000*1000
    #print(timeMilis)
    #print(datetime.fromtimestamp(timeMilis))
    
    returnJSON = []
    #[{"Hour": 0, "Weekday": 1, "avgAvailableBikes": 17.0556},
    # {"Hour": 0, "Weekday": 2, "avgAvailableBikes": 23.0}, ...]
    for i in range(0, 24):
        dt = datetime.fromtimestamp(timeMilis)
        #print(dt.hour, dt.weekday(), analytic(stationID, dt), dt)
        #returnJSON.append({"Hour": dt.hour, "Weekday": dt.weekday(), "avgAvailableBikes": analytic(stationID, dt)})
        print(dt.hour, dt.weekday(), i, dt)
        returnJSON.append({"Hour": dt.hour, "Weekday": dt.weekday(), "avgAvailableBikes": i})
        timeMilis += 3600 #60 * 60 = 1h
        
    print(json.dumps(returnJSON))
    
    return json.dumps(returnJSON)
    
dailyBarChart(42)

