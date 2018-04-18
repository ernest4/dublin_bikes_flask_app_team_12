'''
Created on 16 Mar 2018

@author: naomiwang
'''

from sqlalchemy import create_engine, Column,Integer,String,Boolean,Float,ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
import requests,json
import sys
import pandas as pd
from datetime import datetime,timedelta
import numpy as np

#  mysql -h dublinbike.cztklqig6iua.us-west-2.rds.amazonaws.com -P 3306 -u Admin -p

def getJCD():
    '''
    A function that parse jcd API and return the json file.
    Take care of the timestamp is too much detail.
    '''
    try:
        request = requests.get('''https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=8304657448dbad4944ed9a956f3855be76545f17''').content.decode('utf-8')
        stationsJson = json.loads(request)

        for item in stationsJson:
            if item["last_update"] != None:
                item["last_update"]//=1000
            else:
                pass
        return stationsJson
    
    except (ValueError, requests.exceptions.RequestException) as e:
        print(e)
        sys.exit(1)
    
engine = create_engine('mysql+pymysql://Admin:dublinBike@dublinbike.cztklqig6iua.us-west-2.rds.amazonaws.com:3306/pets',convert_unicode=True)
Base = declarative_base()

class Station(Base):
    '''Station class for SQLAlchemy, static table. Store the information that's relatively static.'''
    
    __tablename__ = 'Station'
    
    id = Column(Integer,primary_key=True)
    name = Column(String(100))
    address = Column(String(200))
    lat = Column(Float)
    lng = Column(Float)
    banking = Column(Boolean)
    bonus = Column(Boolean)
                  
class Dynamic(Base):
    '''Dynamic table class for SQLAlchemy. Populate the dynamic information.'''
    
    __tablename__ = 'Dynamic'
    
    stationID = Column(Integer,ForeignKey('Station.id'),primary_key=True)
    timeStamp = Column(Integer,primary_key=True)
    status = Column(String(100))
    bikeStands = Column(Integer)
    availableBikeStands = Column(Integer)
    availableBikes = Column(Integer)
    
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session=Session()

def populateStaticTable(stationsJson):
    '''Take the json file and parse the static part to populate the Station table.'''
    
    for s in stationsJson:
        station = Station(id=s["number"],name=s["name"],address=s["address"],lat=s["position"]["lat"],
                          lng=s["position"]["lng"],banking=s["banking"],bonus=s["bonus"])

        try:
            session.add(station)
            session.commit()
            
        except:
            session.rollback()
        finally:
            session.close()
            
    #print("populateStaticTable: executed")

def populateDynamicTable(stationsJson):
    '''take json file to populate Dynamic table.'''
    
    for s in stationsJson:
        dynamic = Dynamic(stationID=s["number"],timeStamp=s["last_update"],status = s["status"],
                          bikeStands = s["bike_stands"],availableBikeStands = s["available_bike_stands"],
                          availableBikes = s["available_bikes"])
        try:
            session.add(dynamic)
            session.commit()
            
        except:
            session.rollback()
        finally:
            session.close()
            
    #print("populateDynamicTable: executed")

def query():
    '''This query function will return a formatted json that contain the whole station information combined 
    with newest dynamic information.'''
    
    #statement tested on mysql monitor, working.
    statement='''
    select s.id, s.name, s.address, s.lat, s.lng, s.banking, s.bonus, 
        d.timeStamp, d.status, d.bikeStands, d.availableBikeStands, d.availableBikes
    from Station as s, (
        select stationID, timeStamp, status, bikeStands, availableBikeStands, availableBikes
        from Dynamic, (
                        select stationID as id, max(timeStamp ) as t 
                        from Dynamic 
                        group by id) as maxtimes 
        where stationID=id and timeStamp =t ) as d
    where s.id = d.stationID
    '''

    q=engine.execute(statement)

    preJSON = [dict(r) for r in q]
    for r in preJSON:
        r['number'] = r.pop('id')
        r['last_update'] = r.pop('timeStamp')
        r['bike_stands'] = r.pop('bikeStands')
        r['available_bike_stands'] = r.pop('availableBikeStands')
        r['available_bikes'] = r.pop('availableBikes')
        r['banking'] = bool(r['banking'])
        r['bonus'] = bool(r['bonus'])
        r['position'] = {"lat" : r.pop('lat'), "lng" : r.pop('lng')}
        
    print("query: executed")
    return json.dumps(preJSON)
    
#query()

def weeklyAvailableBikes(stationID):
    '''This function group the average bikes in different hour and weekday.
    Return a json file contains three features: hour(0-23), weekday(Mon-Sun represented by 0-6), average bike
    number in this hour.'''
    
    query='''
    select hour(from_unixtime(timeStamp)) as Hour, dayofweek(from_unixtime(timeStamp)) as Weekday,
     avg(availableBikes ) as avgAvailableBikes 
     from Dynamic where stationID='''+str(stationID)+'''
     group by hour(from_unixtime(timeStamp)), dayofweek(from_unixtime(timeStamp))'''

    q=engine.execute(query)
    
    preJSON = [dict(r) for r in q]
    for r in preJSON:
        r['avgAvailableBikes'] = float(r['avgAvailableBikes']) #converts Decimal() type to pure float type
    
    return preJSON
