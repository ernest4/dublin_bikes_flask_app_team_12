'''
Created on 9 Apr 2018

@author: ernest, Xinyue Wang
'''

from dublinBikes import myDatabase
import pandas as pd
import numpy as np
#from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import requests,json,sys
from builtins import str
from datetime import datetime,timezone
import time

def getForecast():
    try:
        request = requests.get('http://openweathermap.org/data/2.5/forecast?q=dublin&appid=b6907d289e10d714a6e88b30761fae22').content.decode('utf-8')
        forecastJson = json.loads(request)
        #print(stationsJson[0])

        if forecastJson != None:
            #print(currentWeatherJson)
            return forecastJson
        else:
            print('[Error 0] The json is empty.')
    
    except (ValueError, requests.exceptions.RequestException) as e:
        #print(e)
        sys.exit(e)

#def toDatetime(dt):
    
#dt format:2018-04-11 23:32:00    
def analytic(stationID,dt):
#------------------------------------------------------------------------------ 
# Extract weekday and hour information from dt.
#------------------------------------------------------------------------------ 
    if isinstance(dt, str): 
        dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
    weekday = dt.weekday()
    hour = dt.hour
    while dt.hour % 3 != 0:
        dt = dt.replace(hour = dt.hour -1)
    timestamp = int(dt.replace(tzinfo=timezone.utc).timestamp())
    forecastJson = getForecast()
    description = None
    for i,dict in enumerate(forecastJson["list"]):
        if forecastJson["list"][i]["dt"] == timestamp:
            description = "description_"+ forecastJson["list"][i]["weather"][0]["description"]
            #description = forecastJson["list"][i]["weather"][0]["description"]
            if forecastJson["list"][i]["weather"][0]["main"] in ['Clouds','Clear','Mist']:
                weather = 1
            else:
                weather = 0
    #Good weather: ['Clouds','Clear','Mist']
    if description == None:
        sys.exit("[Error 1] Fail to extract description from json.")
    test = [weather,weekday,hour]
    #'description_Sky is Clear', is the dummy not shown
    desList = [ 'description_broken clouds', 'description_clear sky', 'description_few clouds', 'description_fog', 'description_light intensity drizzle', 'description_light intensity drizzle rain', 'description_light intensity shower rain', 'description_light rain', 'description_light shower sleet', 'description_mist', 'description_moderate rain', 'description_proximity shower rain', 'description_scattered clouds', 'description_shower rain']
    for d in desList:
        if d == description:
            test.append(1)
        else:
            test.append(0)
    #print(test)
    testSet = np.asarray(test).reshape(1,-1)
    
#------------------------------------------------------------------------------ 
# Random forest
#------------------------------------------------------------------------------ 
    bikeWeather = myDatabase.getBikeWeather(stationID)
    #bikeWeather = myDatabase.getBikeWeather(42) #testing
    #print(bikeWeather)
    
    #print(list(zip(map(lambda x:x.isoformat(), result.index ), result.values)))
    
    bikeWeather['weekday'] = bikeWeather['datetime'].dt.dayofweek
    #print(bikeWeather) 
    bikeWeather['Hour'] = bikeWeather['datetime'].dt.hour
    #print(bikeWeather)
    
    #dfAll = bikeWeather[np.isfinite(bikeWeather['availableBikes'])]
    #print(dfAll)
    
    #------------------------------------------------------------------------------ 
    # First training, using features:  description, weather, weekday, Hour
    # Target feature: availableBikes
    #df = dfAll.drop(['humidity','temp','icon'],axis=1)
    
    #df_dummies = bikeWeather.join(pd.get_dummies(bikeWeather,drop_first=True))
    labels = np.array(bikeWeather['availableBikes'])
    df_dummies = bikeWeather.drop(['humidity','temp','icon','availableBikes','datetime'],axis=1)
    df_dummies = pd.get_dummies(df_dummies,drop_first=True)
    print(df_dummies)
    
    #labels = np.array(df_dummies['availableBikes'])
    #features = df_dummies.drop(['humidity','temp','icon','availableBikes','datetime'],axis=1)
    #feature_list = list(features.columns)
    #print(feature_list)
    #['weather', 'weekday', 'Hour', 'description_Sky is Clear', 'description_broken clouds', 
    #'description_clear sky', 'description_few clouds', 'description_fog', 'description_light intensity drizzle', 
    #'description_light intensity drizzle rain', 'description_light intensity shower rain', 
    #'description_light rain',
    # 'description_light shower sleet', 'description_mist', 'description_moderate rain', 
    #'description_proximity shower rain', 'description_scattered clouds', 'description_shower rain']
    features = np.array(df_dummies)
    #print(features)
    '''
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.3, random_state = 47)
    
    #Baseline of simple average
    baseline_preds = np.mean(test_labels)
    baseline_errors = abs(baseline_preds - test_labels)
    #print(baseline_errors)
    print('Average baseline error: ', round(np.mean(baseline_errors), 2))
    #Average baseline error:  9.08
        '''
    rf = RandomForestRegressor(n_estimators = 100, random_state = 47)
    #rf.fit(train_features, train_labels)
    rf.fit(features,labels)
    predictions = rf.predict(testSet)
    #predictions = rf.predict(test_features)
    #errors = abs(predictions - test_labels)
    #print(errors)
    #print('Mean Absolute Error:', round(np.mean(errors), 2))
    #Mean Absolute Error: 3.36 
    #print(predictions[0])
    return predictions[0]

print(datetime.fromtimestamp(time.time() + 3600*3))
analytic(42, datetime.fromtimestamp(time.time() + 3600*3))
#pre:24.586715367965375
'''
#------------------------------------------------------------------------------ 
# Import tools needed for visualization
from sklearn.tree import export_graphviz
import pydot

# Pull out one tree from the forest
tree = rf.estimators_[5]

# Export the image to a dot file
export_graphviz(tree, out_file = 'tree.dot', feature_names = feature_list, rounded = True, precision = 1)

# Use dot file to create a graph
(graph, ) = pydot.graph_from_dot_file('tree.dot')

# Write graph to a png file
graph.write_png('tree.png')
'''


#print(list(zip(map(lambda x:x.isoformat(), bikeWeather.index ), bikeWeather .values)))
