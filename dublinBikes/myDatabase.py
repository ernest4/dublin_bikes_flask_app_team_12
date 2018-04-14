'''
Created on 16 Mar 2018

@author: naomiwang
'''

from sqlalchemy import create_engine, Column,Integer,String,Boolean,Float,ForeignKey,DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
import requests,json
import sys
import pandas as pd
from datetime import datetime,timedelta
from unittest.mock import inplace
import numpy as np

#  mysql -h dublinbike.cztklqig6iua.us-west-2.rds.amazonaws.com -P 3306 -u Admin -p

#Test Json file, comment out when using real API
#global request
#with open('../tests/stations0.json', 'rb') as f:
    #print("reading the file")
 #   request = f.read()
    #print("Finished.")
# End here

# Activate this line if pass test
def getJCD():
    try:
        request = requests.get('''https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=8304657448dbad4944ed9a956f3855be76545f17''').content.decode('utf-8')
        stationsJson = json.loads(request)
        #print(stationsJson[0])

        for item in stationsJson:
            #print(stationsJson[i])
            if item["last_update"] != None:
                item["last_update"]//=1000
                #stationsJson[i]["last_update"] = datetime.datetime.fromtimestamp(stationsJson[i]["last_update"])
                #print("datetime:",stationsJson[i]["last_update"])
                # Just in case I want to use weekday later:
                #datetime.fromtimestamp(ep/1000).strftime("%A")
            else:
                pass
        return stationsJson
    
    except (ValueError, requests.exceptions.RequestException) as e:
        print(e)
        sys.exit(1)
    
    
    
#print(stationsJson[0]["last_update"])
#print(stationsJson[0]["banking"])
#for station in stationsJson:
#    station["banking"] 
    
#This is a testing pets db, remember to modify~
engine = create_engine('mysql+pymysql://Admin:dublinBike@dublinbike.cztklqig6iua.us-west-2.rds.amazonaws.com:3306/pets',convert_unicode=True)

Base = declarative_base()

#testJson = [{"number":42,"name":"SMITHFIELD NORTH","address":"Smithfield North","position":{"lat":53.349562,"lng":-6.278198},"banking":True,"bonus":False,"status":"OPEN","contract_name":"Dublin","bike_stands":30,"available_bike_stands":22,"available_bikes":8,"last_update":1521214994000},
    #           {"number":30,"name":"PARNELL SQUARE NORTH","address":"Parnell Square North","position":{"lat":53.353462,"lng":-6.265305},"banking":True,"bonus":False,"status":"CLOSED","contract_name":"Dublin","bike_stands":20,"available_bike_stands":0,"available_bikes":0,"last_update":1521213487000}]
    
class Station(Base):
    __tablename__ = 'Station'
    
    id = Column(Integer,primary_key=True)
    name = Column(String(100))
    address = Column(String(200))
    #position = Column(JSON)
    lat = Column(Float)
    lng = Column(Float)
    banking = Column(Boolean)
    bonus = Column(Boolean)
    
    #{'number': 42, 'name': 'SMITHFIELD NORTH', 'address': 'Smithfield North', 'position': {'lat': 53.349562, 
    #'lng': -6.278198}, 'banking': True, 'bonus': False, 'status': 'OPEN', 'contract_name': 'Dublin', 'bike_stands': 30, 'available_bike_stands': 20, 'available_bikes': 10, 'last_update': 1521565405000}
    '''
    def __repr__(self):
        return '[{"id":'+str(self.id)+', "name":"'+self.name+'", "address":"'+self.address+'", "position": {"lat":'+\
            str(self.lat)+',"lng":'+str(self.lng)+'}, "banking":'+str(self.banking)+',"bonus":'+str(self.bonus)\
            +'}]'
    
    def as_dict(self):
        return str([{"id":self.id,"name":self.name,"address":self.address,"position":{"lat":self.lat,"lng":self.lng},\
                 "banking":self.banking,"bonus":self.bonus}])
    '''

                
