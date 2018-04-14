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
from datetime import datetime

#------------------------------------------------------------------------------
# Get forecast from open weather API, return a json file.
#------------------------------------------------------------------------------ 
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

#------------------------------------------------------------------------------ 
# Function return a available bikes number.
#------------------------------------------------------------------------------ 
def analytic(stationID):
    #Start with time of now.
    weekday = datetime.utcnow().weekday()
    hour = datetime.utcnow().hour
    
    bikeWeather = myDatabase.getBikeWeather(stationID)
    forecastJson = getForecast()
    testSet = []
    desList = [ 'description_broken clouds', 'description_clear sky', 'description_few clouds', 'description_fog', 'description_light intensity drizzle', 'description_light intensity drizzle rain', 'description_light intensity shower rain', 'description_light rain', 'description_light shower sleet', 'description_mist', 'description_moderate rain', 'description_proximity shower rain', 'description_scattered clouds', 'description_shower rain']
    
    # Because open weather API will return forecast for every 3 hours, 
    # so there could be gap between now and forecast.
     
    # Case1: two hours to open weather API forecast time.
    if datetime.utcnow().hour % 3 == 0:
        for i in range(1,3):
            dt = datetime.utcnow().replace(hour = datetime.utcnow().hour + i)
            #print(dt.hour)
            test=[bikeWeather.iloc[-1]['weather'], dt.weekday(), dt.hour]
            for d in desList:
                if d == "description_" + bikeWeather.iloc[-1]['description']:
                    test.append(1)
                else:
                    test.append(0)
            testSet.append(test) 
        
    # Case2: one hour to open weather API forecast time.
    if datetime.utcnow().hour % 3 == 1:
        dt = datetime.utcnow().replace(hour = datetime.utcnow().hour +1)
        #print(dt)
        test=[bikeWeather.iloc[-1]['weather'], dt.weekday(), dt.hour]
        for d in desList:
            if d == "description_" + bikeWeather.iloc[-1]['description']:
                test.append(1)
            else:
                test.append(0)
        testSet.append(test)  
    
    # Forecast part.
    # Using the same weather forecast for three hours to populate three test set with different 'hour'.
    i=0
    while len(testSet) <24:
        # Every 3 hour itself
        if i==0 or i % 3 == 0:
            dt = datetime.utcfromtimestamp(forecastJson["list"][i//3]["dt"])
            #print(dt)
        # Moving only hour forward.
        else:
            dt = datetime.utcfromtimestamp(forecastJson["list"][i//3]["dt"]).replace(hour = dt.hour +1)
            
        hour = dt.hour
        weekday = dt.weekday()
        description = "description_"+ forecastJson["list"][i//3]["weather"][0]["description"]
        #Good weather: ['Clouds','Clear','Mist']
        if forecastJson["list"][i//3]["weather"][0]["main"] in ['Clouds','Clear','Mist']:
            weather = 1
        else:
            weather = 0
        test = [weather,weekday,hour]
        for d in desList:
            if d == description:
                test.append(1)
            else:
                test.append(0)
        testSet.append(test)
        i+=1
        
    testSet = np.array([np.array(xi) for xi in testSet])
    #print(testSet)
    
    #------------------------------------------------------------------------------ 
    # Random forest Training, using all data
    #------------------------------------------------------------------------------ 
    
    bikeWeather['weekday'] = bikeWeather['datetime'].dt.dayofweek
    #print(bikeWeather) 
    bikeWeather['Hour'] = bikeWeather['datetime'].dt.hour
    #print(bikeWeather)
    
    #------------------------------------------------------------------------------ 
    # First training, using features:  description, weather, weekday, Hour
    # Target feature: availableBikes
    #df = dfAll.drop(['humidity','temp','icon'],axis=1)
    
    #df_dummies = bikeWeather.join(pd.get_dummies(bikeWeather,drop_first=True))
    # labels is the target feature.
    labels = np.array(bikeWeather['availableBikes'])
    # df_dummies are the training features.
    df_dummies = bikeWeather.drop(['availableBikes','datetime'],axis=1)
    df_dummies = pd.get_dummies(df_dummies,drop_first=True)
    #print(df_dummies)
    
    
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
    
    # Training and test split below...
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
    return predictions#[0]

#print(analytic(42))


'''
#------------------------------------------------------------------------------ 
# Import tools needed for visualization
#------------------------------------------------------------------------------ 
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