#weeklyAvailableBikes(42)

#==================================weather=============
'''
#-------populate history data---only need run once-----------------------
df = pd.read_csv('../tests/dublin_weather.csv')
df['datetime'] = pd.to_datetime(df['dt'], unit='s')

#weather means good wather or bad weather. True == Good weather, False== bad weather
df['weather.main'] = df['weather.main'].replace(['Clouds','Clear','Mist'],value=True)
df['weather.main'] = df['weather.main'].replace(['Drizzle','Fog','Rain','Snow'], value=False)
df['main.temp'] = df['main.temp']-273.15
df = df.drop(['city_id','clouds.all','dt_iso','main.pressure','main.temp_max','main.temp_min','rain.1h','rain.24h','rain.3h','wind.deg','wind.speed','weather.id'],axis=1)
df = df.drop_duplicates()
#print(df)
df.columns = ['dt','humidity','temp','description','icon','weather','datetime']
print(df.dtypes)
#print(df[df['dt'] == 1522627200])

def populateHistoryWeather(df):
    try:
        df.to_sql(name='weather', con=engine, if_exists = 'fail', index=False)
    except ValueError:
        pass
    engine.execute('alter table weather add primary key(datetime)')

#populateHistoryWeather(df)
#-------populate history data---only need run once above-----------------------
'''
def getOpenWeather():
    '''This function will parse open weather API to get current weather information. Return a json file.'''
    
    try:
        request = requests.get('http://openweathermap.org/data/2.5/weather?q=dublin&appid=b6907d289e10d714a6e88b30761fae22').content.decode('utf-8')
        currentWeatherJson = json.loads(request)

        if currentWeatherJson != None:
            return currentWeatherJson
        else:
            print('[Error 0] The weather json is empty.')
    
    except (ValueError, requests.exceptions.RequestException) as e:
        sys.exit(e)
        
#getOpenWeather()

weatherBase = automap_base()
weatherBase.prepare(engine,reflect=True)
HWeather=weatherBase.classes.weather

def populateCurrentWeather(weatherJson):
    '''Populate current weather into Weather table. Since the open weather API randomly update information.
    Therefore, if when this function is being called and the timestamp matched the latest record in Weather
    table, if will regenerate a new record using the same weather information but current timestamp.
    This is to ensure there is always at least one record each hour.'''
            
    currentWeather = HWeather(dt=weatherJson["dt"],
                              humidity=weatherJson["main"]["humidity"],
                              temp=weatherJson['main']['temp'],
                              description=weatherJson['weather'][0]['description'],
                              icon= weatherJson['weather'][0]['icon'],
                              weather= True if weatherJson['weather'][0]['main'] in ['Clouds','Clear','Mist'] else False,
                              datetime = datetime.fromtimestamp(weatherJson["dt"]).strftime('%Y-%m-%d %H:%M:%S'))

    if str(currentWeather.datetime) == str(session.query(HWeather).order_by(HWeather.datetime.desc()).first().datetime) and datetime.now() - session.query(HWeather).order_by(HWeather.datetime.desc()).first().datetime >= timedelta(minutes=60):
        currentWeather.datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("Open weather API fail to update within an hour, populating database with same data...")
    try:
        
        session.add(currentWeather)
        session.commit()
        
    except:
        session.rollback()
    finally:
        session.close()
            
    print("populateWeatherTable: executed")

#populateCurrentWeather(getOpenWeather())

#------------Combine weather with bike-------------

def getBikeWeather(stationID):
    '''This function will combine bike information with weather information by same day, same hour.'''
    
    weatherQuery = '''select * from weather'''
    df_weather = pd.read_sql_query(weatherQuery,engine)
    
    bikeQuery = ''' select * from Dynamic where stationID = '''+ str(stationID)
    df_bike = pd.read_sql_query(bikeQuery,engine)
     
    df_weather['Hourly'] = df_weather['datetime'].dt.floor('h')
    
    df_bike['Hourly'] = pd.to_datetime(df_bike['timeStamp'],unit='s').dt.floor('h')
    df_bike.set_index('Hourly',inplace=True)
    
    df_bike_resamp = df_bike['availableBikes'].resample('H').mean()
    
    result = pd.concat([df_weather.set_index('Hourly'), df_bike_resamp], axis=1, join='inner')
    
    result = result.drop(['humidity','temp','icon','dt'],axis=1)
    result = result[np.isfinite(result['availableBikes'])]
    #print(result) 
    return result
    
    