class Dynamic(Base):
    #! Mind here the table name
    __tablename__ = 'Dynamic'
    
    stationID = Column(Integer,ForeignKey('Station.id'),primary_key=True)
    timeStamp = Column(Integer,primary_key=True)
    status = Column(String(100))
    bikeStands = Column(Integer)
    availableBikeStands = Column(Integer)
    availableBikes = Column(Integer)
    '''
    def __repr__(self):
        return '[{"stationID":'+str(self.stationID)+',"timeStamp":'+str(self.timeStamp)+',"status":"'+self.status\
            +'","binkStands":'+str(self.bikeStands)+',"availableBikeStands":'+str(self.availableBikeStands)+\
            ',"availableBikes":'+str(self.availableBikes)+'}]'


    def as_dict(self):
        return [{'st'}]
    '''
    
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session=Session()

'''
station=Station(id= 42, name= 'SMITHFIELD NORTH', address= 'Smithfield North', lat= 53.349562, lng= -6.278198, banking= True, bonus= False)
print(station.as_dict()[125:])
json.loads(station.__repr__())
dynamic = Dynamic(stationID=42,timeStamp=1521565405000,status='open',bikeStands=30,availableBikeStands=20,availableBikes=10)
print(dynamic)
'''

def populateStaticTable(stationsJson):
    
    for s in stationsJson:
        station = Station(id=s["number"],name=s["name"],address=s["address"],lat=s["position"]["lat"],
                          lng=s["position"]["lng"],banking=s["banking"],bonus=s["bonus"])
        #print(station.position)
        try:
            session.add(station)
            session.commit()
            #session.close()
        except:
            session.rollback()
        finally:
            session.close()
            
    print("populateStaticTable: executed")

#for q in session.query(Station):
#   print("id:",q.id,"bonus:",q.bonus)
#populateStaticTable()

def populateDynamicTable(stationsJson):
    for s in stationsJson:
        dynamic = Dynamic(stationID=s["number"],timeStamp=s["last_update"],status = s["status"],
                          bikeStands = s["bike_stands"],availableBikeStands = s["available_bike_stands"],
                          availableBikes = s["available_bikes"])
        try:
            session.add(dynamic)
            session.commit()
            #session.close()
        except:
            session.rollback()
        finally:
            session.close()
            
    print("populateDynamicTable: executed")


#def newest(station=None):
#   if station == None:
def query():
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
    #q=session.query(Station,Dynamic).from_statement(text(statement1)).all()
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
    '''
    result=[]
    for weatherJson in q:
        result.append(weatherJson)
    print(result)
    j=[]
    for id,name,address,lat,lng,banking,bonus,timeStamp,status,bikeStands, availableBikeStands, availableBikes in result:
        j.append(dict["id"]=id)
    print(j)
    '''
    
#query()

def weeklyAvailableBikes(stationID):
    query='''
    select hour(from_unixtime(timeStamp)) as Hour, dayofweek(from_unixtime(timeStamp)) as Weekday,
     avg(availableBikes ) as avgAvailableBikes 
     from Dynamic where stationID='''+str(stationID)+'''
     group by hour(from_unixtime(timeStamp)), dayofweek(from_unixtime(timeStamp))'''

    q=engine.execute(query)
    
    preJSON = [dict(r) for r in q]
    for r in preJSON:
        r['avgAvailableBikes'] = float(r['avgAvailableBikes']) #converts Decimal() type to pure float type
    #print(l)
    #l[0]['avgAvailableBikes']
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
    try:
        request = requests.get('http://openweathermap.org/data/2.5/weather?q=dublin&appid=b6907d289e10d714a6e88b30761fae22').content.decode('utf-8')
        currentWeatherJson = json.loads(request)
        #print(stationsJson[0])

        if currentWeatherJson != None:
            #print(currentWeatherJson)
            return currentWeatherJson
        else:
            print('[Error 0] The weather json is empty.')
    
    except (ValueError, requests.exceptions.RequestException) as e:
        #print(e)
        sys.exit(e)
        
#getOpenWeather()

weatherBase = automap_base()
weatherBase.prepare(engine,reflect=True)
HWeather=weatherBase.classes.weather

