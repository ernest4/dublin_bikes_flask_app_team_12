'''
Created on 14 Mar 2018

@author: naomiwang
'''

from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.automap import automap_base

engine = create_engine('mysql+pymysql://Admin:dublinBike@dublinbike.cztklqig6iua.us-west-2.rds.amazonaws.com:3306/pets',convert_unicode=True)

#Base=declarative_base()
Base=automap_base()
Base.prepare(engine,reflect=True)
Cats=Base.classes.cats

#Session = sessionmaker(bind=engine)
session=Session(engine)

for name, owner in session.query(Cats.name, Cats.owner):
    print("Cat Name:",name,"| Owned by:",owner)
    