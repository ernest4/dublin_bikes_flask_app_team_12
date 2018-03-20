'''
Created on 16 Mar 2018

@author: naomiwang
'''

from sqlalchemy import create_engine, Column,Integer,String,Boolean,Float,ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import requests,json

#  mysql -h dublinbike.cztklqig6iua.us-west-2.rds.amazonaws.com -P 3306 -u Admin -p

#Test Json file, comment out when using real API
global request
with open('../tests/stations0.json', 'rb') as f:
    #print("reading the file")
    request = f.read()
    #print("Finished.")
# End here

# Activate this line if pass test
#request = requests.get('''https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=8304657448dbad4944ed9a956f3855be76545f17''').content
    
stationsJson = json.loads(request)
print(stationsJson[0])
for i,item in enumerate(stationsJson):
    #print(stationsJson[i])
    if stationsJson[i]["last_update"] != None:
        stationsJson[i]["last_update"]//=1000
    else:
        pass
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

class Dynamic(Base):
    __tablename__ = 'Dynamic'
    
    stationID = Column(Integer,ForeignKey('Station.id'),primary_key=True)
    timeStamp = Column(Integer(),primary_key=True)
    status = Column(String(100))
    bikeStands = Column(Integer)
    availableBikeStands = Column(Integer)
    availableBikes = Column(Integer)
    
    
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session=Session()

def populateStaticTable():
    
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

#for q in session.query(Station):
#   print("id:",q.id,"bonus:",q.bonus)
#populateStaticTable()

def populateDynamicTable():
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
#populateDynamicTable()
    