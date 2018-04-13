'''
Created on 12 Apr 2018

@author: naomiwang
'''
from dublinBikes import myDatabase
from dublinBikes.dataAnalytics import analytic
from datetime import datetime
import time
import numpy as np

def dailyBarChart(stationID):
    #dt = datetime.fromtimestamp(time.time())
    #print(dt)
    #dt = datetime.utcnow()
    
    #if isinstance(dt, str): 
    #    dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        
    #dt = dt.replace(hour = dt.hour + 1)
    #dt #replace minute
    #dt #replace second
    
    timeMilis = time.time()
    print(timeMilis)
    
    for i in range(0, 24):
        #dt = dt.replace(hour = dt.hour + i)
        timeMilis += 3600 #60 * 60 = 1h
        dt = datetime.fromtimestamp(timeMilis)
        #print(dt.hour, dt.weekday(), analytic(stationID, dt), dt)
        print(dt.hour, dt.weekday(), i, dt)
        
    
    #print(json.dumps(queryResult))

    #preparing JSON for front end
    #for dictionary in queryResult:
    #    for key in dictionary:
    #        if key == "Hour":
    #            print(dictionary[key])
    
    '''
    df = myDatabase.getBikeWeather(stationID)
    df['weekday'] = df['datetime'].dt.dayofweek
    df['Hour'] = df['datetime'].dt.hour
    df_thisweekday = df[df.weekday == weekday]
    #df_thisweekday.set_index(['Hour','weather'],inplace=True)
    df_thisweekday.set_index('weekday',inplace=True)
    #df = df_thisweekday[np.isfinite(df_thisweekday['availableBikes'])]
    df = df_thisweekday.drop(['humidity','temp','description','icon','datetime'],axis=1)
    df.groupby(['Hour', 'weather'])['availableBikes'].mean()
    print(df)
    #df.set_index('weekday',inplace=True)
    #print(df)
    #df = df[['weather','Hour','availableBikes']]
    #print(df)
    
    #df_resamp = df_thisweekday['availableBikes'].resample('H').mean()
    #print(df_resamp)
    '''
        
    #result = list(zip(map(lambda x:x.isoformat(), df_resamp.index ), df_resamp.values))
    #print(result)
    
dailyBarChart(42)

