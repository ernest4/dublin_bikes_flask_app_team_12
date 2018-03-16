'''
Created on 16 Mar 2018

@author: naomiwang
'''

from sqlalchemy import create_engine, Column,Integer,String,Boolean,Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import requests,json

def populateStaticTable():
    request = requests.get('https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=8304657448dbad4944ed9a956f3855be76545f17').content
    stationsJson = json.loads(request)
    #print(stationsJson[0]["banking"])
    #for station in stationsJson:
     #    station["banking"]
    
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
    
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session=Session()
    
    for s in stationsJson:
        station = Station(id=s["number"],name=s["name"],address=s["address"],lat=s["position"]["lat"],lng=s["position"]["lng"],banking=s["banking"],bonus=s["bonus"])
        #print(station.position)
        session.add(station)
    session.commit()

#for q in session.query(Station):
 #   print("id:",q.id,"bonus:",q.bonus)
  
  