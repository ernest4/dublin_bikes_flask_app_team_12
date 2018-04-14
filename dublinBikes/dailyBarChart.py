'''
Created on 12 Apr 2018

@author: ernest
'''

from dublinBikes.dataAnalytics import analytic
from datetime import datetime
import time
import json

def dailyBarChart(stationID):
    timeMilis = int(time.time() + 3600)
    occupancy24h = analytic(stationID)
    
    returnJSON = []
    for i in range(0, 24):
        dt = datetime.fromtimestamp(timeMilis).replace(minute = 0, second = 0)
        returnJSON.append({"Hour": dt.hour, "Weekday": dt.weekday(), "avgAvailableBikes": occupancy24h[i]})
        timeMilis += 3600 #60 * 60 = 1h
        
    return json.dumps(returnJSON)
    

