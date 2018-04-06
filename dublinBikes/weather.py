'''
Created on 4 Apr 2018

@author: naomiwang
'''
from sqlalchemy import create_engine, Column,Integer,String,Boolean,Float,ForeignKey,DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import requests,json
import sys
import pandas as pd

df = pd.read_csv('../tests/dublin_weather.csv')
df['datetime'] = pd.to_datetime(df['dt'], unit='s')

#weather means good wather or bad weather. True == Good weather, False== bad weather
df['weather.main'] = df['weather.main'].replace(['Clouds','Clear','Mist'],value=True)
df['weather.main'] = df['weather.main'].replace(['Drizzle','Fog','Rain','Snow'], False)

print(df['weather.main'])

engine = create_engine('mysql+pymysql://Admin:dublinBike@dublinbike.cztklqig6iua.us-west-2.rds.amazonaws.com:3306/pets',convert_unicode=True)

Base = declarative_base()

class weatherInfo(Base):
    __tablename__ = "Weather"
    
    datetime = Column(DateTime,primary_key=True)
    weather = Column(Boolean)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session=Session()


    
    