def populateCurrentWeather(weatherJson):

    #for dt,datetime in session.query(HWeather.dt, HWeather.datetime):
    #    print("Testy:",dt,datetime)
    #print(type(weatherJson["dt"]))
            
    currentWeather = HWeather(dt=weatherJson["dt"],
                              humidity=weatherJson["main"]["humidity"],
                              temp=weatherJson['main']['temp'],
                              description=weatherJson['weather'][0]['description'],
                              icon= weatherJson['weather'][0]['icon'],
                              weather= True if weatherJson['weather'][0]['main'] in ['Clouds','Clear','Mist'] else False,
                              datetime = datetime.fromtimestamp(weatherJson["dt"]).strftime('%Y-%m-%d %H:%M:%S'))
    #print(currentWeather.datetime)
    #print(session.query(HWeather).order_by(HWeather.datetime.desc()).first().datetime)
    #print(datetime.now() - session.query(HWeather).order_by(HWeather.datetime.desc()).first().datetime < timedelta(minutes=60))
    #currentWeather.datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #print(str(currentWeather.datetime) == str(session.query(HWeather).order_by(HWeather.datetime.desc()).first().datetime))
    #print(datetime.now() - session.query(HWeather).order_by(HWeather.datetime.desc()).first().datetime >= timedelta(minutes=60))
    #print(datetime.now() - session.query(HWeather).order_by(HWeather.datetime.desc()).first().datetime)
    #print(timedelta(minutes=60))
    #currentWeather.datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if str(currentWeather.datetime) == str(session.query(HWeather).order_by(HWeather.datetime.desc()).first().datetime) and datetime.now() - session.query(HWeather).order_by(HWeather.datetime.desc()).first().datetime >= timedelta(minutes=60):
        currentWeather.datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("Open weather API fail to update within an hour, populating database with same data...")
    try:
        #print(currentWeather.datetime)
        session.add(currentWeather)
        session.commit()
        #session.close()
    except:
        session.rollback()
    finally:
        session.close()
            
    print("populateWeatherTable: executed")

#populateCurrentWeather(getOpenWeather())


#t= session.query(HWeather).order_by(HWeather.datetime.desc()).first()
#print(t.datetime)

#------------Combine weather with bike-------------


def getBikeWeather(stationID):
    weatherQuery = '''select * from weather'''
    df_weather = pd.read_sql_query(weatherQuery,engine)
    #print(df_weather)
    bikeQuery = ''' select * from Dynamic where stationID = '''+ str(stationID)
    df_bike = pd.read_sql_query(bikeQuery,engine)
    
    #df_weather['dayOfYear'] = df_weather['datetime'].dt.hour
    #print(df_weather['datetime']) 
    df_weather['Hourly'] = df_weather['datetime'].dt.floor('h')
#    print(df_weather['Hourly'])
    #print(df_weather)
    
    df_bike['Hourly'] = pd.to_datetime(df_bike['timeStamp'],unit='s').dt.floor('h')
    df_bike.set_index('Hourly',inplace=True)
    #print(df_bike['Hourly'])
    #print(df_bike)
    df_bike_resamp = df_bike['availableBikes'].resample('H').mean()
    #df_bike_resamp = df_bike_resamp[np.isfinite(df_bike_resamp['availableBikes'])]
    #print(df_bike_resamp) 
    
    #df1 = df_weather.set_index('Hourly').drop_duplicates(inplace=True)
    #df2 = df_bike_resamp.drop_duplicates(inplace=True)
    #print(df1)
    #print(df2)
    
    result = pd.concat([df_weather.set_index('Hourly'), df_bike_resamp], axis=1, join='inner')
    #print(result)
    
    result = result.drop(['humidity','temp','icon','dt'],axis=1)
    #df_dummies = bikeWeather.drop(['humidity','temp','icon','availableBikes','datetime'],axis=1)
    result = result[np.isfinite(result['availableBikes'])]
    #print(result)
    #print(list(zip(map(lambda x:x.isoformat(), result.index ), result.values))) 
    return result
    
print(getBikeWeather(42).iloc[-1])
    

