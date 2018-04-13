'''
Created on 12 Apr 2018

@author: naomiwang
'''
from dublinBikes import myDatabase
from datetime import datetime
import numpy as np

def dailyBarChart(stationID,dt=datetime.utcnow()):
    if isinstance(dt, str): 
        dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
    weekday = dt.weekday()
    #dt = dt
    
    for i in range(0, 24):
        dt = dt.replace(hour = dt.hour + i)
        print(dt.weekday(), dt)
    
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

