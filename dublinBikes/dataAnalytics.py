'''
Created on 9 Apr 2018

@author: ernest
'''

from dublinBikes import myDatabase
import pandas as pd

bikeWeather = myDatabase.getBikeWeather(42) #testing

print(bikeWeather)

#print(list(zip(map(lambda x:x.isoformat(), bikeWeather.index ), bikeWeather .values)))