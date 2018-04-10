'''
Created on 9 Apr 2018

@author: ernest
'''

from dublinBikes import myDatabase
import pandas as pd
import numpy as np


#def analytic(weekday, hour, weather):
bikeWeather = myDatabase.getBikeWeather(42) #testing

#print(bikeWeather)

#print(list(zip(map(lambda x:x.isoformat(), result.index ), result.values)))

bikeWeather['weekday'] = bikeWeather['datetime'].dt.dayofweek
#print(bikeWeather) 
bikeWeather['Hour'] = bikeWeather['datetime'].dt.hour
#print(bikeWeather)

df = bikeWeather[np.isfinite(bikeWeather['availableBikes'])]
print(df)



